import frappe


@frappe.whitelist()
def show_bank_account_number(doctype, docname):
	doc = frappe.get_doc(doctype, docname)
	routing_number = frappe.get_value('Bank', doc.bank, 'aba_number')
	account_number = doc.get_password('bank_account')
	return {'routing_number': routing_number, 'account_number': account_number}