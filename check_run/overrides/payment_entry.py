# Copyright (c) 2023, AgriTheory and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import get_link_to_form, comma_and, flt
from erpnext.accounts.general_ledger import make_gl_entries, process_gl_map
from frappe.utils.data import getdate
from erpnext.accounts.doctype.payment_entry.payment_entry import (
	PaymentEntry,
	get_outstanding_reference_documents,
)
from frappe import _
import json


class CustomPaymentEntry(PaymentEntry):
	def make_gl_entries(self, cancel=0, adv_adj=0):
		if self.payment_type in ("Receive", "Pay") and not self.get("party_account_field"):
			self.setup_party_account_field()

		if self.status == "Voided":
			original_posting_date = self.posting_date
			self.voided_date = self.posting_date = getdate()

		gl_entries = []
		self.add_party_gl_entries(gl_entries)
		self.add_bank_gl_entries(gl_entries)
		self.add_deductions_gl_entries(gl_entries)
		self.add_tax_gl_entries(gl_entries)

		gl_entries = process_gl_map(gl_entries)
		make_gl_entries(gl_entries, cancel=cancel, adv_adj=adv_adj)

		if self.status == "Voided":
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

	# Bug Fix
	def get_valid_reference_doctypes(self):
		if self.party_type == "Customer":
			return ("Sales Order", "Sales Invoice", "Journal Entry", "Dunning")
		elif self.party_type == "Supplier":
			return ("Purchase Order", "Purchase Invoice", "Journal Entry")
		elif self.party_type == "Shareholder":
			return ("Journal Entry",)
		elif self.party_type == "Employee":
			return ("Journal Entry", "Expense Claim")  # Expense Claim

	#
	def validate_allocated_amount(self):
		if self.payment_type == "Internal Transfer":
			return

		if self.party_type in ("Customer", "Supplier"):
			self.validate_allocated_amount_with_latest_data()
		else:
			fail_message = _(
				"{0} Row {1} / {2}: Allocated Amount of {3} cannot be greater than outstanding amount of {4}."
			)
			for d in self.get("references"):
				if (flt(d.allocated_amount)) > 0 and flt(d.allocated_amount) > flt(d.outstanding_amount):
					frappe.throw(
						fail_message.format(
							self.party_name,
							d.idx,
							get_link_to_form(d.reference_doctype, d.reference_name),
							d.allocated_amount,
							d.outstanding_amount,
						)
					)

				# Check for negative outstanding invoices as well
				if flt(d.allocated_amount) < 0 and flt(d.allocated_amount) < flt(d.outstanding_amount):
					frappe.throw(
						fail_message.format(
							self.party_name,
							d.idx,
							get_link_to_form(d.reference_doctype, d.reference_name),
							d.allocated_amount,
							d.outstanding_amount,
						)
					)

	def validate_allocated_amount_with_latest_data(self):
		if self.references:
			uniq_vouchers = {(x.reference_doctype, x.reference_name) for x in self.references}
			vouchers = [frappe._dict({"voucher_type": x[0], "voucher_no": x[1]}) for x in uniq_vouchers]
			latest_references = get_outstanding_reference_documents(
				{
					"posting_date": self.posting_date,
					"company": self.company,
					"party_type": self.party_type,
					"payment_type": self.payment_type,
					"party": self.party,
					"party_account": self.paid_from if self.payment_type == "Receive" else self.paid_to,
					"get_outstanding_invoices": True,
					"get_orders_to_be_billed": True,
					"vouchers": vouchers,
				}
			)

			# Group latest_references by (voucher_type, voucher_no)
			latest_lookup = {}
			for d in latest_references:
				d = frappe._dict(d)
				latest_lookup.setdefault((d.voucher_type, d.voucher_no), frappe._dict())[d.payment_term] = d

			for idx, d in enumerate(self.get("references"), start=1):
				latest = latest_lookup.get((d.reference_doctype, d.reference_name)) or frappe._dict()

				# If term based allocation is enabled, throw
				if (
					d.payment_term is None or d.payment_term == ""
				) and self.term_based_allocation_enabled_for_reference(
					d.reference_doctype, d.reference_name
				):
					frappe.throw(
						_(
							"{0} has Payment Term based allocation enabled. Select a Payment Term for Row #{1} in Payment References section"
						).format(frappe.bold(d.reference_name), frappe.bold(idx))
					)

				# if no payment template is used by invoice and has a custom term(no `payment_term`), then invoice outstanding will be in 'None' key
				latest = latest.get(d.payment_term) or latest.get(None)
				# The reference has already been fully paid
				if not latest:
					frappe.throw(
						_("{0} {1} has already been fully paid.").format(_(d.reference_doctype), d.reference_name)
					)
				# The reference has already been partly paid
				elif (
					latest.outstanding_amount < latest.invoice_amount
					and flt(d.outstanding_amount, d.precision("outstanding_amount"))
					!= flt(latest.outstanding_amount, d.precision("outstanding_amount"))
					and d.payment_term == ""
				):
					frappe.throw(
						_(
							"{0} {1} has already been partly paid. Please use the 'Get Outstanding Invoice' or the 'Get Outstanding Orders' button to get the latest outstanding amounts."
						).format(_(d.reference_doctype), d.reference_name)
					)

				fail_message = _(
					"<b>Row #{1}</b> {0} / {2}: Allocated Amount of {3} cannot be greater than outstanding amount of {4}."
				)

				if (
					d.payment_term
					and (
						(flt(d.allocated_amount)) > 0
						and latest.payment_term_outstanding
						and (flt(d.allocated_amount) > flt(latest.payment_term_outstanding))
					)
					and self.term_based_allocation_enabled_for_reference(d.reference_doctype, d.reference_name)
				):
					frappe.throw(
						_(
							"Row #{0}: Allocated amount:{1} is greater than outstanding amount:{2} for Payment Term {3}"
						).format(
							d.idx, d.allocated_amount, latest.payment_term_outstanding, d.payment_term
						)
					)

				if (flt(d.allocated_amount)) > 0 and flt(d.allocated_amount) > flt(latest.outstanding_amount):
					frappe.throw(
						fail_message.format(
							self.party_name,
							d.idx,
							get_link_to_form(d.reference_doctype, d.reference_name),
							d.allocated_amount,
							d.outstanding_amount,
						)
					)

				# Check for negative outstanding invoices as well
				if flt(d.allocated_amount) < 0 and flt(d.allocated_amount) < flt(latest.outstanding_amount):
					frappe.throw(
						fail_message.format(
							self.party_name,
							d.idx,
							get_link_to_form(d.reference_doctype, d.reference_name),
							d.allocated_amount,
							d.outstanding_amount,
						)
					)


