# Copyright (c) 2022, AgriTheory and contributors
# For license information, please see license.txt

import frappe
from frappe.desk.form.load import get_attachments
from frappe.query_builder import DocType
from pypika import Order


def execute(filters=None):
	return get_columns(filters), get_data(filters)


def get_data(filters):
	PurchaseInvoice = DocType("Purchase Invoice")
	data = (
		frappe.qb.from_(PurchaseInvoice)
		.select(
			PurchaseInvoice.name,
			PurchaseInvoice.title,
			PurchaseInvoice.supplier,
			PurchaseInvoice.company,
			PurchaseInvoice.posting_date,
			PurchaseInvoice.grand_total,
			PurchaseInvoice.status,
			PurchaseInvoice.currency,
			PurchaseInvoice.supplier_name,
			PurchaseInvoice.grand_total,
			PurchaseInvoice.outstanding_amount,
			PurchaseInvoice.due_date,
			PurchaseInvoice.is_return,
			PurchaseInvoice.release_date,
			PurchaseInvoice.represents_company,
			PurchaseInvoice.is_internal_supplier,
		)
		.orderby("modified", Order.desc)
	).run(as_dict=True)

	for row in data:
		row["attachments"] = "  ".join(
			[
				f"""<a data-pdf-preview="{attachment.file_url}" onclick="pdf_preview('{attachment.file_url}')">{attachment.file_name}</a>"""
				for attachment in get_attachments("Purchase Invoice", row["name"])
				if attachment.file_url.endswith(".pdf")
			]
		)
	return data


def get_columns(filters):
	return [
		{
			"label": frappe._("Name"),
			"fieldname": "name",
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
			"width": "400px",
		},
	]
