# Copyright (c) 2023, AgriTheory and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import get_link_to_form, flt
from erpnext.accounts.general_ledger import make_gl_entries, process_gl_map
from frappe.utils.data import getdate
from erpnext.accounts.doctype.payment_entry.payment_entry import (
	PaymentEntry,
	get_outstanding_reference_documents,
)
from frappe import _


class CheckRunPaymentEntry(PaymentEntry):
	def make_gl_entries(self, cancel=0, adv_adj=0):
		"""
		HASH: ff14d72a4620f55c4282e0cc29b6ffc08419334d
		REPO: https://github.com/frappe/erpnext/
		PATH: erpnext/accounts/doctype/payment_entry/payment_entry.py
		METHOD: make_gl_entries
		"""
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
		"""
		HASH: ff14d72a4620f55c4282e0cc29b6ffc08419334d
		REPO: https://github.com/frappe/erpnext/
		PATH: erpnext/accounts/doctype/payment_entry/payment_entry.py
		METHOD: set_status
		"""
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
		"""
		HASH: ff14d72a4620f55c4282e0cc29b6ffc08419334d
		REPO: https://github.com/frappe/erpnext/
		PATH: erpnext/accounts/doctype/payment_entry/payment_entry.py
		METHOD: get_valid_reference_doctypes
		"""
		if self.party_type == "Customer":
			return ("Sales Order", "Sales Invoice", "Journal Entry", "Dunning")
		elif self.party_type == "Supplier":
			return ("Purchase Order", "Purchase Invoice", "Journal Entry")
		elif self.party_type == "Shareholder":
			return ("Journal Entry",)
		elif self.party_type == "Employee":
			return ("Journal Entry", "Expense Claim")  # Expense Claim

	"""
	Because Check Run processes multiple payment entries in a background queue, errors generally do not include
	enough data to identify the problem since there were written and remain appropriate for the context of an individual
	Payment Entry. This code is copied from: 

	https://github.com/frappe/erpnext/blob/version-14/erpnext/accounts/doctype/payment_entry/payment_entry.py#L164

	https://github.com/frappe/erpnext/blob/version-14/erpnext/accounts/doctype/payment_entry/payment_entry.py#L194
	"""

	def validate_allocated_amount(self):
		"""
		HASH: ff14d72a4620f55c4282e0cc29b6ffc08419334d
		REPO: https://github.com/frappe/erpnext/
		PATH: erpnext/accounts/doctype/payment_entry/payment_entry.py
		METHOD: validate_allocated_amount
		"""
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
		"""
		HASH: ff14d72a4620f55c4282e0cc29b6ffc08419334d
		REPO: https://github.com/frappe/erpnext/
		PATH: erpnext/accounts/doctype/payment_entry/payment_entry.py
		METHOD: validate_allocated_amount_with_latest_data
		"""
		if self.references:
			unique_vouchers = {(x.reference_doctype, x.reference_name) for x in self.references}
			vouchers = [frappe._dict({"voucher_type": x[0], "voucher_no": x[1]}) for x in unique_vouchers]
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
def update_outstanding_amount(doc: PaymentEntry, method: str | None = None):
	paid_amount = doc.paid_amount if method == "on_submit" else 0.0
	for r in doc.get("references"):
		if r.reference_doctype != "Purchase Invoice":
			continue
		payment_schedules = frappe.get_all(
			"Payment Schedule",
			{"parent": r.reference_name},
			["name", "outstanding", "payment_term", "payment_amount"],
			order_by="due_date ASC",
		)
		if not payment_schedules:
			continue

		payment_schedule = frappe.get_doc("Payment Schedule", payment_schedules[0]["name"])
		precision = payment_schedule.precision("outstanding")
		payment_schedules = payment_schedules if method == "on_submit" else reversed(payment_schedules)

		for term in payment_schedules:
			if r.payment_term and term.payment_term != r.payment_term:
				continue

			if method == "on_submit":
				if term.outstanding > 0.0 and paid_amount > 0.0:
					if term.outstanding > paid_amount:
						frappe.db.set_value(
							"Payment Schedule",
							term.name,
							"outstanding",
							flt(term.outstanding - paid_amount, precision),
						)
						break
					else:
						paid_amount = flt(paid_amount - term.outstanding, precision)
						frappe.db.set_value("Payment Schedule", term.name, "outstanding", 0)
						if paid_amount <= 0.0:
							break

			if method == "on_cancel":
				if term.outstanding != term.payment_amount:
					# if this payment term had previously been allocated against
					paid_amount += flt(paid_amount + (term.payment_amount - term.outstanding), precision)
					reverse = (
						flt(paid_amount + term.outstanding, precision)
						if paid_amount < term.payment_amount
						else term.payment_amount
					)
					frappe.db.set_value("Payment Schedule", term.name, "outstanding", reverse)
					if paid_amount >= doc.paid_amount:
						break
