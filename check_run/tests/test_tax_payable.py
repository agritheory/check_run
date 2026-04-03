# Copyright (c) 2026, AgriTheory and contributors
# For license information, please see license.txt

import datetime
import json

import frappe
import pytest
from erpnext.controllers.sales_and_purchase_return import make_return_doc
from erpnext.accounts.party import get_due_date
from frappe.utils import flt, getdate

from check_run.check_run.doctype.check_run.check_run import (
	check_for_draft_check_run,
	get_check_run_settings,
	get_entries,
)

year = datetime.date.today().year


@pytest.fixture
def tax_payable_cr():
	"""Draft Check Run targeting 2320 - Sales Tax Payable - CFC with all transactions marked to pay."""
	cr_name = check_for_draft_check_run(
		company="Chelsea Fruit Co",
		bank_account="Primary Checking - Local Bank",
		payable_account="2320 - Sales Tax Payable - CFC",
	)
	cr = frappe.get_doc("Check Run", cr_name)
	cr.flags.in_test = True
	cr.posting_date = cr.end_date = datetime.date(year, 12, 31)
	cr.set_last_check_number()
	cr.set_default_payable_account()
	cr.save()
	crs = get_check_run_settings(cr)
	crs.include_tax_payable = 1
	crs.include_purchase_invoices = 0
	crs.include_journal_entries = 0
	crs.include_expense_claims = 0
	crs.tax_payable = "Check"
	crs.number_of_invoices_per_voucher = 100
	crs.save()
	entries = get_entries(cr)
	for row in entries.get("transactions"):
		row["pay"] = True
	cr.transactions = frappe.as_json(entries.get("transactions"))
	cr.save()
	return cr


@pytest.mark.order(40)
def test_tax_payable_gl():
	"""
	| Account                 |   Debit  |  Credit  | Party                               |
	| ----------------------- | --------:| --------:| ----------------------------------- |
	| Accounts Receivable     | $138.13  |          | Almacs Food Group                   |
	| Sales                   |          | $130.00  |                                     |
	| 2320 Sales Tax Payable  |          |   $8.13  | Massachusetts Department of Revenue |
	"""
	si_name = frappe.get_value(
		"Sales Invoice",
		{"customer": "Almacs Food Group", "docstatus": 1},
		"name",
	)
	assert (
		si_name
	), "Expected a submitted Sales Invoice for Almacs Food Group from before_test fixtures"
	doc = frappe.get_doc("Sales Invoice", si_name)
	precision = frappe.get_precision(doc.doctype, "grand_total")

	ma_row = next((r for r in doc.taxes if r.party == "Massachusetts Department of Revenue"), None)
	assert (
		ma_row
	), "Expected a Massachusetts Department of Revenue tax row on the Almacs Food Group SI"
	expected_due_date = get_due_date(doc.posting_date, ma_row.party_type, ma_row.party, doc.company)
	assert ma_row.due_date == getdate(expected_due_date or doc.posting_date)

	gl1 = frappe.get_doc(
		"GL Entry", {"voucher_no": doc.name, "account": "2320 - Sales Tax Payable - CFC"}
	)
	assert flt(gl1.credit, precision) == flt(doc.total_taxes_and_charges, precision)
	assert gl1.party == "Massachusetts Department of Revenue"


@pytest.mark.order(41)
def test_tax_payable_check_run(tax_payable_cr):
	"""
	Processing the Sales Tax Payable Check Run creates a single Payment Entry
	for Massachusetts Department of Revenue covering the Almacs Food Group SI,
	and the PE name is linked back on every processed transaction row.
	"""
	cr = tax_payable_cr
	transactions = json.loads(cr.transactions)
	parties = {t.get("party") for t in transactions}
	assert "Massachusetts Department of Revenue" in parties
	cr.process_check_run()

	entries = get_entries(cr)
	processed = entries.get("transactions")
	assert processed, "Expected at least one processed transaction after Check Run"
	pe_name = processed[0].get("payment_entry")
	assert pe_name, "Expected payment_entry to be linked on processed transactions"
	assert all(t.get("payment_entry") == pe_name for t in processed)


