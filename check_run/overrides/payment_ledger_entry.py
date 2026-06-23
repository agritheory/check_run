# Copyright (c) 2026, AgriTheory and contributors
# For license information, please see license.txt

import frappe
from erpnext.accounts.doctype.payment_ledger_entry.payment_ledger_entry import PaymentLedgerEntry


class CheckRunPaymentLedgerEntry(PaymentLedgerEntry):
	def validate_account(self):
		if frappe.db.exists(
			"Check Run Settings",
			{
				"company": self.company,
				"pay_to_account": self.account,
				"include_tax_payable": 1,
			},
		):
			return
		super().validate_account()
