# Copyright (c) 2025, AgriTheory and contributors
# For license information, please see license.txt

import datetime
import json

import frappe
import pytest
from erpnext.accounts.utils import get_balance_on
from frappe import _dict
from frappe.utils import flt

from check_run.check_run.doctype.check_run.check_run import (
	ach_only,
	build_nacha_file_from_payment_entries,
	calculate_payment_term_discount,
	check_for_draft_check_run,
	download_nacha,
	get_address,
	get_authorized_role_for_ach,
	get_balance,
	get_check_run_settings,
	get_entries,
)
from check_run.tests.tax_payable_helpers import (
	process_tax_payable_check_run_for_rows,
	tax_payable_check_run_entries,
)

year = datetime.date.today().year


@pytest.fixture
def cr():  # return draft check run
	cr_name = check_for_draft_check_run(
		company="Chelsea Fruit Co",
		bank_account="Primary Checking - Local Bank",
		payable_account="2110 - Accounts Payable - CFC",
	)
	cr = frappe.get_doc("Check Run", cr_name)
	cr.flags.in_test = True
	cr.posting_date = cr.end_date = datetime.date(year, 12, 31)
	cr.set_last_check_number()
	cr.set_default_payable_account()

	crs = get_check_run_settings(cr)
	entries = get_entries(cr)
	for row in entries.get("transactions"):
		row["pay"] = False
	cr.transactions = frappe.as_json(entries.get("transactions"))
	cr.save()
	return cr


@pytest.mark.order(10)
def test_get_entries(cr):
	crs = get_check_run_settings(cr)
	assert frappe.db.exists("Check Run Settings", crs)
	cr.transactions = frappe.utils.safe_json_loads(cr.transactions)
	assert len(cr.transactions) > 1
	# assert that each type of source document appears at least once
	assert any([doc.get("doctype") == "Purchase Invoice" for doc in cr.transactions])
	assert any([doc.get("doctype") == "Journal Entry" for doc in cr.transactions])
	assert any([doc.get("doctype") == "Expense Claim" for doc in cr.transactions])
	# assert that the invoice with installment payment schedule appears more than once
	assert len([doc.get("name") == f"ACC-PINV-{year}-00001 " for doc in cr.transactions]) > 1


@pytest.mark.order(11)
def test_process_check_run_on_hold_invoice_error(cr):
	cr.transactions = frappe.utils.safe_json_loads(cr.transactions)
	# try to pay invoice on hold to raise error
	for row in cr.transactions:
		if row.get("party") == "Liu & Loewen Accountants LLP":
			row["pay"] = True
			row["mode_of_payment"] = "Credit Card"
	cr.transactions = frappe.as_json(cr.transactions)
	cr.flags.in_test = True
	cr.save()
	with pytest.raises(
		frappe.exceptions.ValidationError, match=f"Purchase Invoice ACC-PINV-{year}-00020 is on hold"
	):
		cr.process_check_run()


@pytest.mark.order(12)
def test_process_check_run_on_hold_invoice_auto_release(cr):
	# Test Settings auto-release of on-hold invoices
	crs = get_check_run_settings(cr)
	crs.pre_check_overdue_items = True
	crs.save()
	cr.end_date = datetime.date(year, 12, 30)
	cr.transactions = get_entries(cr).get("transactions")
	for row in cr.transactions:
		if row.get("party") == "Liu & Loewen Accountants LLP" and row.get("on_hold") == True:
			assert not row.get("pay")  # test that on-hold invoices are not selected for payment
			row["pay"] = True
			row["mode_of_payment"] = "Credit Card"
		else:
			assert row["pay"]

	crs = get_check_run_settings(cr)
	crs.pre_check_overdue_items = False
	crs.automatically_release_on_hold_invoices = True
	crs.save()

	cr.end_date = datetime.date(year, 12, 31)
	cr.transactions = get_entries(cr).get("transactions")
	for row in cr.transactions:
		if row.get("party") == "Liu & Loewen Accountants LLP" and row.get("on_hold") == True:
			row["pay"] = True
			row["mode_of_payment"] = "Credit Card"
	cr.transactions = frappe.as_json(cr.transactions)
	cr.flags.in_test = True
	cr.save()

	try:
		cr.process_check_run()
	except frappe.exceptions.ValidationError:
		pytest.fail("Error raised on Check Run process when should have passed.")

	try:
		cr.process_check_run()
	except frappe.exceptions.ValidationError:
		pytest.fail("Error raised on Check Run process when should have passed.")