@pytest.mark.order(42)
def test_tax_payable_due_date_from_supplier_terms():
	"""
	Verify that the due_date on a Sales Taxes and Charges row is computed from
	the tax authority supplier's payment terms (Due After Month End), not just
	copied from the invoice's posting_date.

	Massachusetts Department of Revenue has payment_terms = "Due After Month End",
	so a January 1 invoice's tax row should have a due_date of January 31 (or later),
	not January 1.
	"""
	si_name = frappe.get_value(
		"Sales Invoice",
		{"docstatus": 1, "taxes_and_charges": "MA Sales Tax - CFC"},
		"name",
	)
	assert si_name, "No submitted SI with MA Sales Tax - CFC found"
	si = frappe.get_doc("Sales Invoice", si_name)
	ma_tax_row = next(
		(row for row in si.taxes if row.party == "Massachusetts Department of Revenue"), None
	)
	assert ma_tax_row, "No Massachusetts Department of Revenue tax row found on SI"
	expected_due_date = get_due_date(
		si.posting_date, ma_tax_row.party_type, ma_tax_row.party, si.company
	)
	assert ma_tax_row.due_date == getdate(expected_due_date or si.posting_date)
	if expected_due_date:
		assert ma_tax_row.due_date != getdate(si.posting_date), (
			f"due_date {ma_tax_row.due_date} should differ from posting_date {si.posting_date} "
			"because Massachusetts Department of Revenue has 'Due After Month End' payment terms"
		)


@pytest.mark.order(43)
def test_sales_invoice_return_reduces_payable():
	"""
	Verify that submitting a return Sales Invoice reduces the outstanding_amount
	on the original invoice's Sales Taxes and Charges row to zero.

	Original SI:
	| Account                 |   Debit  |  Credit  | Party                               |
	| ----------------------- | --------:| --------:| ----------------------------------- |
	| Accounts Receivable     |  $13.81  |          | Downtown Deli                       |
	| Sales                   |          |  $13.00  |                                     |
	| 2320 Sales Tax Payable  |          |   $0.81  | Massachusetts Department of Revenue |

	Return SI (reversal):
	| Account                 |   Debit  |  Credit  | Party                               |
	| ----------------------- | --------:| --------:| ----------------------------------- |
	| 2320 Sales Tax Payable  |   $0.81  |          | Massachusetts Department of Revenue |
	| Sales                   |  $13.00  |          |                                     |
	| Accounts Receivable     |          |  $13.81  | Downtown Deli                       |
	"""
	si = frappe.new_doc("Sales Invoice")
	si.customer = "Downtown Deli"
	si.set_posting_time = 1
	si.company = "Chelsea Fruit Co"
	si.posting_date = getdate().replace(month=6, day=1)
	si.append("items", {"item_code": "Cloudberry", "qty": 10, "rate": 1.30})
	si.taxes_and_charges = "MA Sales Tax - CFC"
	taxes = frappe.call(
		"erpnext.controllers.accounts_controller.get_taxes_and_charges",
		master_doctype="Sales Taxes and Charges Template",
		master_name="MA Sales Tax - CFC",
	)
	for tax in taxes:
		si.append("taxes", tax)
	si.save()
	si.submit()

	ma_tax_row = next(row for row in si.taxes if row.party == "Massachusetts Department of Revenue")
	original_outstanding = flt(
		frappe.db.get_value("Sales Taxes and Charges", ma_tax_row.name, "outstanding_amount")
	)
	assert original_outstanding > 0.0, "Outstanding should be positive after SI submission"

	return_si = make_return_doc("Sales Invoice", si.name)
	return_si.posting_date = frappe.utils.add_days(si.posting_date, 1)
	return_si.save()
	return_si.submit()

	reduced_outstanding = flt(
		frappe.db.get_value("Sales Taxes and Charges", ma_tax_row.name, "outstanding_amount")
	)
	assert (
		reduced_outstanding == 0.0
	), f"Outstanding should be 0 after full return, got {reduced_outstanding}"


