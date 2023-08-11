# Copyright (c) 2022, AgriTheory and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	return get_columns(filters), get_data(filters)


def get_data(filters):
	return frappe.db.sql("""
		SELECT 
		pi.name AS purchase_invoice_name,
		pi.title,
		pi.supplier,
		pi.company,
		pi.posting_date,
		pi.grand_total,
		pi.status,
		pi.currency,
		pi.supplier_name,
		pi.grand_total,
		pi.outstanding_amount,
		pi.due_date,
		pi.is_return,
		pi.release_date,
		pi.represents_company,
		pi.is_internal_supplier,
		file.file_name AS attachments,
		file.file_url
		FROM `tabPurchase Invoice` AS pi
		LEFT JOIN `tabFile` AS file
		ON  file.attached_to_name = pi.name
		AND file.attached_to_doctype = 'Purchase Invoice'
		AND file.file_url  LIKE '%.pdf'
		ORDER BY pi.modified DESC
		""",
		as_dict=True,
	)


def get_columns(filters):
	return [
		
		{
			"label": frappe._("Name"),
			"fieldname": "purchase_invoice_name",
			"fieldtype": "Link",
			"options": "Purchase Invoice",
			"width": "150px",
		},
		{
			"label": frappe._("Title"),
			"fieldname": "title",
			"fieldtype": "Data",
			"width": "200px",
		},
		{
			"label": frappe._("Supplier"),
			"fieldname": "supplier",
			"fieldtype": "Link",
			"options": "Supplier",
			"width": "200px",
		},
		{
			"label": frappe._("Supplier Name"),
			"fieldname": "supplier_name",
			"fieldtype": "Data",
			"width": "200px",
		},
		{
			"label": frappe._("Company"),
			"fieldname": "company",
			"fieldtype": "Link",
			"options": "Company",
			"width": "200px",
		},
		{
			"label": frappe._("Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": "200px",
		},
		{
			"label": frappe._("Grand Total"),
			"fieldname": "grand_total",
			"fieldtype": "Currency",
			"width": "200px",
		},
		{
			"label": frappe._("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": "200px",
		},
		{
			"label": frappe._("Currency"),
			"fieldname": "currency",
			"fieldtype": "Link",
			"options": "Currency",
			"width": "200px",
		},
		{
			"label": frappe._("Grand Total (Company Currency)"),
			"fieldname": "grand_total",
			"fieldtype": "Currency",
			"width": "200px",
		},
		{
			"label": frappe._("Outstanding Amount"),
			"fieldname": "outstanding_amount",
			"fieldtype": "Currency",
			"width": "200px",
		},
		{
			"label": frappe._("Due Date"),
			"fieldname": "due_date",
			"fieldtype": "Date",
			"width": "200px",
		},
		{
			"label": frappe._("Is Return (Debit Note)"),
			"fieldname": "is_return",
			"fieldtype": "Check",
			"width": "200px",
		},
		{
			"label": frappe._("Release Date"),
			"fieldname": "release_date",
			"fieldtype": "Date",
			"width": "200px",
		},
		{
			"label": frappe._("Represents Company"),
			"fieldname": "represents_company",
			"fieldtype": "Link",
			"options": "Company",
			"width": "200px",
		},
		{
			"label": frappe._("Is Internal Supplier"),
			"fieldname": "is_internal_supplier",
			"fieldtype": "Check",
			"width": "200px",
		},
		{
			"label": frappe._("Attachments"),
			"fieldname": "attachments",
			"fieldtype": "Data",
			"width": "200px",
		},
	]

