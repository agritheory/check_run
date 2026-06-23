# Copyright (c) 2025, AgriTheory and contributors
# For license information, please see license.txt

import datetime

import frappe
import pytest
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry
from frappe.exceptions import ValidationError
from frappe.model.workflow import apply_workflow
from frappe.utils import add_days, getdate

from check_run.check_run.doctype.check_run.check_run import get_entries
from check_run.overrides.payment_entry import set_voided_date
from check_run.tests.test_check_run import cr  # noqa

year = datetime.date.today().year


@pytest.mark.order(30)
def test_partial_payment_payment_entry_with_terms():
	pi_name = frappe.get_value(
		"Purchase Invoice",
		{"supplier": "Exceptional Grid", "grand_total": 150, "posting_date": datetime.date(year, 1, 1)},
	)
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


@pytest.mark.order(31)
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


@pytest.mark.order(32)
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


@pytest.mark.order(33)
def test_outstanding_amount_in_check_run(cr):
	pi_name = frappe.get_value(
		"Purchase Invoice",
		{"supplier": "Mare Digitalis", "grand_total": 200, "posting_date": datetime.date(year, 1, 1)},
	)
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


@pytest.mark.order(34)
def test_voided_payment_entry(cr):
	"""
	For illustrative purposes, the dates used for the following T-accounts assume
	- current date is Jan-02
	- original PI created on Nov-01 (prior year) with Net 30 terms, due Dec-01
	- check payment sent and Payment Entry posting date set to Dec-01 (prior year)
	- current date is Jan-02, but learned about lost check two days prior on Dec-31

	Purchase Invoice:
	| Date | Account | Party | Debit | Credit |
	| :---- | :--------| :----: | -----: | ------: |
	| Nov-01 | Accounts Payable | Cooperative Ag Finance | | $5,000 |
	| Nov-01 | Inventory Received But Not Billed |  | $5,000 |  |

	Payment Entry:
	| Date | Account | Party | Debit | Credit |
	| :---- | :--------| :----: | -----: | ------: |
	| Dec-01 | Accounts Payable | Cooperative Ag Finance | $5,000 |  |
	| Dec-01 | Primary Checking |  |  | $5,000 |

	Payment Entry Voided as of Dec-31:
	| Date | Account | Party | Debit | Credit |
	| :---- | :--------| :----: | -----: | ------: |
	| Dec-31 | Accounts Payable | Cooperative Ag Finance |  | $5,000 |
	| Dec-31 | Primary Checking |  | $5,000 |  |
	"""
	# Activate Voidable Payment Entry workflow
	vpe = frappe.get_doc("Workflow", "Voidable Payment Entry")
	vpe.is_active = 1
	vpe.save()

	invoice_date = add_days(getdate(), -60)
	payment_posting_date = add_days(getdate(), -30)
	lost_check_date = add_days(getdate(), -2)

	# Create a 2-month-old Purchase Invoice
	pi = frappe.new_doc("Purchase Invoice")
	pi.supplier = "Cooperative Ag Finance"
	pi.company = frappe.defaults.get_defaults().company
	pi.set_posting_time = 1
	pi.posting_date = invoice_date
	pi.append(
		"items",
		{
			"item_code": "Financial Services",
			"rate": 5000.00,
			"qty": 1,
		},
	)
	pi.payment_terms = "Net 30"
	pi.save()
	pi.submit()

	# Create a Payment Entry 1 month ago using Check
	company = frappe.defaults.get_defaults().company
	bank_account = "Primary Checking - Local Bank"
	gl_account = frappe.get_value("Bank Account", bank_account, "account")
	gl_account_currency = frappe.db.get_value("Account", gl_account, "account_currency")
	last_check_no = frappe.get_value("Bank Account", bank_account, "check_number")
	total_amount = pi.outstanding_amount

	pe = frappe.new_doc("Payment Entry")
	pe.payment_type = "Pay"
	pe.posting_date = payment_posting_date
	pe.mode_of_payment = "Check"
	pe.company = company
	pe.bank_account = bank_account
	pe.paid_from = gl_account
	pe.paid_to = frappe.get_value("Account", {"name": ["like", "%Accounts Payable%"]})
	pe.paid_to_account_currency = gl_account_currency
	pe.paid_from_account_currency = pe.paid_to_account_currency
	pe.party_type = "Supplier"
	pe.party = pi.supplier
	pe.reference_no = int(last_check_no) + 1
	pe.reference_date = pe.posting_date
	pe.append(
		"references",
		{
			"reference_doctype": pi.doctype,
			"reference_name": pi.name,
			"due_date": pi.get("due_date"),
			"outstanding_amount": total_amount,
			"allocated_amount": total_amount,
			"total_amount": total_amount,
			"payment_term": frappe.get_value("Payment Schedule", {"parent": pi.name}, "payment_term"),
		},
	)
	pe.received_amount = total_amount
	pe.base_received_amount = total_amount
	pe.paid_amount = total_amount
	pe.base_paid_amount = total_amount
	pe.base_grand_total = total_amount
	pe.save()
	pe.submit()

	pi.reload()
	assert pi.outstanding_amount == 0

	# Check initial GL Entries
	gl_count = len(
		frappe.get_all("GL Entry", {"voucher_type": "Payment Entry", "voucher_no": pe.name})
	)
	assert gl_count == 2

	payable_acct = frappe.get_value(
		"Account", {"account_type": "Payable", "name": ["like", "%Accounts Payable%"]}
	)
	checking_acct = frappe.get_value(
		"Account", {"account_type": "Bank", "name": ["like", "%Primary Checking%"]}
	)

	gl_1 = frappe.get_doc(
		"GL Entry", {"voucher_no": pe.name, "account": payable_acct, "party": pi.supplier}
	)
	assert gl_1.against_voucher == pi.name
	assert gl_1.debit == total_amount
	assert gl_1.credit == 0
	assert gl_1.is_cancelled == 0
	assert gl_1.posting_date == payment_posting_date

	gl_2 = frappe.get_doc(
		"GL Entry", {"voucher_no": pe.name, "account": checking_acct, "against": pi.supplier}
	)
	assert gl_2.debit == 0
	assert gl_2.credit == total_amount
	assert gl_2.is_cancelled == 0
	assert gl_2.posting_date == payment_posting_date

	# Learned check lost in mail (two days ago), apply Voidable Payment Entry workflow
	# Note: set_voided_date would normally be called from the dialog in UI

	# Raise error if void date is before Payment Entry posting date
	invalid_void_date = add_days(pe.posting_date, -5)
	with pytest.raises(ValidationError) as exc_info:
		set_voided_date(pe.doctype, pe.name, str(invalid_void_date))

	assert (
		"Void As Of Date cannot be before the Payment Entry's posting date." in exc_info.value.args[0]
	)

	# Use appropriate void date
	set_voided_date(pe.doctype, pe.name, str(lost_check_date))
	apply_workflow(pe, "Void")
	pe.reload()
	assert pe.status == "Voided"
	assert pe.voided_date == lost_check_date
	pi.reload()
	assert pi.outstanding_amount == total_amount

	# Check voided GL Entries
	gl_count = len(
		frappe.get_all("GL Entry", {"voucher_type": "Payment Entry", "voucher_no": pe.name})
	)
	assert gl_count == 4

	gl_1.reload()
	assert gl_1.is_cancelled == 1
	gl_2.reload()
	assert gl_2.is_cancelled == 1

	gl_3 = frappe.get_doc(
		"GL Entry",
		{"voucher_no": pe.name, "account": payable_acct, "party": pi.supplier, "credit": [">", 0]},
	)
	assert gl_3.against_voucher == pi.name
	assert gl_3.debit == 0
	assert gl_3.credit == total_amount
	assert gl_3.is_cancelled == 1
	assert gl_3.posting_date == lost_check_date

	gl_4 = frappe.get_doc(
		"GL Entry",
		{"voucher_no": pe.name, "account": checking_acct, "against": pi.supplier, "debit": [">", 0]},
	)
	assert gl_4.debit == total_amount
	assert gl_4.credit == 0
	assert gl_4.is_cancelled == 1
	assert gl_4.posting_date == lost_check_date