@pytest.mark.order(44)
def test_return_after_payable_remitted():
	"""
	Verify that creating a return SI after the tax payable has already been
	remitted via Payment Entry correctly:
	  - leaves the original SI's outstanding_amount at 0 (already paid, stays 0)
	  - sets the return SI's tax row outstanding_amount to a negative value
	    (representing the credit owed back from the tax authority)

	Timeline:
	  1. Submit SI → outstanding_amount = tax_amount
	  2. Submit Payment Entry → outstanding_amount = 0
	  3. Submit return SI → original outstanding stays 0, return row outstanding = -tax_amount
	"""
	si = frappe.new_doc("Sales Invoice")
	si.customer = "Cafe 27 Cafeteria"
	si.set_posting_time = 1
	si.company = "Chelsea Fruit Co"
	si.posting_date = getdate().replace(month=7, day=1)
	si.append("items", {"item_code": "Cloudberry", "qty": 10, "rate": 1.30})
	si.taxes_and_charges = "MA Sales Tax - CFC"
	taxes = frappe.call(
		"erpnext.controllers.accounts_controller.get_taxes_and_charges",
		master_doctype="Sales Taxes and Charges Template",
		master_name="MA Sales Tax - CFC",
	)
	for tax in taxes:
		si.append("taxes", tax)
	si.save()
	si.submit()

	ma_tax_row = next(row for row in si.taxes if row.party == "Massachusetts Department of Revenue")
	tax_row_name = ma_tax_row.name
	tax_amount = flt(ma_tax_row.tax_amount)

	gl_account = frappe.get_value(
		"Account",
		{"account_type": "Bank", "company": "Chelsea Fruit Co", "is_group": 0},
	)
	pe = frappe.new_doc("Payment Entry")
	pe.payment_type = "Pay"
	pe.posting_date = getdate().replace(month=7, day=25)
	pe.mode_of_payment = "Check"
	pe.company = "Chelsea Fruit Co"
	pe.bank_account = "Primary Checking - Local Bank"
	pe.paid_from = gl_account
	pe.paid_to = "2320 - Sales Tax Payable - CFC"
	pe.paid_to_account_currency = frappe.db.get_value("Account", gl_account, "account_currency")
	pe.paid_from_account_currency = pe.paid_to_account_currency
	pe.reference_no = "Test-Tax-Return-After-Paid"
	pe.reference_date = pe.posting_date
	pe.party_type = "Supplier"
	pe.party = "Massachusetts Department of Revenue"
	pe.paid_amount = tax_amount
	pe.received_amount = tax_amount
	pe.base_paid_amount = tax_amount
	pe.base_received_amount = tax_amount
	pe.base_grand_total = tax_amount
	pe.append(
		"references",
		{
			"reference_doctype": "Sales Taxes and Charges",
			"reference_name": tax_row_name,
			"due_date": ma_tax_row.due_date,
			"total_amount": tax_amount,
			"outstanding_amount": tax_amount,
			"allocated_amount": tax_amount,
		},
	)
	pe.save()
	frappe.clear_messages()
	pe.submit()
	assert not any("No outstanding" in str(m) for m in frappe.get_message_log()), (
		"validate_allocated_amount_with_latest_data should not emit a 'No outstanding' message "
		f"for a Sales Taxes and Charges-only Payment Entry: {frappe.get_message_log()}"
	)

	outstanding_after_payment = flt(
		frappe.db.get_value("Sales Taxes and Charges", tax_row_name, "outstanding_amount")
	)
	assert outstanding_after_payment == 0.0, "Outstanding should be 0 after payment"

	return_si = make_return_doc("Sales Invoice", si.name)
	return_si.posting_date = frappe.utils.add_days(si.posting_date, 1)
	return_si.save()
	return_si.submit()

	return_ma_tax_row = next(
		(row for row in return_si.taxes if row.party == "Massachusetts Department of Revenue"),
		None,
	)
	assert return_ma_tax_row, "Return SI should have a Massachusetts Department of Revenue tax row"
	return_outstanding = flt(
		frappe.db.get_value("Sales Taxes and Charges", return_ma_tax_row.name, "outstanding_amount")
	)
	assert (
		return_outstanding < 0.0
	), f"Return SI tax row outstanding should be negative, got {return_outstanding}"
	assert flt(abs(return_outstanding), 2) == flt(tax_amount, 2), (
		f"Return outstanding magnitude {abs(return_outstanding)} should equal "
		f"original tax amount {tax_amount}"
	)

	original_outstanding_unchanged = flt(
		frappe.db.get_value("Sales Taxes and Charges", tax_row_name, "outstanding_amount")
	)
	assert (
		original_outstanding_unchanged == 0.0
	), "Original outstanding should remain 0 after the return (it was already paid)"


