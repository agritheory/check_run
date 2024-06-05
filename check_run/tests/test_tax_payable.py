import datetime
import json

import frappe
import pytest
from frappe.utils import flt

from check_run.check_run.doctype.check_run.check_run import (
	check_for_draft_check_run,
	get_check_run_settings,
	get_entries,
)

year = datetime.date.today().year


@pytest.fixture
def tax_payable_cr():  # return draft check run
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
	# Need CR Settings in place to call get_entries
	crs = get_check_run_settings(cr)
	crs.include_tax_payable = 1
	crs.number_of_invoices_per_voucher = 100
	crs.save()
	entries = get_entries(cr)
	for row in entries.get("transactions"):
		row["pay"] = True
	cr.transactions = frappe.as_json(entries.get("transactions"))
	cr.save()
	return cr


def test_tax_payable_gl():
	sis = [
		frappe.get_doc("Sales Invoice", si) for si in frappe.get_all("Sales Invoice", pluck="name")
	]
	for doc in sis:
		precision = frappe.get_precision(doc.doctype, "grand_total")
		doc.submit()
		gl1 = frappe.get_doc(
			"GL Entry", {"voucher_no": doc.name, "account": "2320 - Sales Tax Payable - CFC"}
		)
		assert flt(gl1.credit, precision) == doc.total_taxes_and_charges
		assert gl1.party == "Massachusetts Department of Revenue"


def test_tax_payable_check_run(tax_payable_cr):
	cr = tax_payable_cr
	transactions = json.loads(cr.transactions)
	for t in transactions:
		t["pay"] = True
		assert t.get("doctype") == "Sales Invoice"
		assert t.get("party") == "Massachusetts Department of Revenue"
	cr.process_check_run()

	entries = get_entries(cr)
	transactions = entries.get("transactions")
	pe_name = transactions[0].get("payment_entry")
	assert all([pe_name == t.get("payment_entry") for t in transactions])