@pytest.mark.order(13)
def test_return_excluded_in_check_run(cr):
	# Test for ValidationError when Check Run only includes a return transaction
	cr.transactions = frappe.utils.safe_json_loads(cr.transactions)
	for row in cr.transactions:
		if row.get("party") == "Cooperative Ag Finance" and row.get("amount") < 0:
			raise ValueError("Default Settings should exclude this invoice from appearing")


@pytest.mark.order(14)
def test_return_included_in_check_run_error(cr):
	# Test for ValidationError when Check Run includes only a return transaction
	_transactions = get_entries(cr).get("transactions")
	settings = get_check_run_settings(cr)
	assert settings.allow_stand_alone_debit_notes == "No"
	settings.allow_stand_alone_debit_notes = "Yes"
	settings.save()
	cr.posting_date = cr.end_date = datetime.date(year, 12, 30)
	cr.transactions = ""
	transactions = get_entries(cr).get("transactions")
	assert transactions != _transactions
	for row in transactions:
		if row.get("party") == "Cooperative Ag Finance" and row.get("amount") < 0:
			row["pay"] = True
	cr.transactions = frappe.as_json(transactions)
	cr.flags.in_test = True
	cr.save()

	with pytest.raises(frappe.exceptions.ValidationError, match=f"Difference Amount must be zero"):
		cr.process_check_run()


@pytest.mark.order(15)
def test_return_offset_other_amounts(cr):
	# Test for offset when return applied to other invoices and net amount to pay is > 0
	party = "Cooperative Ag Finance"

	cr.transactions = frappe.utils.safe_json_loads(cr.transactions)
	total = 0.0
	for row in cr.transactions:
		if row.get("party") == party:
			total += row["amount"]
			row["pay"] = True
	cr.transactions = frappe.as_json(cr.transactions)
	cr.flags.in_test = True
	cr.save()
	cr.process_check_run()

	pe = frappe.get_doc("Payment Entry", {"party": party, "check_run": cr.name})
	assert total == pe.paid_amount == 9000.00


@pytest.mark.order(16)
def test_default_posting_date_config(cr):
	party = "HIJ Telecom, Inc"
	crs = get_check_run_settings(cr)
	assert crs.set_payment_entry_posting_date == "Use Today's Date"

	cr.transactions = frappe.utils.safe_json_loads(cr.transactions)
	# Pay one row for party
	for row in cr.transactions:
		if row.get("party") == party:
			row["pay"] = True
			break
	cr.transactions = frappe.as_json(cr.transactions)
	cr.flags.in_test = True
	cr.save()
	cr.process_check_run()

	pe = frappe.get_doc("Payment Entry", {"party": party, "check_run": cr.name})
	assert pe.posting_date == frappe.utils.getdate()


@pytest.mark.order(17)
def test_use_cr_posting_date_config(cr):
	party = "HIJ Telecom, Inc"
	crs = get_check_run_settings(cr)
	assert crs.set_payment_entry_posting_date == "Use Today's Date"

	crs.set_payment_entry_posting_date = "Use Check Run's Posting Date"
	crs.save()
	assert crs.set_payment_entry_posting_date == "Use Check Run's Posting Date"

	cr.transactions = frappe.utils.safe_json_loads(cr.transactions)
	# Pay one row for party
	for row in cr.transactions:
		if row.get("party") == party:
			row["pay"] = True
			break
	cr.transactions = frappe.as_json(cr.transactions)
	cr.flags.in_test = True
	cr.save()
	cr.process_check_run()

	pe = frappe.get_doc("Payment Entry", {"party": party, "check_run": cr.name})
	assert pe.posting_date == cr.posting_date

	crs.set_payment_entry_posting_date = "Use Today's Date"
	crs.save()
	assert crs.set_payment_entry_posting_date == "Use Today's Date"


