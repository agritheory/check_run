import frappe
from erpnext.accounts.doctype.sales_taxes_and_charges.sales_taxes_and_charges import (
	SalesTaxesandCharges,
)


class CheckRunSalesTaxesandCharges(SalesTaxesandCharges):
	@property
	def company(self):
		return frappe.get_value("Sales Invoice", self.parent, "company")
