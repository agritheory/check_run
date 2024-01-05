# Copyright (c) 2023, AgriTheory and contributors
# For license information, please see license.txt

import frappe
from erpnext.accounts.doctype.payment_entry.payment_entry import PaymentEntry
from erpnext.accounts.general_ledger import make_gl_entries, process_gl_map
from frappe.utils.data import getdate


class CustomPaymentEntry(PaymentEntry):
	def make_gl_entries(self, cancel=0, adv_adj=0):
		if self.payment_type in ("Receive", "Pay") and not self.get("party_account_field"):
			self.setup_party_account_field()

		if self.status == 'Voided':
			original_posting_date = self.posting_date
			self.voided_date = self.posting_date = getdate()

		gl_entries = []
		self.add_party_gl_entries(gl_entries)
		self.add_bank_gl_entries(gl_entries)
		self.add_deductions_gl_entries(gl_entries)
		self.add_tax_gl_entries(gl_entries)

		gl_entries = process_gl_map(gl_entries)
		make_gl_entries(gl_entries, cancel=cancel, adv_adj=adv_adj)
		
		if self.status == 'Voided':
			self.posting_date = original_posting_date

	def set_status(self):
		if self.status == "Voided":
			pass
		elif self.docstatus == 2:
			self.status = "Cancelled"
		elif self.docstatus == 1:
			self.status = "Submitted"
		else:
			self.status = "Draft"

		self.db_set("status", self.status, update_modified=True)


@frappe.whitelist()
def update_check_number(doc: PaymentEntry, method: str | None = None) -> None:
	mode_of_payment_type = frappe.db.get_value("Mode of Payment", doc.mode_of_payment, "type")
	if doc.bank_account and mode_of_payment_type == "Bank" and str(doc.reference_no).isdigit():
		frappe.db.set_value("Bank Account", doc.bank_account, "check_number", doc.reference_no)


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