@pytest.mark.order(18)
def test_calculate_payment_term_discount_function():
	# Create precise dates to test edge cases
	today = datetime.date.today()
	first_of_current_month = today.replace(day=1)
	last_month = first_of_current_month - datetime.timedelta(days=1)
	first_of_last_month = last_month.replace(day=1)
	last_day_of_last_month = last_month

	# Simulate being on the 9th day of current month (within 10-day discount period)
	simulated_today_within = first_of_current_month + datetime.timedelta(days=8)  # day 9
	# Simulate being on the 12th day of current month (outside 10-day discount period)
	simulated_today_outside = first_of_current_month + datetime.timedelta(days=11)  # day 12

	cases = [
		{
			"desc": "2% 10 Net 30 - within the discount period",
			"payment_term": "2% 10 Net 30",
			"posting_date": first_of_last_month,  # Invoice on 1st of previous month
			"payment_date": simulated_today_within,  # Payment on 9th of current month
			"amount": 1000.0,
			"expected_discount": 1000.0 * 0.02,
			"should_have_discount": True,
		},
		{
			"desc": "2% 10 Net 30 - outside the discount period",
			"payment_term": "2% 10 Net 30",
			"posting_date": first_of_last_month,  # Invoice on 1st of previous month
			"payment_date": simulated_today_outside,  # Payment on 12th of current month (outside period)
			"amount": 1000.0,
			"expected_discount": 0.0,
			"should_have_discount": False,
		},
		{
			"desc": "$20 10 Net 30 - within the discount period",
			"payment_term": "$20 10 Net 30",
			"posting_date": last_day_of_last_month,  # Invoice on last day of previous month
			"payment_date": simulated_today_within,  # Payment on 9th of current month
			"amount": 500.0,
			"expected_discount": min(20.0, 500.0),
			"should_have_discount": True,
		},
		{
			"desc": "$20 10 Net 30 - outside the discount period",
			"payment_term": "$20 10 Net 30",
			"posting_date": last_day_of_last_month,  # Invoice on last day of previous month
			"payment_date": simulated_today_outside,  # Payment on 12th of current month (outside period)
			"amount": 500.0,
			"expected_discount": 0.0,
			"should_have_discount": False,
		},
		{
			"desc": "2% 10 Net 30 - Invoice Date - last valid day",
			"payment_term": "2% 10 Net 30 - Invoice Date",
			"posting_date": today - datetime.timedelta(days=10),  # Exactly 10 days ago
			"payment_date": today,
			"amount": 800.0,
			"expected_discount": 800.0 * 0.02,
			"should_have_discount": True,
		},
		{
			"desc": "2% 10 Net 30 - Invoice Date - outside the discount period",
			"payment_term": "2% 10 Net 30 - Invoice Date",
			"posting_date": today - datetime.timedelta(days=11),  # 11 days ago (outside period)
			"payment_date": today,
			"amount": 800.0,
			"expected_discount": 0.0,
			"should_have_discount": False,
		},
		{
			"desc": "3% Net 30 - within valid month",
			"payment_term": "3% Net 30",
			"posting_date": first_of_last_month,  # Invoice from previous month
			"payment_date": today,  # Payment today (within validity month)
			"amount": 600.0,
			"expected_discount": 600.0 * 0.03,
			"should_have_discount": True,
		},
		{
			"desc": "3% Net 30 - outside valid month",
			"payment_term": "3% Net 30",
			"posting_date": first_of_last_month - datetime.timedelta(days=32),  # Invoice from 2 months ago
			"payment_date": today,  # Payment today (outside validity month)
			"amount": 600.0,
			"expected_discount": 0.0,
			"should_have_discount": False,
		},
	]

	for case in cases:
		transaction = _dict(
			{
				"name": f"Test-{case['desc']}",
				"payment_term": case["payment_term"],
				"amount": case["amount"],
				"posting_date": case["posting_date"],
			}
		)
		payment_date = case["payment_date"]
		discount_amount, has_discount = calculate_payment_term_discount(transaction, payment_date)

		assert (
			abs(discount_amount - case["expected_discount"]) < 0.01
		), f"{case['desc']}: expected {case['expected_discount']}, obtained {discount_amount}"
		assert (
			has_discount == case["should_have_discount"]
		), (
			f"{case['desc']}: expected has_discount={case['should_have_discount']}, obtained {has_discount}"
		)


