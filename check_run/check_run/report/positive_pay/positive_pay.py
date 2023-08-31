# Copyright (c) 2022, AgriTheory and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	return get_columns(filters), get_data(filters)


def get_columns(filters):
	return [
		{
			"label": frappe._("Check Date"),
			"fieldname": "check_date",
			"fieldtype": "Date",
			"width": "150px",
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
	pe = frappe.qb.DocType("Payment Entry")
	mop = frappe.qb.DocType("Mode of Payment")
	return (
		frappe.qb.from_(pe)
		.inner_join(mop)
		.on(pe.mode_of_payment == mop.name)
		.select(
			(pe.reference_no).as_("check_number"),
			(pe.reference_date).as_("check_date"),
			pe.party_name,
		)
		.where(pe.reference_date >= filters.start_date)
		.where(pe.reference_date <= filters.end_date)
		.where(pe.bank_account >= filters.bank_account)
		.where(mop.type == "Bank")
		.where(pe.docstatus == 1)
		.orderby(pe.reference_date)
		.run(as_dict=True)
	)
