import frappe


@frappe.whitelist()
def get_buying_settings():
	return frappe.get_doc("Buying Settings")
