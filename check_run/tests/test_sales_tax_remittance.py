# Copyright (c) 2026, AgriTheory and contributors
# For license information, please see license.txt

import datetime

import frappe
import pytest
from erpnext.controllers.sales_and_purchase_return import make_return_doc
from frappe.utils import add_days, flt

from check_run.check_run.report.sales_tax_remittance.sales_tax_remittance import execute

year = datetime.date.today().year


def make_taxed_si(customer, template_name, posting_date, qty=100, rate=1.30):
	si = frappe.new_doc("Sales Invoice")
	si.customer = customer
	si.set_posting_time = 1
	si.company = "Chelsea Fruit Co"
	si.posting_date = posting_date
	si.append("items", {"item_code": "Cloudberry", "qty": qty, "rate": rate})
	si.taxes_and_charges = template_name
	taxes = frappe.call(
		"erpnext.controllers.accounts_controller.get_taxes_and_charges",
		master_doctype="Sales Taxes and Charges Template",
		master_name=template_name,
	)
	for tax in taxes:
		si.append("taxes", tax)
	si.save()
	si.submit()
	return si


@pytest.mark.order(75)
def test_remittance_report_summary_unremitted():
	"""
	Two freshly-submitted VT invoices appear in the summary report as fully
	outstanding: nothing has been remitted and no customer has paid.

	| Account                |   Debit  |  Credit  | Party                       |
	| ---------------------- | --------:| --------:| --------------------------- |
	| Accounts Receivable    | $137.80  |          | Almacs Food Group           |
	| Sales                  |          | $130.00  |                             |
	| 2320 Sales Tax Payable |          |   $7.80  | Vermont Department of Taxes |

	(Same GL structure for Beans and Dreams Roasters)
	"""
	posting_date = datetime.date(year, 11, 1)
	for customer in ("Almacs Food Group", "Beans and Dreams Roasters"):
		make_taxed_si(customer, "VT Sales Tax - CFC", posting_date)

	data = execute(
		{
			"company": "Chelsea Fruit Co",
			"to_date": datetime.date(year, 12, 31),
			"tax_authority": "Vermont Department of Taxes",
		}
	)[1]

	# Test 60 created a VT SI in August — filter to the November bucket we own
	nov = f"{year}-11"
	nov_rows = [r for r in data if r.get("period") == nov]
	assert len(nov_rows) == 1, f"Expected 1 summary row for {nov}, got {len(nov_rows)}: {nov_rows}"
	row = nov_rows[0]
	assert flt(row["total_collected"], 2) == 15.60
	assert flt(row["total_outstanding"], 2) == 15.60
	assert flt(row["total_remitted"], 2) == 0.00
	assert flt(row["customer_paid_amount"], 2) == 0.00


