# Copyright (c) 2022, AgriTheory and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	print(filters)
	return get_columns(filters), get_data(filters)

def get_columns(filters):
	return [
		{
			"label": frappe._("Check Date"),
			"fieldname": "check_date",
			"fieldtype": "Date",
			"width": "150px"
		},
		{
			"label": frappe._("Check Number"),
			"fieldname": "check_number",
			"fieldtype": "Data",
			"width": "200px",
		},
		{
			"label": frappe._("Party Name"),
			"fieldname": "party_name",
			"fieldtype": "Data",
			"width": "400px",
		},
	]

def get_data(filters):
	return frappe.db.sql("""
		SELECT
			`tabPayment Entry`.reference_no AS check_number,
			`tabPayment Entry`.reference_date AS check_date,
			`tabPayment Entry`.party_name AS party_name
		FROM `tabPayment Entry`
		WHERE
		`tabPayment Entry`.reference_date >= %(start_date)s 
		AND `tabPayment Entry`.reference_date <= %(end_date)s
		AND `tabPayment Entry`.bank_account = %(bank_account)s
		AND `tabPayment Entry`.payment_type = 'Pay'
		AND `tabPayment Entry`.mode_of_payment = 'Check'
		AND `tabPayment Entry`.docstatus = 1
		ORDER BY check_date
		""", {
			'start_date': filters.start_date,
			'end_date': filters.end_date,
			'bank_account': filters.bank_account
	}, as_dict=True)

