import frappe


def execute():
	cr_settings = frappe.get_all("Check Run Settings", pluck="name")
	bank_mop = frappe.get_all("Mode of Payment", {"type": "Bank"}, pluck="name")

	if not cr_settings or not bank_mop:
		return

	for crs in cr_settings:
		crs = frappe.get_doc("Check Run Settings", crs)
		crs_mops = frappe.get_all(
			"Check Run Printable MOP", {"parent": crs}, "mode_of_payment", pluck="mode_of_payment"
		)
		for mop in bank_mop:
			if mop not in crs_mops:
				crs.append("printable_mop_in_check_run", {"mode_of_payment": mop})
		crs.save()