@pytest.mark.order(76)
def test_remittance_report_customer_paid_flag():
	"""
	When a customer pays their invoice the detail report's "Customer Paid"
	column becomes 1 for that row, but the outstanding tax to the authority
	is unchanged — the two obligations are independent.
	"""
	posting_date = datetime.date(year, 11, 15)
	si = make_taxed_si("Cafe 27 Cafeteria", "VT Sales Tax - CFC", posting_date)

	ar_account = frappe.get_value(
		"Account",
		{"account_type": "Receivable", "company": "Chelsea Fruit Co", "is_group": 0},
	)
	bank_account = frappe.get_value(
		"Account",
		{"account_type": "Bank", "company": "Chelsea Fruit Co", "is_group": 0},
	)
	currency = frappe.db.get_value("Account", ar_account, "account_currency")
	pe = frappe.new_doc("Payment Entry")
	pe.payment_type = "Receive"
	pe.posting_date = add_days(posting_date, 10)
	pe.mode_of_payment = "Check"
	pe.company = "Chelsea Fruit Co"
	pe.bank_account = "Primary Checking - Local Bank"
	pe.party_type = "Customer"
	pe.party = "Cafe 27 Cafeteria"
	pe.paid_from = ar_account
	pe.paid_to = bank_account
	pe.paid_from_account_currency = currency
	pe.paid_to_account_currency = currency
	pe.reference_no = "Test-VT-Customer-Pay-76"
	pe.reference_date = pe.posting_date
	pe.paid_amount = flt(si.outstanding_amount)
	pe.received_amount = flt(si.outstanding_amount)
	pe.base_paid_amount = flt(si.outstanding_amount)
	pe.base_received_amount = flt(si.outstanding_amount)
	pe.append(
		"references",
		{
			"reference_doctype": "Sales Invoice",
			"reference_name": si.name,
			"due_date": si.due_date,
			"total_amount": flt(si.grand_total),
			"outstanding_amount": flt(si.outstanding_amount),
			"allocated_amount": flt(si.outstanding_amount),
		},
	)
	pe.save()
	pe.submit()

	detail = execute(
		{
			"company": "Chelsea Fruit Co",
			"to_date": datetime.date(year, 12, 31),
			"tax_authority": "Vermont Department of Taxes",
			"show_detail": 1,
		}
	)[1]

	# Restrict to the November rows we own (test 60 has an August VT row)
	nov_detail = [r for r in detail if r.get("posting_date") and r["posting_date"].month == 11]
	assert len(nov_detail) == 3, f"Expected 3 November VT rows, got {len(nov_detail)}"

	cafe27_row = next(r for r in nov_detail if r["customer"] == "Cafe 27 Cafeteria")
	assert cafe27_row["customer_paid"] == 1, "Cafe 27 customer has paid; flag should be 1"

	for row in nov_detail:
		if row["customer"] != "Cafe 27 Cafeteria":
			assert row["customer_paid"] == 0, f"{row['customer']} has not paid; customer_paid should be 0"
		assert flt(row["outstanding_amount"]) > 0, (
			f"Tax outstanding to VT authority should remain > 0 regardless of customer payment, "
			f"got {row['outstanding_amount']} for {row['customer']}"
		)

	summary = execute(
		{
			"company": "Chelsea Fruit Co",
			"to_date": datetime.date(year, 12, 31),
			"tax_authority": "Vermont Department of Taxes",
		}
	)[1]
	nov = f"{year}-11"
	nov_row = next(r for r in summary if r.get("period") == nov)
	assert (
		flt(nov_row["customer_paid_amount"], 2) == 7.80
	), "Only the Cafe 27 invoice's tax should count as customer-paid"
	assert (
		flt(nov_row["total_outstanding"], 2) == 23.40
	), "All 3 November VT invoices remain unremitted to the tax authority"


@pytest.mark.order(77)
def test_remittance_report_shows_remittance_details():
	"""
	After remitting a RI tax liability via Payment Entry, the detail report
	shows outstanding = 0, the correct remitted amount, and a link back to
	the Payment Entry voucher.

	Remittance Payment Entry GL:
	| Account                |   Debit  |  Credit  | Party                              |
	| ---------------------- | --------:| --------:| ---------------------------------- |
	| 2320 Sales Tax Payable |   $9.10  |          | Rhode Island Division of Taxation  |
	| Primary Checking       |          |   $9.10  |                                    |
	"""
	posting_date = datetime.date(year, 10, 1)
	si = make_taxed_si("Capital Grille Restaurant Group", "RI Sales Tax - CFC", posting_date)

	ri_tax_row = next(r for r in si.taxes if r.party == "Rhode Island Division of Taxation")
	tax_amount = flt(ri_tax_row.tax_amount)

	bank_account = frappe.get_value(
		"Account",
		{"account_type": "Bank", "company": "Chelsea Fruit Co", "is_group": 0},
	)
	currency = frappe.db.get_value("Account", bank_account, "account_currency")
	pe = frappe.new_doc("Payment Entry")
	pe.payment_type = "Pay"
	pe.posting_date = add_days(posting_date, 30)
	pe.mode_of_payment = "Check"
	pe.company = "Chelsea Fruit Co"
	pe.bank_account = "Primary Checking - Local Bank"
	pe.paid_from = bank_account
	pe.paid_to = "2320 - Sales Tax Payable - CFC"
	pe.paid_from_account_currency = currency
	pe.paid_to_account_currency = currency
	pe.reference_no = "Test-RI-Remittance-77"
	pe.reference_date = pe.posting_date
	pe.party_type = "Supplier"
	pe.party = "Rhode Island Division of Taxation"
	pe.paid_amount = tax_amount
	pe.received_amount = tax_amount
	pe.base_paid_amount = tax_amount
	pe.base_received_amount = tax_amount
	pe.append(
		"references",
		{
			"reference_doctype": "Sales Taxes and Charges",
			"reference_name": ri_tax_row.name,
			"due_date": ri_tax_row.due_date,
			"total_amount": tax_amount,
			"outstanding_amount": tax_amount,
			"allocated_amount": tax_amount,
		},
	)
	pe.save()
	pe.submit()

	detail = execute(
		{
			"company": "Chelsea Fruit Co",
			"to_date": datetime.date(year, 12, 31),
			"tax_authority": "Rhode Island Division of Taxation",
			"show_detail": 1,
		}
	)[1]

	assert len(detail) == 1, f"Expected 1 RI row, got {len(detail)}"
	row = detail[0]
	assert flt(row["outstanding_amount"], 2) == 0.00
	assert flt(row["amount_remitted"], 2) == flt(tax_amount, 2)
	assert row["remittance_voucher"] == pe.name
	assert row["remittance_date"] is not None

	remitted = execute(
		{
			"company": "Chelsea Fruit Co",
			"to_date": datetime.date(year, 12, 31),
			"tax_authority": "Rhode Island Division of Taxation",
			"show_detail": 1,
			"remittance_status": "Remitted",
		}
	)[1]
	assert len(remitted) == 1, "Remitted filter should still show the fully-paid RI row"

	outstanding = execute(
		{
			"company": "Chelsea Fruit Co",
			"to_date": datetime.date(year, 12, 31),
			"tax_authority": "Rhode Island Division of Taxation",
			"show_detail": 1,
			"remittance_status": "Outstanding",
		}
	)[1]
	assert len(outstanding) == 0, "Outstanding filter should exclude the fully-remitted RI row"