@frappe.whitelist()
def update_check_number(doc: PaymentEntry, method: str | None = None) -> None:
	mode_of_payment_type = frappe.db.get_value("Mode of Payment", doc.mode_of_payment, "type")
	if doc.bank_account and mode_of_payment_type == "Bank" and str(doc.reference_no).isdigit():
		frappe.db.set_value("Bank Account", doc.bank_account, "check_number", doc.reference_no)


@frappe.whitelist()
def validate_duplicate_check_number(doc: PaymentEntry, method: str | None = None) -> None:
	check_run_settings = frappe.db.exists(
		"Check Run Settings", {"bank_account": doc.bank_account, "pay_to_account": doc.paid_to}
	)
	if not check_run_settings or not frappe.db.get_value(
		"Check Run Settings", check_run_settings, "validate_unique_check_number"
	):
		return

	mode_of_payment_type = frappe.db.get_value("Mode of Payment", doc.mode_of_payment, "type")
	if mode_of_payment_type != "Bank" or not str(doc.reference_no).isdigit():
		return

	pe_names = frappe.get_all(
		"Payment Entry",
		{
			"payment_type": "Pay",
			"name": ["!=", doc.name],
			"docstatus": ["!=", 2],
			"reference_no": doc.reference_no,
		},
	)
	if not pe_names:
		return

	error_message = "</li><li>".join([get_link_to_form("Payment Entry", p.name) for p in pe_names])
	frappe.throw(
		msg=frappe._(
			f"Check Number {doc.reference_no} is already set in:<br><br><ul><li>{error_message}</li></ul>"
		),
		title="Check Number already exists",
	)


@frappe.whitelist()
def validate_add_payment_term(doc: PaymentEntry, method: str | None = None):
	doc = frappe._dict(json.loads(doc)) if isinstance(doc, str) else doc
	if doc.check_run:
		return
	adjusted_refs = []
	for r in doc.get("references"):
		if r.reference_doctype == "Purchase Invoice" and not r.payment_term:
			pmt_term = frappe.get_all(
				"Payment Schedule",
				{"parent": r.reference_name, "outstanding": [">", 0.0]},
				["payment_term"],
				order_by="due_date ASC",
				limit=1,
			)
			if pmt_term:
				r.payment_term = pmt_term[0].get("payment_term")
				adjusted_refs.append(r.reference_name)
	if adjusted_refs:
		frappe.msgprint(
			msg=frappe._(
				f"An outstanding Payment Schedule term was detected and added for {comma_and(adjusted_refs)} in the references table.<br>Please review - "
				"this field must be filled in for the Payment Schedule to synchronize and to prevent a paid invoice portion from showing up in a Check Run."
			),
			title=frappe._("Payment Schedule Term Added"),
		)
