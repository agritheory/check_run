# Copyright (c) 2023, AgriTheory and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import get_link_to_form
from erpnext.accounts.doctype.payment_entry.payment_entry import PaymentEntry


@frappe.whitelist()
def update_check_number(doc: PaymentEntry, method: str | None = None) -> None:
	mode_of_payment_type = frappe.db.get_value("Mode of Payment", doc.mode_of_payment, "type")
	if doc.bank_account and mode_of_payment_type == "Bank" and str(doc.reference_no).isdigit():
		frappe.db.set_value("Bank Account", doc.bank_account, "check_number", doc.reference_no)


@frappe.whitelist()
def validate_outstanding_payment_terms(doc: PaymentEntry, method: str | None = None) -> None:
	references = doc.get("references")
	errors = []
	for r in references:
		if r.reference_doctype != "Purchase Invoice":
			continue
		pmt_terms = frappe.get_all(
			"Payment Schedule", {"parent": r.reference_name, "outstanding": ["!=", 0.0]}
		)
		if pmt_terms and not r.payment_term:
			errors.append((r.idx, r.reference_name))

	if errors:
		list_items = "</li><li>".join([f"Row {row}: {inv}" for row, inv in errors])
		message = frappe._(
			f"There is at least one outstanding Payment Schedule Payment Term for the following Purchase Invoices in the Payment References table:<br><br><ul><li>{list_items}</li></ul><br>Please update the Payment Term field to tie this Payment Entry to the invoice's Payment Schedule and prevent paid invoice portions from showing up in a Check Run."
		)
		frappe.throw(
			msg=message,
			title="Missing Field",
		)


@frappe.whitelist()
def validate_duplicate_check_number(doc: PaymentEntry, method: str | None = None) -> None:
	check_run_settings = frappe.db.exists("Check Run Settings", {"bank_account": doc.bank_account, "pay_to_account": doc.paid_to})
	if not check_run_settings or not frappe.db.get_value("Check Run Settings", check_run_settings, "validate_unique_check_number"):
		return

	mode_of_payment_type = frappe.db.get_value("Mode of Payment", doc.mode_of_payment, "type")
	if mode_of_payment_type != "Bank" or not str(doc.reference_no).isdigit():
		return
		
	pe_names = frappe.get_all("Payment Entry", {"payment_type": "Pay", "name": ["!=", doc.name], "docstatus": ["!=", 2], "reference_no": doc.reference_no})
	if not pe_names:
		return
	
	error_message = "</li><li>".join([get_link_to_form('Payment Entry', p.name) for p in pe_names])
	frappe.throw(
		msg=frappe._(
			f"Check Number {doc.reference_no} is already set in:<br><br><ul><li>{error_message}</li></ul>"
		),
		title="Check Number already exists",
	)
	