@pytest.mark.order(78)
def test_remittance_report_return_shows_credit():
	"""
	When a return SI is submitted against an unremitted invoice, the original's
	outstanding is reduced to zero and the return carries a negative outstanding.
	Both rows appear in the detail report; the summary reflects the net position.

	Original SI:
	| Account                |   Debit  |  Credit  | Party                       |
	| ---------------------- | --------:| --------:| --------------------------- |
	| Accounts Receivable    | $137.80  |          | Downtown Deli               |
	| Sales                  |          | $130.00  |                             |
	| 2320 Sales Tax Payable |          |   $7.80  | Vermont Department of Taxes |

	Return SI (reversal):
	| Account                |   Debit  |  Credit  | Party                       |
	| ---------------------- | --------:| --------:| --------------------------- |
	| 2320 Sales Tax Payable |   $7.80  |          | Vermont Department of Taxes |
	| Sales                  | $130.00  |          |                             |
	| Accounts Receivable    |          | $137.80  | Downtown Deli               |
	"""
	posting_date = datetime.date(year, 11, 20)
	si = make_taxed_si("Downtown Deli", "VT Sales Tax - CFC", posting_date)
	vt_tax_row = next(r for r in si.taxes if r.party == "Vermont Department of Taxes")
	tax_amount = flt(vt_tax_row.tax_amount)

	return_si = make_return_doc("Sales Invoice", si.name)
	return_si.posting_date = add_days(posting_date, 1)
	return_si.save()
	return_si.submit()

	detail = execute(
		{
			"company": "Chelsea Fruit Co",
			"to_date": datetime.date(year, 12, 31),
			"tax_authority": "Vermont Department of Taxes",
			"show_detail": 1,
		}
	)[1]

	nov_detail = [r for r in detail if r.get("posting_date") and r["posting_date"].month == 11]

	original_row = next((r for r in nov_detail if r["sales_invoice"] == si.name), None)
	return_row = next((r for r in nov_detail if r["sales_invoice"] == return_si.name), None)
	assert original_row, f"Original SI {si.name} should appear in November VT detail"
	assert return_row, f"Return SI {return_si.name} should appear in November VT detail"

	assert flt(original_row["tax_amount"], 2) == flt(
		tax_amount, 2
	), "Original row tax_amount should be positive"
	assert (
		flt(original_row["outstanding_amount"], 2) == 0.00
	), "Original outstanding should be 0 — reduced to zero by the return"
	assert flt(return_row["tax_amount"], 2) == flt(
		-tax_amount, 2
	), "Return row tax_amount should be negative"
	assert flt(return_row["outstanding_amount"], 2) == flt(
		-tax_amount, 2
	), "Return row outstanding should be negative — credit owed back from authority"

	# November summary: 3 unremitted SIs (tests 75, 76) + original (outstanding=0) + return (outstanding=-7.80)
	summary = execute(
		{
			"company": "Chelsea Fruit Co",
			"to_date": datetime.date(year, 12, 31),
			"tax_authority": "Vermont Department of Taxes",
		}
	)[1]
	nov = f"{year}-11"
	nov_row = next(r for r in summary if r.get("period") == nov)
	# total_collected: Almacs(7.80) + Beans(7.80) + Cafe27(7.80) + Downtown(7.80) + return(-7.80) = 23.40
	assert flt(nov_row["total_collected"], 2) == 23.40
	# total_outstanding: 7.80*3 (unremitted) + 0 (original reduced) + (-7.80) (return) = 15.60
	assert flt(nov_row["total_outstanding"], 2) == 15.60


