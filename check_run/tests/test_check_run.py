import json
import datetime
import pytest

import frappe

from check_run.check_run.doctype.check_run.check_run import get_check_run_settings, get_entries

year = datetime.date.today().year


@pytest.fixture
def cr():  # return draft check run
	cr = frappe.new_doc("Check Run")
	cr.company = "Chelsea Fruit Co"
	cr.bank_account = "Primary Checking - Local Bank"
	cr.pay_to_account = "2110 - Accounts Payable - CFC"
	cr.posting_date = cr.end_date = datetime.date(year, 12, 31)
	cr.set_last_check_number()
	cr.set_default_payable_account()
	entries = get_entries(cr)
	# manipulate entries / selections
	cr.save()
	cr.entries = frappe.as_json(entries.get("transactions"))
	return cr


def test_get_entries(cr):
	crs = get_check_run_settings(cr)
	assert frappe.db.exists("Check Run Settings", crs)
	cr.entries = frappe.utils.safe_json_loads(cr.entries)
	assert len(cr.entries) > 1
	# assert that each type of source document appears at least once
	assert any([doc.get("doctype") == "Purchase Invoice" for doc in cr.entries])
	assert any([doc.get("doctype") == "Journal Entry" for doc in cr.entries])
	assert any([doc.get("doctype") == "Expense Claim" for doc in cr.entries])
	# assert that the invoice with installment payment schedule appears more than once
	assert len([doc.get("name") == f"ACC-PINV-{year}-00001 " for doc in cr.entries]) > 1
