import frappe
from frappe import _

from erpnext.accounts.doctype.bank.bank import Bank


class CustomBank(Bank):
	def validate(self):
		# Canadian banking institutions limit DFI Routing Numbers to 8 characters
		addresses = frappe.qb.DocType("Address")
		dls = frappe.qb.DocType("Dynamic Link")

		countries_qb = (
			frappe.qb.from_(addresses)
			.inner_join(dls)
			.on(addresses.name == dls.parent)
			.select(addresses.country)
			.where(dls.parenttype == "Address")
			.where(dls.link_doctype == "Bank")
			.where(dls.link_name == self.name)
		)

		countries = frappe.db.sql(countries_qb, as_dict=True, pluck="country")
		if "Canada" in countries:
			if len(self.aba_number) > 8:
				frappe.throw(
					_(
						"This Bank is linked to at least one Canadian address. Canadian banking institutions require the ABA Number must not exceed 8 characters."
					)
				)
		return