@pytest.mark.order(19)
def test_cr_payment_term_discounts(cr):
	cr.transactions = frappe.utils.safe_json_loads(cr.transactions)
	payment_date = datetime.date.today()
	test_cases = []

	for row in cr.transactions:
		if row.get("doctype") != "Purchase Invoice":
			continue

		payment_term = row.get("payment_term", "")
		if not payment_term:
			continue

		invoice_name = row.get("name")
		amount = row.get("amount")
		posting_date = row.get("posting_date")

		transaction = _dict(
			{
				"name": invoice_name,
				"payment_term": payment_term,
				"amount": amount,
				"posting_date": posting_date,
			}
		)

		# Calculate discount for this transaction using today's date
		discount_amount, has_discount = calculate_payment_term_discount(transaction, payment_date)

		test_case = {
			"invoice": invoice_name,
			"payment_term": payment_term,
			"amount": amount,
			"posting_date": posting_date,
			"payment_date": payment_date,
			"discount_amount": discount_amount,
			"has_discount": has_discount,
		}
		test_cases.append(test_case)

		if payment_term in [
			"2% 10 Net 30",
			"$20 10 Net 30",
			"2% 10 Net 30 - Invoice Date",
			"3% Net 30",
		]:
			row["pay"] = True
			row["mode_of_payment"] = "Credit Card"

	assert len(test_cases) > 0, "No payment term discount test cases found"

	# Test Case 1: Invoices with percentage discounts (2%)
	percentage_discount_cases = [tc for tc in test_cases if "2%" in tc["payment_term"]]
	assert len(percentage_discount_cases) > 0, "No percentage discount test cases found"

	for case in percentage_discount_cases:
		if case["has_discount"]:
			expected_discount = case["amount"] * 0.02
			assert (
				abs(case["discount_amount"] - expected_discount) < 0.01
			), f"Percentage discount mismatch for {case['invoice']}: expected {expected_discount}, got {case['discount_amount']}"

	# Test Case 2: Invoices with amount-based discounts (fixed amount)
	amount_discount_cases = [tc for tc in test_cases if "$20 10 Net 30" in tc["payment_term"]]
	for case in amount_discount_cases:
		if case["has_discount"]:
			if case["payment_term"] == "3% Net 30":
				expected_discount = case["amount"] * 0.03
			else:
				expected_discount = min(20.0, case["amount"])

			assert (
				abs(case["discount_amount"] - expected_discount) < 0.01
			), f"Amount discount mismatch for {case['invoice']}: expected {expected_discount}, got {case['discount_amount']}"

	# Test Case 3: Expired discount scenarios
	expired_cases = [tc for tc in test_cases if not tc["has_discount"]]
	for case in expired_cases:
		assert (
			case["discount_amount"] == 0
		), f"Expired discount should be 0 for {case['invoice']}, got {case['discount_amount']}"


