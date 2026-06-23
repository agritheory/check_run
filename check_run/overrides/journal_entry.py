# Copyright (c) 2026, AgriTheory and contributors
# For license information, please see license.txt

from erpnext.accounts.doctype.journal_entry.journal_entry import JournalEntry
from erpnext.accounts.general_ledger import make_gl_entries
from erpnext.accounts.utils import cancel_exchange_gain_loss_journal

import frappe
from check_run.overrides.payment_entry import create_payment_ledger_entry, tax_payable_gl_entries


class CheckRunJournalEntry(JournalEntry):
	def make_gl_entries(self, cancel=0, adv_adj=0):
		merge_entries = frappe.db.get_single_value("Accounts Settings", "merge_similar_account_heads")

		gl_map = self.build_gl_map()
		if self.voucher_type in ("Deferred Revenue", "Deferred Expense"):
			update_outstanding = "No"
		else:
			update_outstanding = "Yes"

		tax_gl = tax_payable_gl_entries(gl_map)

		if gl_map:
			make_gl_entries(
				gl_map,
				cancel=cancel,
				adv_adj=adv_adj,
				merge_entries=merge_entries,
				update_outstanding=update_outstanding,
			)
			frappe.flags.party_not_required = False
			if cancel:
				cancel_exchange_gain_loss_journal(frappe._dict(doctype=self.doctype, name=self.name))

		if tax_gl:
			create_payment_ledger_entry(
				tax_gl,
				cancel=cancel,
				adv_adj=adv_adj,
				update_outstanding=update_outstanding,
			)