@pytest.mark.order(45)
def test_reversed_payable_in_check_run():
	"""
	Verify that a return SI's negative outstanding tax row (created by
	test_return_after_payable_remitted) surfaces in get_entries for the
	Sales Tax Payable Check Run, allowing the credit to be reconciled.

	The outstanding_amount != 0 filter in the st_qb query must include
	negative values so that returns-after-payment appear for review.
	"""
	cr_name = check_for_draft_check_run(
		company="Chelsea Fruit Co",
		bank_account="Primary Checking - Local Bank",
		payable_account="2320 - Sales Tax Payable - CFC",
	)
	cr = frappe.get_doc("Check Run", cr_name)
	cr.flags.in_test = True
	cr.posting_date = cr.end_date = datetime.date(year, 12, 31)
	cr.set_last_check_number()
	cr.save()
	crs = get_check_run_settings(cr)
	crs.include_tax_payable = 1
	crs.allow_stand_alone_debit_notes = "Yes"
	crs.number_of_invoices_per_voucher = 100
	crs.save()

	entries = get_entries(cr)
	transactions = entries.get("transactions")

	negative_transactions = [t for t in transactions if flt(t.get("amount", 0)) < 0.0]
	assert (
		negative_transactions
	), "Expected at least one negative tax payable entry from the return SI created in test 50"
	for t in negative_transactions:
		assert t.get("doctype") == "Sales Invoice"
		assert t.get("party") == "Massachusetts Department of Revenue"


