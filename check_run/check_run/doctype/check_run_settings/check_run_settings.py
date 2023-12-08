# Copyright (c) 2022, AgriTheory and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CheckRunSettings(Document):
	pass


@frappe.whitelist()
def create(company: str, bank_account: str, pay_to_account: str) -> str:
	crs = frappe.new_doc("Check Run Settings")
	crs.company = company
	crs.bank_account = bank_account
	crs.pay_to_account = pay_to_account
	crs.save()
	return crs
