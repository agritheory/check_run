import frappe


def execute():
	pts = frappe.db.sql(
		"""
		SELECT `tabPayment Schedule`.parent, `tabPayment Schedule`.name
		FROM `tabPayment Schedule`, `tabPurchase Invoice`
		WHERE `tabPayment Schedule`.outstanding > 0.0
		AND `tabPayment Schedule`.parent = `tabPurchase Invoice`.name
		AND `tabPurchase Invoice`.status = 'Paid'
	""",
		as_dict=True,
	)

	for ps in pts:
		frappe.db.set_value("Payment Schedule", ps.name, "outstanding", 0.0)