@pytest.mark.order(20)
def test_cr_process_with_discounts(cr):
	"""Test actual Check Run processing with discounts applied"""
	cr.transactions = frappe.utils.safe_json_loads(cr.transactions)
	payment_date = datetime.date.today()
	total_expected_discount = 0
	invoices_to_pay = []

	for row in cr.transactions:
		if row.get("doctype") == "Purchase Invoice" and row.get("payment_term") in [
			"2% 10 Net 30",
			"$20 10 Net 30",
			"3% Net 30",
			"2% 10 Net 30 - Invoice Date",
		]:
			row["pay"] = True
			row["mode_of_payment"] = "Credit Card"

			transaction = _dict(
				{
					"name": row["name"],
					"payment_term": row["payment_term"],
					"amount": row["amount"],
					"posting_date": row["posting_date"],
				}
			)

			discount_amount, has_discount = calculate_payment_term_discount(transaction, payment_date)

			if has_discount:
				total_expected_discount += discount_amount
				invoices_to_pay.append(
					{"name": row["name"], "amount": row["amount"], "expected_discount": discount_amount}
				)

	if len(invoices_to_pay) > 0:
		cr.transactions = frappe.as_json(cr.transactions)
		cr.flags.in_test = True
		cr.save()
		cr.process_check_run()

		payment_entries = frappe.get_all(
			"Payment Entry",
			filters={"check_run": cr.name},
			fields=["name", "total_allocated_amount", "paid_amount", "difference_amount"],
		)
		assert len(payment_entries) > 0, "No Payment Entries created"

		# Check if any payment entry has discount
		total_discount_in_pe = sum(pe.get("difference_amount", 0) for pe in payment_entries)
		if total_expected_discount > 0:
			assert (
				len(payment_entries) > 0
			), f"Expected Payment Entries to be created with discounts totaling {total_expected_discount}"


@pytest.mark.order(21)
def test_check_run_settings_create():
	company = "Chelsea Fruit Co"
	bank_account = "Primary Checking - Local Bank"
	pay_to_account = "2110 - Accounts Payable - CFC"
	crs_name = frappe.db.get_value(
		"Check Run Settings",
		{"bank_account": bank_account, "pay_to_account": pay_to_account},
	)
	if crs_name:
		frappe.delete_doc("Check Run Settings", crs_name, force=True)

	frappe.call(
		"check_run.check_run.doctype.check_run_settings.check_run_settings.create",
		company=company,
		bank_account=bank_account,
		pay_to_account=pay_to_account,
	)
	assert frappe.db.exists(
		"Check Run Settings", {"bank_account": bank_account, "pay_to_account": pay_to_account}
	)


@pytest.mark.order(22)
def test_get_check_run_settings_creates_when_missing(cr):
	crs_name = frappe.db.get_value(
		"Check Run Settings",
		{"bank_account": cr.bank_account, "pay_to_account": cr.pay_to_account},
	)
	frappe.delete_doc("Check Run Settings", crs_name, force=True)

	settings = get_check_run_settings(cr)
	assert settings.company == cr.company
	assert settings.bank_account == cr.bank_account
	assert settings.pay_to_account == cr.pay_to_account
	assert frappe.db.exists(
		"Check Run Settings",
		{"bank_account": cr.bank_account, "pay_to_account": cr.pay_to_account},
	)


@pytest.mark.order(23)
def test_get_balance(cr):
	gl_account = frappe.get_value("Bank Account", cr.bank_account, "account")
	expected = get_balance_on(gl_account, cr.posting_date)
	balance = get_balance(cr.as_dict())
	assert flt(balance) == flt(expected)
	assert flt(balance) > 0


@pytest.mark.order(24)
def test_get_address(cr):
	transactions = get_entries(cr).get("transactions")
	pi_row = next(
		t
		for t in transactions
		if t.get("doctype") == "Purchase Invoice" and t.get("party") == "HIJ Telecom, Inc"
	)
	assert (
		get_address(pi_row["party"], pi_row["party_type"], pi_row["doctype"], pi_row["name"])
		== "HIJ Telecom - Burlingame-Billing"
	)

	je_supplier_row = next(
		t
		for t in transactions
		if t.get("doctype") == "Journal Entry" and t.get("party_type") == "Supplier"
	)
	supplier_address = get_address(
		je_supplier_row["party"],
		je_supplier_row["party_type"],
		je_supplier_row["doctype"],
		je_supplier_row["name"],
	)
	assert supplier_address

	ec_row = next(t for t in transactions if t.get("doctype") == "Expense Claim")
	assert ec_row.get("party")
	assert ec_row.get("party_type") == "Employee"


