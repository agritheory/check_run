import frappe
from frappe import _
from frappe.utils import cint, flt

from erpnext.accounts.doctype.bank.bank import Bank


class CustomBank(Bank):
	def validate(self):
		# Canadian banking institutions limit DFI Routing Numbers to 8 characters
		countries = frappe.db.sql(
			"""
			select a.country
			from `tabAddress` a, `tabDynamic Link` dl
			where dl.parent = a.name and dl.parenttype = 'Address'
			and dl.link_doctype = 'Bank' and dl.link_name = %s
			""",
			(self.name),
			as_dict=True
		)
		if 'Canada' in [c['country'] for c in countries]:
			if len(self.aba_number) > 8:
				frappe.throw(_("This Bank is linked to at least one Canadian address. Canadian banking institutions require the ABA Number must not exceed 8 characters."))
		return
