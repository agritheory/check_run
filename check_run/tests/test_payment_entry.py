import datetime

import frappe
import pytest
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry

from check_run.check_run.doctype.check_run.check_run import (
	check_for_draft_check_run,
	get_check_run_settings,
	get_entries,
)
from check_run.tests.test_check_run import cr

year = datetime.date.today().year


def test_partial_payment_payment_entry_with_terms():
	pi_name = frappe.get_all(
		"Purchase Invoice",
		{"supplier": "Exceptional Grid"},
		pluck="name",
		order_by="posting_date ASC",
		limit=1,
	)[0]
	pe0 = get_payment_entry("Purchase Invoice", pi_name)
	pe0.mode_of_payment = "Check"
	pe0.paid_amount = 30.00
	pe0.bank_account = "Primary Checking - Local Bank"
	pe0.reference_no = frappe.get_value("Bank Account", pe0.bank_account, "check_number")
	pe0.references[0].allocated_amount = 30.00
	pe0.save()
	pe0.submit()

	pi = frappe.get_doc("Purchase Invoice", pi_name)
	assert pi.payment_schedule[0].outstanding == 120.00
	assert pi.outstanding_amount == 120.00

	pe1 = get_payment_entry("Purchase Invoice", pi_name)
	pe1.mode_of_payment = "Check"
	pe1.paid_amount = 120.00
	pe1.bank_account = "Primary Checking - Local Bank"
	pe1.reference_no = frappe.get_value("Bank Account", pe1.bank_account, "check_number")
	pe1.references[0].allocated_amount = 120.00
	pe1.save()
	pe1.submit()

	pi = frappe.get_doc("Purchase Invoice", pi_name)
	assert pi.payment_schedule[0].outstanding == 0.00
	assert pi.outstanding_amount == 0.0


def test_payment_payment_entry_of_multiple_terms():
	pi_name = frappe.get_all(
		"Purchase Invoice",
		{"supplier": "Tireless Equipment Rental, Inc"},
		pluck="name",
		order_by="posting_date ASC",
		limit=1,
	)[0]
	pe0 = get_payment_entry("Purchase Invoice", pi_name)
	pe0.mode_of_payment = "Check"
	pe0.paid_amount = 4500.00
	pe0.bank_account = "Primary Checking - Local Bank"
	pe0.reference_no = frappe.get_value("Bank Account", pe0.bank_account, "check_number")
	pe0.references[0].allocated_amount = 4500
	pe0.save()
	pe0.submit()

	pi = frappe.get_doc("Purchase Invoice", pi_name)
	assert pi.payment_schedule[0].outstanding == 0.0
	assert pi.payment_schedule[1].outstanding == 0.0
	assert pi.payment_schedule[2].outstanding == 500.01

	pe0.cancel()
	pi.reload()
	assert pi.payment_schedule[2].outstanding == 1666.67
	assert pi.payment_schedule[1].outstanding == 1666.67
	assert pi.payment_schedule[0].outstanding == 1666.67


def test_partial_payment_payment_entry_without_terms():
	pi_name = frappe.get_all(
		"Purchase Invoice",
		{"supplier": "Sphere Cellular"},
		pluck="name",
		order_by="posting_date ASC",
		limit=1,
	)[0]
	pi = frappe.get_doc("Purchase Invoice", pi_name)
	assert pi.payment_schedule[0].outstanding == 250.00
	assert pi.outstanding_amount == 250.00

	pe0 = get_payment_entry("Purchase Invoice", pi_name)
	pe0.mode_of_payment = "Check"
	pe0.paid_amount = 100.00
	pe0.bank_account = "Primary Checking - Local Bank"
	pe0.reference_no = frappe.get_value("Bank Account", pe0.bank_account, "check_number")
	pe0.references[0].allocated_amount = 100.00
	pe0.save()
	pe0.submit()

	pi.reload()
	assert pi.payment_schedule[0].outstanding == 150.00
	assert pi.outstanding_amount == 150

	pe1 = get_payment_entry("Purchase Invoice", pi_name)
	pe1.mode_of_payment = "Check"
	pe1.paid_amount = 100.00
	pe1.bank_account = "Primary Checking - Local Bank"
	pe1.reference_no = frappe.get_value("Bank Account", pe1.bank_account, "check_number")
	pe1.references[0].allocated_amount = 100.00
	pe1.save()
	pe1.submit()

	pi = frappe.get_doc("Purchase Invoice", pi_name)
	assert pi.payment_schedule[0].outstanding == 50.00
	assert pi.outstanding_amount == 50.00

	pe2 = get_payment_entry("Purchase Invoice", pi_name)
	pe2.mode_of_payment = "Check"
	pe2.paid_amount = 100.00
	pe2.bank_account = "Primary Checking - Local Bank"
	pe2.reference_no = frappe.get_value("Bank Account", pe2.bank_account, "check_number")
	pe2.references[0].allocated_amount = 100.00

	pi = frappe.get_doc("Purchase Invoice", pi_name)
	with pytest.raises(
		frappe.exceptions.ValidationError,
		# match='Allocated Amount of 100.0 cannot be greater than outstanding amount of 50.0',
	):
		pe2.save()

	pe2.paid_amount = 50.00
	pe2.references[0].allocated_amount = 50.00
	pe2.save()
	pe2.submit()

	pi.reload()
	assert pi.payment_schedule[0].outstanding == 00.00
	assert pi.outstanding_amount == 0.00


def test_outstanding_amount_in_check_run(cr):
	pi_name = frappe.get_all(
		"Purchase Invoice",
		{"supplier": "Mare Digitalis"},
		pluck="name",
		order_by="posting_date ASC",
		limit=1,
	)[0]
	pi = frappe.get_doc("Purchase Invoice", pi_name)
	assert pi.outstanding_amount == 200.00
	assert pi.payment_schedule[0].outstanding == 200.00

	pe0 = get_payment_entry("Purchase Invoice", pi_name)
	pe0.mode_of_payment = "Check"
	pe0.paid_amount = 110.00
	pe0.bank_account = "Primary Checking - Local Bank"
	pe0.reference_no = frappe.get_value("Bank Account", pe0.bank_account, "check_number")
	pe0.references[0].allocated_amount = 110.00
	pe0.save()
	pe0.submit()
	pi.reload()
	assert pi.payment_schedule[0].outstanding == 90.00
	assert pi.outstanding_amount == 90.00

	cr.transactions = None
	cr.save()
	entries = get_entries(cr)
	for row in entries.get("transactions"):
		row["pay"] = False
	transactions = frappe.utils.safe_json_loads(entries.get("transactions"))

	t = list(filter(lambda x: x.get("name") == f"ACC-PINV-{year}-00004", transactions))
	assert t[0].get("amount") == 90.00

	pe0.cancel()
	pi.reload()
	assert pi.payment_schedule[0].outstanding == 200.00
	assert pi.outstanding_amount == 200.00

	cr.transactions = None
	cr.save()
	entries = get_entries(cr)
	for row in entries.get("transactions"):
		row["pay"] = False
	transactions = frappe.utils.safe_json_loads(entries.get("transactions"))

	t = list(filter(lambda x: x.get("name") == f"ACC-PINV-{year}-00004", transactions))
	assert t[0].get("amount") == 200.00
