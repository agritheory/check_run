# Copyright (c) 2026, AgriTheory and contributors
# For license information, please see license.txt

import frappe
from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import (
	get_accounting_dimensions,
)
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice
from erpnext.accounts.party import get_due_date
from erpnext.accounts.utils import get_account_currency
from check_run.overrides.payment_entry import (
	create_payment_ledger_entry,
	get_tax_payable_gl_entries_for_voucher,
	tax_payable_gl_entries,
)
from frappe.utils.data import cint, flt


def is_tax_payable_account(company, account):
	return bool(
		company
		and account
		and frappe.db.exists(
			"Check Run Settings",
			{"company": company, "pay_to_account": account, "include_tax_payable": 1},
		)
	)


class CheckRunSalesInvoice(SalesInvoice):
	def validate(self):
		"""
		HASH: 0e64acb0fa04042268805e11fa4f7b4a082708aa
		REPO: https://github.com/frappe/erpnext/
		PATH: erpnext/accounts/doctype/sales_invoice/sales_invoice.py
		METHOD: validate
		"""
		for row in self.taxes:
			if not is_tax_payable_account(self.company, row.account_head):
				continue
			if not (row.party_type and row.party):
				frappe.throw(
					frappe._("Party Type and Party are required on tax row {0} when using account {1}").format(
						row.description or row.idx, row.account_head
					)
				)
			row.outstanding_amount = row.tax_amount
			due_date = get_due_date(self.posting_date, row.party_type, row.party, self.company)
			row.due_date = due_date or self.posting_date
		super().validate()

	def on_submit(self):
		"""
		HASH: 0e64acb0fa04042268805e11fa4f7b4a082708aa
		REPO: https://github.com/frappe/erpnext/
		PATH: erpnext/accounts/doctype/sales_invoice/sales_invoice.py
		METHOD: on_submit
		"""
		if self.is_return and self.return_against:
			self._reduce_original_tax_outstanding()
		super().on_submit()

	def _reduce_original_tax_outstanding(self):
		for return_row in self.taxes:
			if not (return_row.party and return_row.party_type):
				continue
			orig_row_name = frappe.db.get_value(
				"Sales Taxes and Charges",
				{
					"parent": self.return_against,
					"account_head": return_row.account_head,
					"party": return_row.party,
				},
				"name",
			)
			if not orig_row_name:
				continue
			orig_outstanding = flt(
				frappe.db.get_value("Sales Taxes and Charges", orig_row_name, "outstanding_amount")
			)
			reduction = flt(abs(return_row.tax_amount))
			new_outstanding = flt(orig_outstanding - reduction, return_row.precision("tax_amount"))
			frappe.db.set_value(
				"Sales Taxes and Charges",
				orig_row_name,
				"outstanding_amount",
				max(0.0, new_outstanding),
			)

	def make_gl_entries(self, gl_entries=None, from_repost=False):
		if self.docstatus == 2 and not gl_entries:
			tax_gl = get_tax_payable_gl_entries_for_voucher(self.doctype, self.name)
		else:
			if not gl_entries:
				gl_entries = self.get_gl_entries()
			tax_gl = tax_payable_gl_entries(gl_entries, company=self.company)

		super().make_gl_entries(gl_entries, from_repost=from_repost)

		if not tax_gl:
			return

		update_outstanding = "Yes"
		if self.docstatus == 1:
			update_outstanding = (
				"No"
				if (cint(self.is_pos) or self.write_off_account or cint(self.redeem_loyalty_points))
				else "Yes"
			)

		create_payment_ledger_entry(
			tax_gl,
			cancel=(self.docstatus == 2),
			from_repost=from_repost,
			update_outstanding=update_outstanding,
		)

	def make_tax_gl_entries(self, gl_entries):
		"""
		HASH: 0e64acb0fa04042268805e11fa4f7b4a082708aa
		REPO: https://github.com/frappe/erpnext/
		PATH: erpnext/accounts/doctype/sales_invoice/sales_invoice.py
		METHOD: make_tax_gl_entries
		"""
		enable_discount_accounting = cint(
			frappe.db.get_single_value("Selling Settings", "enable_discount_accounting")
		)

		accounting_dimensions = get_accounting_dimensions()
		for tax in self.get("taxes"):
			amount, base_amount = self.get_tax_amounts(tax, enable_discount_accounting)
			if flt(tax.base_tax_amount_after_discount_amount):
				account_currency = get_account_currency(tax.account_head)
				track_tax_payable = is_tax_payable_account(self.company, tax.account_head)
				dimensions = {d: tax.get(d) for d in accounting_dimensions if d != "cost_center"}
				gl_entries.append(
					self.get_gl_dict(
						{
							"account": tax.account_head,
							"against": self.customer,
							"credit": flt(base_amount, tax.precision("tax_amount_after_discount_amount")),
							"credit_in_account_currency": (
								flt(base_amount, tax.precision("base_tax_amount_after_discount_amount"))
								if account_currency == self.company_currency
								else flt(amount, tax.precision("tax_amount_after_discount_amount"))
							),
							"cost_center": tax.cost_center,
							"party_type": tax.party_type if track_tax_payable else None,
							"party": tax.party if track_tax_payable else None,
							"against_voucher": tax.name if track_tax_payable else None,
							"against_voucher_type": ("Sales Taxes and Charges" if track_tax_payable else None),
							**dimensions,
						},
						account_currency,
						item=tax,
					)
				)
