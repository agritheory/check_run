import json

import frappe


@frappe.whitelist()
@frappe.read_only()
def show_bank_account_number(doctype, docname):
	doc = frappe.get_doc(doctype, docname)
	routing_number = frappe.get_value("Bank", doc.bank, "aba_number") or ""
	account_number = doc.get_password("bank_account", raise_exception=False) or ""
	return {"routing_number": routing_number, "account_number": account_number}


@frappe.whitelist()
def disallow_cancellation_if_in_check_run(doc, method=None):
	draft_check_runs = frappe.get_all("Check Run", ["name", "transactions"], {"docstatus": 0})
	for draft_check_run in draft_check_runs:
		if not draft_check_run.transactions:
			continue
		transactions = [
			t.get("ref_number") or t.get("name")
			for t in json.loads(draft_check_run.transactions)
			if t.get("pay")
		]
		if doc.name in transactions:
			frappe.throw(
				frappe._(
					f"""This document is currently selected for payment in draft {frappe.get_desk_link('Check Run', draft_check_run.name)} and cannot be cancelled."""
				)
			)
