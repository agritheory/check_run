import frappe
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice
from erpnext.accounts.party import get_due_date
from erpnext.accounts.utils import get_account_currency
from frappe.utils.data import cint, flt


class CheckRunSalesInvoice(SalesInvoice):
	# TODO: update due date in taxes with validate hook
	def validate(self):
		super().validate()
		for row in self.taxes:
			if not row.party:
				continue
			due_date = get_due_date(self.posting_date, row.party_type, row.party, self.company)
			row.due_date = due_date or self.posting_date
			row.outstanding_amount = row.tax_amount

	def on_submit(self):
		for row in self.taxes:
			if row.party and row.party_type:
				row.outstanding_amount = row.tax_amount
		super().on_submit()

	def make_tax_gl_entries(self, gl_entries):
		enable_discount_accounting = cint(
			frappe.db.get_single_value("Selling Settings", "enable_discount_accounting")
		)

		for tax in self.get("taxes"):
			amount, base_amount = self.get_tax_amounts(tax, enable_discount_accounting)
			if flt(tax.base_tax_amount_after_discount_amount):
				account_currency = get_account_currency(tax.account_head)
				is_payable_account = bool(
					frappe.get_value("Account", tax.account_head, "account_type") == "Payable"
				)
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
						},
						account_currency,
						item=tax,
					)
				)