@pytest.mark.order(25)
def test_ach_only(cr):
	cr_doc = frappe.get_doc("Check Run", cr.name)
	original_transactions = cr_doc.transactions
	all_transactions = frappe.utils.safe_json_loads(original_transactions)
	ach_transactions = [t for t in all_transactions if t.get("mode_of_payment") == "ACH/EFT"]
	assert ach_transactions

	cr_doc.transactions = json.dumps(
		[
			{"mode_of_payment": "Check", "pay": True},
			{"mode_of_payment": "Credit Card", "pay": True},
		]
	)
	result = cr_doc.ach_only()
	assert result.ach_only is False
	assert result.print_checks_only is True

	cr_doc.transactions = frappe.as_json(ach_transactions)
	result = cr_doc.ach_only()
	assert result.ach_only is True
	assert result.print_checks_only is False

	frappe.db.set_value(
		"Check Run", cr.name, "transactions", cr_doc.transactions, update_modified=False
	)
	try:
		module_result = ach_only(cr.name)
		assert module_result.ach_only is True
		assert module_result.print_checks_only is False
	finally:
		frappe.db.set_value(
			"Check Run", cr.name, "transactions", original_transactions, update_modified=False
		)


@pytest.mark.order(26)
def test_get_authorized_role_for_ach(cr):
	crs = get_check_run_settings(cr)
	original_role = crs.role_allowed_to_download_ach_file_multiple_times
	crs.role_allowed_to_download_ach_file_multiple_times = "Accounts User"
	crs.save()
	try:
		doc_payload = frappe.as_json(
			{"bank_account": cr.bank_account, "pay_to_account": cr.pay_to_account}
		)
		role = get_authorized_role_for_ach(doc_payload)
		assert role == "Accounts User"
	finally:
		crs.role_allowed_to_download_ach_file_multiple_times = original_role
		crs.save()


@pytest.mark.order(27)
def test_get_entries_accepts_json_string(cr):
	result = get_entries(frappe.as_json(cr.as_dict()))
	assert result.get("transactions")
	assert result.get("modes_of_payment")


@pytest.mark.order(28)
def test_not_outstanding_or_cancelled_excludes_paid_tax_row():
	_, transactions = tax_payable_check_run_entries()
	tax_row_entry = next(t for t in transactions if t.get("doctype") == "Sales Invoice")
	tax_row_name = tax_row_entry["name"]
	process_tax_payable_check_run_for_rows([tax_row_name])

	_, refreshed = tax_payable_check_run_entries()
	assert not any(t.get("name") == tax_row_name for t in refreshed)

	cr_name = check_for_draft_check_run(
		company="Chelsea Fruit Co",
		bank_account="Primary Checking - Local Bank",
		payable_account="2320 - Sales Tax Payable - CFC",
	)
	cr_doc = frappe.get_doc("Check Run", cr_name)
	assert cr_doc.not_outstanding_or_cancelled(tax_row_entry) is True


@pytest.mark.order(29)
def test_on_cancel_cascade_cancels_payment_entries(cr):
	"""
	Cancelling a submitted Check Run with cascade enabled reverses linked payments.

	| Account          |   Debit   |   Credit  |     Party              |
	| ---------------- | ---------:| ---------:| ---------------------- |
	| Accounts Payable |           | $1,000.00 | AgriTheory             |
	| Cash at Bank     | $1,000.00 |           |                        |
	"""
	crs = get_check_run_settings(cr)
	original_allow = crs.allow_cancellation
	original_cascade = crs.cascade_cancellation
	crs.allow_cancellation = 1
	crs.cascade_cancellation = 1
	crs.save()

	party = "AgriTheory"
	cr.transactions = frappe.utils.safe_json_loads(cr.transactions)
	for row in cr.transactions:
		if row.get("party") == party:
			row["pay"] = True
	cr.transactions = frappe.as_json(cr.transactions)
	cr.flags.in_test = True
	cr.save()
	cr.process_check_run()

	pe_name = frappe.db.get_value("Payment Entry", {"party": party, "check_run": cr.name})
	assert pe_name
	assert frappe.db.get_value("Payment Entry", pe_name, "docstatus") == 1
	submitted_gl = frappe.get_all(
		"GL Entry",
		filters={"voucher_no": pe_name, "is_cancelled": 0},
		pluck="name",
	)
	assert submitted_gl

	try:
		cr.reload()
		cr.cancel()
		assert frappe.db.get_value("Payment Entry", pe_name, "docstatus") == 2
		assert not frappe.get_all(
			"GL Entry",
			filters={"voucher_no": pe_name, "is_cancelled": 0},
			pluck="name",
		)
		for gl_name in submitted_gl:
			assert frappe.db.get_value("GL Entry", gl_name, "is_cancelled") == 1
	finally:
		crs.allow_cancellation = original_allow
		crs.cascade_cancellation = original_cascade
		crs.save()


