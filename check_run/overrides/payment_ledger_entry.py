# Copyright (c) 2026, AgriTheory and contributors
# For license information, please see license.txt

import frappe
from erpnext.accounts.doctype.payment_ledger_entry.payment_ledger_entry import PaymentLedgerEntry


class CheckRunPaymentLedgerEntry(PaymentLedgerEntry):
	def validate_account(self):
		if frappe.get_cached_value("Account", self.account, "account_type") == "Tax":
			return
		super().validate_account()
