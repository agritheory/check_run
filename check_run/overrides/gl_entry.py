# Copyright (c) 2026, AgriTheory and contributors
# For license information, please see license.txt

import frappe
from erpnext.accounts.doctype.gl_entry.gl_entry import GLEntry
from erpnext.accounts.party import validate_account_party_type, validate_party_frozen_disabled


class CheckRunGLEntry(GLEntry):
	def validate_party(self):
		validate_party_frozen_disabled(self.party_type, self.party)
		if (
			self.party_type
			and self.party
			and frappe.db.exists(
				"Check Run Settings",
				{
					"company": self.company,
					"pay_to_account": self.account,
					"include_tax_payable": 1,
				},
			)
		):
			return
		validate_account_party_type(self)
