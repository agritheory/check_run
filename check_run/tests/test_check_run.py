import json

import pytest

import frappe

from check_run.check_run.doctype.check_run.check_run import get_check_run_settings, get_entries


def test_setup():
	cr = frappe.new_doc("Check Run")
	cr.company = "Chelsea Fruit Co"
	cr.bank_account = "Primary Checking - Local Bank"
	cr.pay_to_account = "2110 - Accounts Payable - CFC"
	cr.set_last_check_number()
	cr.set_default_payable_account()
	cr.set_default_dates()
	entries = get_entries(cr)
	# manipulate entries / selections
	cr.save()
	cr.entries = frappe.as_json(entries.get("transactions"))
	crs = get_check_run_settings(cr)
	assert frappe.db.exists("Check Run Settings", crs)

	print(len(frappe.utils.safe_json_loads(cr.entries)))
	assert len(frappe.utils.safe_json_loads(cr.entries)) > 1
	# invoice, expense claim and journal entry present
	#