@pytest.mark.order(35)
def test_render_check_pdf(cr):
	party = "HIJ Telecom, Inc"
	cr.transactions = frappe.utils.safe_json_loads(cr.transactions)
	for row in cr.transactions:
		if row.get("party") == party:
			row["pay"] = True
			row["mode_of_payment"] = "Check"
			break
	cr.transactions = frappe.as_json(cr.transactions)
	cr.flags.in_test = True
	cr.save()
	cr.process_check_run()

	cr.reload()
	cr.render_check_pdf()
	cr.reload()
	assert cr.status == "Ready to Print"
	check_pdfs = frappe.get_all(
		"File",
		filters={"attached_to_doctype": "Check Run", "attached_to_name": cr.name},
		fields=["file_name", "file_size"],
	)
	assert any(f.file_name.endswith(".pdf") and f.file_size > 0 for f in check_pdfs)


@pytest.mark.order(36)
def test_create_and_attach_positive_pay(cr):
	crs = get_check_run_settings(cr)
	original_attach = crs.attach_positive_pay
	original_format = crs.positive_pay_file_format
	crs.attach_positive_pay = 1
	crs.positive_pay_file_format = "CSV"
	crs.save()

	party = "HIJ Telecom, Inc"
	cr.transactions = frappe.utils.safe_json_loads(cr.transactions)
	for row in cr.transactions:
		if row.get("party") == party:
			row["pay"] = True
			row["mode_of_payment"] = "Check"
			break
	cr.transactions = frappe.as_json(cr.transactions)
	cr.flags.in_test = True
	cr.save()

	try:
		cr.process_check_run()
		cr.reload()
		cr.create_and_attach_positive_pay()
		positive_pay_files = frappe.get_all(
			"File",
			filters={"attached_to_doctype": "Check Run", "attached_to_name": cr.name},
			fields=["file_name"],
		)
		assert any("positive_pay" in f.file_name for f in positive_pay_files)
	finally:
		crs.attach_positive_pay = original_attach
		crs.positive_pay_file_format = original_format
		crs.save()


@pytest.mark.order(37)
def test_build_nacha_file_missing_aba_throws(cr):
	settings = get_check_run_settings(cr)
	bank = frappe.db.get_value("Bank Account", cr.bank_account, "bank")
	original_aba = frappe.db.get_value("Bank", bank, "aba_number")
	frappe.db.set_value("Bank", bank, "aba_number", None)
	try:
		with pytest.raises(frappe.ValidationError, match="ABA"):
			build_nacha_file_from_payment_entries(cr, [], settings)
	finally:
		frappe.db.set_value("Bank", bank, "aba_number", original_aba)


@pytest.mark.order(38)
def test_build_and_download_nacha_file(cr):
	party = "Exceptional Grid"
	cr.transactions = frappe.utils.safe_json_loads(cr.transactions)
	for row in cr.transactions:
		if row.get("party") == party:
			row["pay"] = True
			row["mode_of_payment"] = "ACH/EFT"
	cr.transactions = frappe.as_json(cr.transactions)
	cr.flags.in_test = True
	cr.save()
	cr.process_check_run()

	cr.reload()
	settings = get_check_run_settings(cr)
	nacha = cr.build_nacha_file(settings)
	nacha_content = nacha()
	assert isinstance(nacha_content, str)
	assert len(nacha_content) > 0

	download_nacha(cr.name)
	assert frappe.local.response.type == "download"
	assert frappe.local.response.filecontent
	assert len(frappe.local.response.filecontent) > 0