@pytest.mark.order(46)
def test_multiple_tax_authorities_single_invoice():
	"""
	Verify that an SI with tax rows pointing to two different tax authorities
	produces separate GL entries for each and appears as two independent rows
	in the Check Run.

	| Account                 |   Debit  |  Credit  | Party                               |
	| ----------------------- | --------:| --------:| ----------------------------------- |
	| Accounts Receivable     | $150.75  |          | Beans and Dreams Roasters           |
	| Sales                   |          | $130.00  |                                     |
	| 2320 Sales Tax Payable  |          |   $8.13  | Massachusetts Department of Revenue |
	| 2320 Sales Tax Payable  |          |   $7.80  | Vermont Department of Taxes         |

	Two GL entries against the same account but different parties; two separate
	rows in the Check Run allowing independent payment to each authority.
	"""
	si = frappe.new_doc("Sales Invoice")
	si.customer = "Beans and Dreams Roasters"
	si.set_posting_time = 1
	si.company = "Chelsea Fruit Co"
	si.posting_date = getdate().replace(month=8, day=1)
	si.append("items", {"item_code": "Cloudberry", "qty": 100, "rate": 1.30})

	for template_name in ("MA Sales Tax - CFC", "VT Sales Tax - CFC"):
		taxes = frappe.call(
			"erpnext.controllers.accounts_controller.get_taxes_and_charges",
			master_doctype="Sales Taxes and Charges Template",
			master_name=template_name,
		)
		for tax in taxes:
			si.append("taxes", tax)

	si.save()
	si.submit()

	gl_entries = frappe.get_all(
		"GL Entry",
		{"voucher_no": si.name, "account": "2320 - Sales Tax Payable - CFC", "is_cancelled": 0},
		["name", "credit", "party"],
	)
	assert (
		len(gl_entries) == 2
	), f"Expected 2 GL entries for tax payable (one per authority), got {len(gl_entries)}"
	parties = {g.party for g in gl_entries}
	assert "Massachusetts Department of Revenue" in parties
	assert "Vermont Department of Taxes" in parties

	cr_name = check_for_draft_check_run(
		company="Chelsea Fruit Co",
		bank_account="Primary Checking - Local Bank",
		payable_account="2320 - Sales Tax Payable - CFC",
	)
	cr = frappe.get_doc("Check Run", cr_name)
	cr.flags.in_test = True
	cr.posting_date = cr.end_date = datetime.date(year, 12, 31)
	cr.set_last_check_number()
	cr.save()
	crs = get_check_run_settings(cr)
	crs.include_tax_payable = 1
	crs.number_of_invoices_per_voucher = 100
	crs.save()

	entries = get_entries(cr)
	transactions = entries.get("transactions")

	ma_entries = [t for t in transactions if t.get("party") == "Massachusetts Department of Revenue"]
	vt_entries = [t for t in transactions if t.get("party") == "Vermont Department of Taxes"]
	assert ma_entries, "Massachusetts Department of Revenue should appear in Check Run entries"
	assert vt_entries, "Vermont Department of Taxes should appear in Check Run entries"

	this_si_ma = [t for t in ma_entries if t.get("ref_number") == si.name]
	this_si_vt = [t for t in vt_entries if t.get("ref_number") == si.name]
	assert (
		this_si_ma
	), f"SI {si.name} should appear in Check Run for Massachusetts Department of Revenue"
	assert this_si_vt, f"SI {si.name} should appear in Check Run for Vermont Department of Taxes"


@pytest.mark.order(47)
def test_accounting_dimensions_in_tax_gl_entries():
	"""
	Verify that the cost_center from the Sales Taxes and Charges row flows
	through to the GL Entry created for the tax payable account. Also verifies
	that any custom accounting dimensions defined in the system are passed
	through from the tax row to the GL entry.

	| Account                |   Debit  |  Credit  | Cost Center | Party                               |
	| ---------------------- | --------:| --------:| ----------- | ----------------------------------- |
	| 2320 Sales Tax Payable |          |   $0.81  | Main - CFC  | Massachusetts Department of Revenue |
	"""
	from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import (
		get_accounting_dimensions,
	)

	si = frappe.new_doc("Sales Invoice")
	si.customer = "Capital Grille Restaurant Group"
	si.set_posting_time = 1
	si.company = "Chelsea Fruit Co"
	si.posting_date = getdate().replace(month=9, day=1)
	si.append("items", {"item_code": "Cloudberry", "qty": 10, "rate": 1.30})
	si.taxes_and_charges = "MA Sales Tax - CFC"
	taxes = frappe.call(
		"erpnext.controllers.accounts_controller.get_taxes_and_charges",
		master_doctype="Sales Taxes and Charges Template",
		master_name="MA Sales Tax - CFC",
	)
	for tax in taxes:
		si.append("taxes", tax)
	si.save()
	si.submit()

	tax_row = next(row for row in si.taxes if row.party == "Massachusetts Department of Revenue")
	gl_entry = frappe.get_doc(
		"GL Entry",
		{
			"voucher_no": si.name,
			"account": "2320 - Sales Tax Payable - CFC",
			"is_cancelled": 0,
		},
	)
	assert gl_entry.cost_center == tax_row.cost_center, (
		f"GL Entry cost_center '{gl_entry.cost_center}' should match "
		f"tax row cost_center '{tax_row.cost_center}'"
	)
	assert gl_entry.cost_center, "cost_center should not be empty on tax GL entry"

	for dimension in get_accounting_dimensions():
		expected = tax_row.get(dimension)
		actual = gl_entry.get(dimension)
		assert actual == expected, (
			f"Accounting dimension '{dimension}': GL Entry has '{actual}', " f"tax row has '{expected}'"
		)
