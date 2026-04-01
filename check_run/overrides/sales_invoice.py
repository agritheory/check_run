# Copyright (c) 2026, AgriTheory and contributors
# For license information, please see license.txt

import frappe
from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import (
	get_accounting_dimensions,
)
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice
from erpnext.accounts.party import get_due_date
from erpnext.accounts.utils import get_account_currency
from frappe.utils.data import cint, flt


class CheckRunSalesInvoice(SalesInvoice):
	def validate(self):
		"""
		HASH: f8ab56ecc96ae7c28b9f7b8e79488ff2c47cc810
		REPO: https://github.com/frappe/erpnext/
		PATH: erpnext/accounts/doctype/sales_invoice/sales_invoice.py
		METHOD: validate
		"""
		for row in self.taxes:
			if not row.party:
				continue
			due_date = get_due_date(self.posting_date, row.party_type, row.party, self.company)
			row.due_date = due_date or self.posting_date
			row.outstanding_amount = row.tax_amount
		super().validate()

	def on_submit(self):
		"""
		HASH: f8ab56ecc96ae7c28b9f7b8e79488ff2c47cc810
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

	def make_tax_gl_entries(self, gl_entries):
		"""
		HASH: f8ab56ecc96ae7c28b9f7b8e79488ff2c47cc810
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
				is_payable_account = bool(
					frappe.get_value("Account", tax.account_head, "account_type") == "Payable"
				)
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
							"party_type": tax.party_type if is_payable_account else None,
							"party": tax.party if is_payable_account else None,
							**dimensions,
						},
						account_currency,
						item=tax,
					)
				)
