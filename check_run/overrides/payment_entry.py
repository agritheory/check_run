# Copyright (c) 2023, AgriTheory and contributors
# For license information, please see license.txt

import frappe
from erpnext.accounts.doctype.payment_entry.payment_entry import PaymentEntry


@frappe.whitelist()
def update_check_number(doc: PaymentEntry, method: str | None = None):
	mode_of_payment_type = frappe.db.get_value("Mode of Payment", doc.mode_of_payment, "type")
	if doc.bank_account and mode_of_payment_type == "Bank" and str(doc.reference_no).isdigit():
		frappe.db.set_value("Bank Account", doc.bank_account, "check_number", doc.reference_no)