@pytest.mark.order(79)
def test_remittance_report_status_filter():
	"""
	The remittance_status filter correctly partitions rows:
	- "Outstanding" shows only rows where outstanding > 0
	- "Remitted" shows rows where outstanding <= 0 (fully paid or return credits)
	- default ("All") shows all rows including negative-outstanding return credits
	"""
	nov = f"{year}-11"

	# VT Outstanding: only the 3 unremitted November SIs (Almacs, Beans, Cafe 27)
	# Downtown Deli original (outstanding=0) and return (outstanding<0) are excluded
	outstanding_vt = execute(
		{
			"company": "Chelsea Fruit Co",
			"to_date": datetime.date(year, 12, 31),
			"tax_authority": "Vermont Department of Taxes",
			"show_detail": 1,
			"remittance_status": "Outstanding",
		}
	)[1]
	nov_outstanding = [
		r for r in outstanding_vt if r.get("posting_date") and r["posting_date"].month == 11
	]
	assert (
		len(nov_outstanding) == 3
	), f"Expected 3 outstanding November VT rows, got {len(nov_outstanding)}"
	assert all(flt(r["outstanding_amount"]) > 0 for r in nov_outstanding)
	outstanding_customers = {r["customer"] for r in nov_outstanding}
	assert outstanding_customers == {
		"Almacs Food Group",
		"Beans and Dreams Roasters",
		"Cafe 27 Cafeteria",
	}

	# VT Remitted: Downtown Deli original (outstanding=0) and return (outstanding<0)
	remitted_vt = execute(
		{
			"company": "Chelsea Fruit Co",
			"to_date": datetime.date(year, 12, 31),
			"tax_authority": "Vermont Department of Taxes",
			"show_detail": 1,
			"remittance_status": "Remitted",
		}
	)[1]
	nov_remitted = [r for r in remitted_vt if r.get("posting_date") and r["posting_date"].month == 11]
	assert len(nov_remitted) == 2, (
		f"Expected 2 'remitted' November VT rows (original outstanding=0, return outstanding<0), "
		f"got {len(nov_remitted)}"
	)
	assert all(flt(r["outstanding_amount"]) <= 0 for r in nov_remitted)

	# RI Remitted: Capital Grille (fully remitted in test 77)
	remitted_ri = execute(
		{
			"company": "Chelsea Fruit Co",
			"to_date": datetime.date(year, 12, 31),
			"tax_authority": "Rhode Island Division of Taxation",
			"show_detail": 1,
			"remittance_status": "Remitted",
		}
	)[1]
	assert len(remitted_ri) == 1
	assert remitted_ri[0]["customer"] == "Capital Grille Restaurant Group"

	# VT All: 5 November rows (Almacs, Beans, Cafe27, Downtown original, Downtown return)
	all_vt = execute(
		{
			"company": "Chelsea Fruit Co",
			"to_date": datetime.date(year, 12, 31),
			"tax_authority": "Vermont Department of Taxes",
			"show_detail": 1,
		}
	)[1]
	nov_all = [r for r in all_vt if r.get("posting_date") and r["posting_date"].month == 11]
	assert len(nov_all) == 5, f"Expected 5 November VT rows in All view, got {len(nov_all)}"
	return_rows = [r for r in nov_all if flt(r["tax_amount"]) < 0]
	assert len(return_rows) == 1, "Exactly one return (negative tax_amount) row should be present"
	assert (
		flt(return_rows[0]["outstanding_amount"]) < 0
	), "The return row's outstanding should be negative (credit owed from authority)"
