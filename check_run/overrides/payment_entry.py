# Copyright (c) 2023, AgriTheory and contributors
# For license information, please see license.txt

import base64
import copy

import frappe
from erpnext.accounts.doctype.payment_entry.payment_entry import (
	PaymentEntry,
	add_regional_gl_entries,
	get_outstanding_reference_documents,
)
from erpnext.accounts.general_ledger import (
	check_freezing_date,
	make_acc_dimensions_offsetting_entry,
	make_entry,
	process_gl_map,
	save_entries,
	set_as_cancel,
	validate_accounting_period,
	validate_against_pcv,
	validate_disabled_accounts,
)
from erpnext.accounts.utils import get_payment_ledger_entries, is_immutable_ledger_enabled
from frappe import _, safe_decode
from frappe.core.doctype.file.utils import get_local_image
from frappe.utils import flt, get_link_to_form, now
from frappe.utils.data import getdate


class CheckRunPaymentEntry(PaymentEntry):
	def make_gl_entries(self, cancel=0, adv_adj=0):
		"""
		HASH: 86853224c3df3089c78b09916c1d26a63bd9751e
		REPO: https://github.com/frappe/erpnext/
		PATH: erpnext/accounts/doctype/payment_entry/payment_entry.py
		METHOD: make_gl_entries

		This method overrides both build_gl_map and make_gl_entries
		"""
		if self.payment_type in ("Receive", "Pay") and not self.get("party_account_field"):
			self.setup_party_account_field()
		self.set_transaction_currency_and_rate()

		voided_date = None
		if self.status == "Voided":
			# voided_date field is set via the dialog from the UI
			voided_date = frappe.get_value(self.doctype, self.name, "voided_date") or getdate()
			original_posting_date = self.posting_date
			self.voided_date = self.posting_date = voided_date

		gl_entries = []
		self.add_party_gl_entries(gl_entries)
		self.add_bank_gl_entries(gl_entries)
		self.add_deductions_gl_entries(gl_entries)
		self.add_tax_gl_entries(gl_entries)
		add_regional_gl_entries(gl_entries, self)

		gl_entries = process_gl_map(gl_entries)
		make_gl_entries(gl_entries, cancel=cancel, adv_adj=adv_adj, voided_date=voided_date)

		if self.status == "Voided":
			self.posting_date = original_posting_date

	def set_status(self):
		"""
		HASH: 86853224c3df3089c78b09916c1d26a63bd9751e
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
		HASH: 86853224c3df3089c78b09916c1d26a63bd9751e
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
		HASH: 86853224c3df3089c78b09916c1d26a63bd9751e
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
		HASH: 86853224c3df3089c78b09916c1d26a63bd9751e
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


def make_gl_entries(
	gl_map,
	cancel=False,
	adv_adj=False,
	merge_entries=True,
	update_outstanding="Yes",
	from_repost=False,
	voided_date=None,  # CUSTOM CODE
):
	"""
	HASH: a2b6e4a1c587ce2f7e017f39944899f76e3e2f7d
	REPO: https://github.com/frappe/erpnext/
	PATH: erpnext/accounts/general_ledger.py
	METHOD: make_gl_entries
	"""
	if gl_map:
		if not cancel:
			make_acc_dimensions_offsetting_entry(gl_map)
			validate_accounting_period(gl_map)
			validate_disabled_accounts(gl_map)
			gl_map = process_gl_map(gl_map, merge_entries, from_repost=from_repost)
			if gl_map and len(gl_map) > 1:
				if gl_map[0].voucher_type != "Period Closing Voucher":
					create_payment_ledger_entry(
						gl_map,
						cancel=0,
						adv_adj=adv_adj,
						update_outstanding=update_outstanding,
						from_repost=from_repost,
						voided_date=voided_date,  # CUSTOM CODE
					)
				save_entries(gl_map, adv_adj, update_outstanding, from_repost)
			# Post GL Map process there may no be any GL Entries
			elif gl_map:
				frappe.throw(
					_(
						"Incorrect number of General Ledger Entries found. You might have selected a wrong Account in the transaction."
					)
				)
		else:
			make_reverse_gl_entries(
				gl_map, adv_adj=adv_adj, update_outstanding=update_outstanding, voided_date=voided_date
			)  # CUSTOM CODE


def make_reverse_gl_entries(
	gl_entries=None,
	voucher_type=None,
	voucher_no=None,
	adv_adj=False,
	update_outstanding="Yes",
	partial_cancel=False,
	voided_date=None,  # CUSTOM CODE
):
	"""
	HASH: a2b6e4a1c587ce2f7e017f39944899f76e3e2f7d
	REPO: https://github.com/frappe/erpnext/
	PATH: erpnext/accounts/general_ledger.py
	METHOD: make_reverse_gl_entries

	Get original gl entries of the voucher
	and make reverse gl entries by swapping debit and credit
	"""

	immutable_ledger_enabled = is_immutable_ledger_enabled()

	if not gl_entries:
		gl_entry = frappe.qb.DocType("GL Entry")
		gl_entries = (
			frappe.qb.from_(gl_entry)
			.select("*")
			.where(gl_entry.voucher_type == voucher_type)
			.where(gl_entry.voucher_no == voucher_no)
			.where(gl_entry.is_cancelled == 0)
			.for_update()
		).run(as_dict=1)

	if gl_entries:
		create_payment_ledger_entry(
			gl_entries,
			cancel=1,
			adv_adj=adv_adj,
			update_outstanding=update_outstanding,
			partial_cancel=partial_cancel,
			voided_date=voided_date,  # CUSTOM CODE
		)
		validate_accounting_period(gl_entries)
		check_freezing_date(gl_entries[0]["posting_date"], adv_adj)

		is_opening = any(d.get("is_opening") == "Yes" for d in gl_entries)
		validate_against_pcv(is_opening, gl_entries[0]["posting_date"], gl_entries[0]["company"])
		if partial_cancel:
			# Partial cancel is only used by `Advance` in separate account feature.
			# Only cancel GL entries for unlinked reference using `voucher_detail_no`
			gle = frappe.qb.DocType("GL Entry")
			for x in gl_entries:
				query = (
					frappe.qb.update(gle)
					.set(gle.modified, now())
					.set(gle.modified_by, frappe.session.user)
					.where(
						(gle.company == x.company)
						& (gle.account == x.account)
						& (gle.party_type == x.party_type)
						& (gle.party == x.party)
						& (gle.voucher_type == x.voucher_type)
						& (gle.voucher_no == x.voucher_no)
						& (gle.against_voucher_type == x.against_voucher_type)
						& (gle.against_voucher == x.against_voucher)
						& (gle.voucher_detail_no == x.voucher_detail_no)
					)
				)

				if not immutable_ledger_enabled:
					query = query.set(gle.is_cancelled, True)

				query.run()
		else:
			if not immutable_ledger_enabled:
				gle_names = [x.get("name") for x in gl_entries]

				# if names are available, cancel only that set of entries
				if not all(gle_names):
					set_as_cancel(gl_entries[0]["voucher_type"], gl_entries[0]["voucher_no"])
				else:
					frappe.db.sql(
						"""UPDATE `tabGL Entry` SET is_cancelled = 1,
						modified=%s, modified_by=%s
						where name in %s and is_cancelled = 0""",
						(now(), frappe.session.user, tuple(gle_names)),
					)

		for entry in gl_entries:
			new_gle = copy.deepcopy(entry)
			new_gle["name"] = None
			debit = new_gle.get("debit", 0)
			credit = new_gle.get("credit", 0)

			debit_in_account_currency = new_gle.get("debit_in_account_currency", 0)
			credit_in_account_currency = new_gle.get("credit_in_account_currency", 0)
			debit_in_transaction_currency = new_gle.get("debit_in_transaction_currency", 0)
			credit_in_transaction_currency = new_gle.get("credit_in_transaction_currency", 0)

			new_gle["debit"] = credit
			new_gle["credit"] = debit
			new_gle["debit_in_account_currency"] = credit_in_account_currency
			new_gle["credit_in_account_currency"] = debit_in_account_currency
			new_gle["debit_in_transaction_currency"] = credit_in_transaction_currency
			new_gle["credit_in_transaction_currency"] = debit_in_transaction_currency

			new_gle["remarks"] = "On cancellation of " + new_gle["voucher_no"]
			new_gle["is_cancelled"] = 1

			if immutable_ledger_enabled:
				new_gle["is_cancelled"] = 0
				new_gle["posting_date"] = frappe.form_dict.get("posting_date") or getdate()

			if new_gle["debit"] or new_gle["credit"]:
				make_entry(new_gle, adv_adj, "Yes")


def create_payment_ledger_entry(
	gl_entries,
	cancel=0,
	adv_adj=0,
	update_outstanding="Yes",
	from_repost=0,
	partial_cancel=False,
	voided_date=None,  # CUSTOM CODE
):
	"""
	HASH: f039bfe35a575272049534bac9aa771260691bde
	REPO: https://github.com/frappe/erpnext/
	PATH: erpnext/accounts/utils.py
	METHOD: create_payment_ledger_entry
	"""
	if gl_entries:
		ple_map = get_payment_ledger_entries(gl_entries, cancel=cancel)

		for entry in ple_map:
			ple = frappe.get_doc(entry)

			if cancel:
				delink_original_entry(ple, partial_cancel=partial_cancel, voided_date=voided_date)
				if is_immutable_ledger_enabled():
					ple.delinked = 0
					ple.posting_date = frappe.form_dict.get("posting_date") or getdate()
				elif voided_date:
					ple.delinked = 0
					ple.posting_date = voided_date

			ple.flags.ignore_permissions = 1
			ple.flags.adv_adj = adv_adj
			ple.flags.from_repost = from_repost
			ple.flags.update_outstanding = update_outstanding
			ple.submit()


def delink_original_entry(pl_entry, partial_cancel=False, voided_date=None):  # CUSTOM CODE
	"""
	HASH: f039bfe35a575272049534bac9aa771260691bde
	REPO: https://github.com/frappe/erpnext/
	PATH: erpnext/accounts/utils.py
	METHOD: delink_original_entry
	"""
	if not pl_entry:
		return

	if pl_entry.doctype == "Advance Payment Ledger Entry":
		adv = frappe.qb.DocType("Advance Payment Ledger Entry")

		(
			frappe.qb.update(adv)
			.set(adv.delinked, 1)
			.set(adv.event, "Cancel")
			.set(adv.modified, now())
			.set(adv.modified_by, frappe.session.user)
			.where(adv.voucher_type == pl_entry.voucher_type)
			.where(adv.voucher_no == pl_entry.voucher_no)
			.where(adv.against_voucher_type == pl_entry.against_voucher_type)
			.where(adv.against_voucher_no == pl_entry.against_voucher_no)
			.where(adv.event == pl_entry.event)
			.run()
		)

	else:
		ple = frappe.qb.DocType("Payment Ledger Entry")
		query = (
			frappe.qb.update(ple)
			.set(ple.modified, now())
			.set(ple.modified_by, frappe.session.user)
			.where(
				(ple.company == pl_entry.company)
				& (ple.account_type == pl_entry.account_type)
				& (ple.account == pl_entry.account)
				& (ple.party_type == pl_entry.party_type)
				& (ple.party == pl_entry.party)
				& (ple.voucher_type == pl_entry.voucher_type)
				& (ple.voucher_no == pl_entry.voucher_no)
				& (ple.against_voucher_type == pl_entry.against_voucher_type)
				& (ple.against_voucher_no == pl_entry.against_voucher_no)
			)
		)

		if partial_cancel:
			query = query.where(ple.voucher_detail_no == pl_entry.voucher_detail_no)

		if not (is_immutable_ledger_enabled() or voided_date):  # CUSTOM CODE
			query = query.set(ple.delinked, True)

		query.run()


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


@frappe.whitelist()
def get_image_base64_data(file_url):
	file_doc = frappe.get_doc("File", {"file_url": file_url})
	if not file_doc.has_permission(permtype="read"):
		return ""
	image, unused_filename, extn = get_local_image(file_url)
	file_content = file_doc.get_content()
	return f"data:image/{extn};base64,{safe_decode(base64.b64encode(file_content).decode('utf-8'))}"


@frappe.whitelist()
def set_voided_date(doctype, docname, voided_date):
	doc = frappe.get_doc(doctype, docname)
	voided_date = getdate(voided_date)
	if voided_date < doc.posting_date:
		frappe.throw(
			msg=_("Void As Of Date cannot be before the Payment Entry's posting date."),
			title=_("Invalid Void As Of Date"),
		)
	frappe.db.set_value(doctype, docname, "voided_date", voided_date, update_modified=False)
