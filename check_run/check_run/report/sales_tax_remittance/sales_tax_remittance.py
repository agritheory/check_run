# Copyright (c) 2026, AgriTheory and contributors
# For license information, please see license.txt

from collections import defaultdict

import frappe
from frappe import _
from frappe.query_builder.functions import Coalesce
from frappe.utils import flt


def execute(filters=None):
	filters = frappe._dict(filters or {})
	return get_columns(filters), get_data(filters)


def get_columns(filters):
	if filters.get("show_detail"):
		return [
			{
				"label": _("Tax Authority"),
				"fieldname": "party",
				"fieldtype": "Link",
				"options": "Supplier",
				"width": 200,
			},
			{
				"label": _("Sales Invoice"),
				"fieldname": "sales_invoice",
				"fieldtype": "Link",
				"options": "Sales Invoice",
				"width": 160,
			},
			{
				"label": _("Customer"),
				"fieldname": "customer",
				"fieldtype": "Link",
				"options": "Customer",
				"width": 160,
			},
			{
				"label": _("Invoice Date"),
				"fieldname": "posting_date",
				"fieldtype": "Date",
				"width": 110,
			},
			{
				"label": _("Due Date"),
				"fieldname": "due_date",
				"fieldtype": "Date",
				"width": 110,
			},
			{
				"label": _("Tax Account"),
				"fieldname": "account_head",
				"fieldtype": "Link",
				"options": "Account",
				"width": 200,
			},
			{
				"label": _("Rate %"),
				"fieldname": "rate",
				"fieldtype": "Percent",
				"width": 80,
			},
			{
				"label": _("Tax Amount (Accrual)"),
				"fieldname": "tax_amount",
				"fieldtype": "Currency",
				"width": 150,
			},
			{
				"label": _("Customer Paid"),
				"fieldname": "customer_paid",
				"fieldtype": "Check",
				"width": 110,
			},
			{
				"label": _("Amount Remitted"),
				"fieldname": "amount_remitted",
				"fieldtype": "Currency",
				"width": 140,
			},
			{
				"label": _("Outstanding"),
				"fieldname": "outstanding_amount",
				"fieldtype": "Currency",
				"width": 120,
			},
			{
				"label": _("Remittance Date"),
				"fieldname": "remittance_date",
				"fieldtype": "Date",
				"width": 130,
			},
			{
				"label": _("Remittance Voucher"),
				"fieldname": "remittance_voucher",
				"fieldtype": "Link",
				"options": "Payment Entry",
				"width": 170,
			},
		]
	else:
		return [
			{
				"label": _("Tax Authority"),
				"fieldname": "party",
				"fieldtype": "Link",
				"options": "Supplier",
				"width": 200,
			},
			{
				"label": _("Period"),
				"fieldname": "period",
				"fieldtype": "Data",
				"width": 90,
			},
			{
				"label": _("Tax Account"),
				"fieldname": "account_head",
				"fieldtype": "Link",
				"options": "Account",
				"width": 200,
			},
			{
				"label": _("Total Collected (Accrual)"),
				"fieldname": "total_collected",
				"fieldtype": "Currency",
				"width": 180,
			},
			{
				"label": _("Customer-Paid Amount"),
				"fieldname": "customer_paid_amount",
				"fieldtype": "Currency",
				"width": 170,
			},
			{
				"label": _("Total Remitted"),
				"fieldname": "total_remitted",
				"fieldtype": "Currency",
				"width": 140,
			},
			{
				"label": _("Total Outstanding"),
				"fieldname": "total_outstanding",
				"fieldtype": "Currency",
				"width": 150,
			},
		]


def get_data(filters):
	if filters.get("show_detail"):
		return get_detail_data(filters)
	return get_summary_data(filters)


def get_detail_data(filters):
	stc = frappe.qb.DocType("Sales Taxes and Charges")
	si = frappe.qb.DocType("Sales Invoice")

	rows = (
		frappe.qb.from_(stc)
		.inner_join(si)
		.on(stc.parent == si.name)
		.select(
			stc.party,
			stc.parent.as_("sales_invoice"),
			si.customer,
			si.posting_date,
			Coalesce(stc.due_date, si.posting_date).as_("due_date"),
			stc.account_head,
			stc.rate,
			stc.tax_amount_after_discount_amount.as_("tax_amount"),
			stc.outstanding_amount,
			stc.name.as_("stc_name"),
			si.outstanding_amount.as_("si_outstanding"),
		)
		.where(si.company == filters.company)
		.where(si.docstatus == 1)
		.where(stc.party.isnotnull())
		.where(stc.party != "")
	)

	if filters.get("to_date"):
		rows = rows.where(si.posting_date <= filters.to_date)
	if filters.get("tax_authority"):
		rows = rows.where(stc.party == filters.tax_authority)
	if filters.get("tax_account"):
		rows = rows.where(stc.account_head == filters.tax_account)

	rows = rows.orderby(stc.party).orderby(si.posting_date).orderby(stc.parent).run(as_dict=True)

	# Fetch remittance totals in one query to avoid N+1
	stc_names = [r.stc_name for r in rows]
	remittance_map = {}
	if stc_names:
		rem_rows = frappe.db.sql(
			"""
			SELECT
				per.reference_name AS stc_name,
				SUM(per.allocated_amount) AS total_allocated,
				MAX(pe.posting_date) AS last_remittance_date,
				(
					SELECT pe2.name
					FROM `tabPayment Entry` pe2
					JOIN `tabPayment Entry Reference` per2 ON per2.parent = pe2.name
					WHERE per2.reference_doctype = 'Sales Taxes and Charges'
					  AND per2.reference_name = per.reference_name
					  AND pe2.docstatus = 1
					ORDER BY pe2.posting_date DESC
					LIMIT 1
				) AS last_voucher
			FROM `tabPayment Entry Reference` per
			JOIN `tabPayment Entry` pe ON per.parent = pe.name
			WHERE per.reference_doctype = 'Sales Taxes and Charges'
			  AND per.reference_name IN %(stc_names)s
			  AND pe.docstatus = 1
			GROUP BY per.reference_name
			""",
			{"stc_names": stc_names},
			as_dict=True,
		)
		for rem in rem_rows:
			remittance_map[rem.stc_name] = rem

	output = []
	for row in rows:
		rem = remittance_map.get(row.stc_name, frappe._dict())
		amount_remitted = flt(rem.get("total_allocated", 0))

		# Remittance status filter
		status = filters.get("remittance_status")
		if status == "Outstanding" and flt(row.outstanding_amount) <= 0:
			continue
		if status == "Remitted" and flt(row.outstanding_amount) > 0:
			continue

		output.append(
			{
				"party": row.party,
				"sales_invoice": row.sales_invoice,
				"customer": row.customer,
				"posting_date": row.posting_date,
				"due_date": row.due_date,
				"account_head": row.account_head,
				"rate": row.rate,
				"tax_amount": row.tax_amount,
				"customer_paid": 1 if flt(row.si_outstanding) == 0.0 else 0,
				"amount_remitted": amount_remitted,
				"outstanding_amount": row.outstanding_amount,
				"remittance_date": rem.get("last_remittance_date"),
				"remittance_voucher": rem.get("last_voucher"),
			}
		)

	return output


def get_summary_data(filters):
	stc = frappe.qb.DocType("Sales Taxes and Charges")
	si = frappe.qb.DocType("Sales Invoice")

	rows = (
		frappe.qb.from_(stc)
		.inner_join(si)
		.on(stc.parent == si.name)
		.select(
			stc.party,
			stc.account_head,
			stc.tax_amount_after_discount_amount.as_("tax_amount"),
			stc.outstanding_amount,
			si.posting_date,
			si.outstanding_amount.as_("si_outstanding"),
		)
		.where(si.company == filters.company)
		.where(si.docstatus == 1)
		.where(stc.party.isnotnull())
		.where(stc.party != "")
	)

	if filters.get("to_date"):
		rows = rows.where(si.posting_date <= filters.to_date)
	if filters.get("tax_authority"):
		rows = rows.where(stc.party == filters.tax_authority)
	if filters.get("tax_account"):
		rows = rows.where(stc.account_head == filters.tax_account)

	rows = rows.run(as_dict=True)

	# Aggregate in Python — grouping by (party, account_head, YYYY-MM)
	buckets = defaultdict(
		lambda: {
			"total_collected": 0.0,
			"customer_paid_amount": 0.0,
			"total_remitted": 0.0,
			"total_outstanding": 0.0,
		}
	)

	for row in rows:
		period = row.posting_date.strftime("%Y-%m") if row.posting_date else ""
		key = (row.party, period, row.account_head)
		b = buckets[key]
		tax = flt(row.tax_amount)
		outstanding = flt(row.outstanding_amount)
		remitted = flt(tax - outstanding)

		b["total_collected"] += tax
		b["total_outstanding"] += outstanding
		b["total_remitted"] += remitted
		if flt(row.si_outstanding) == 0.0:
			b["customer_paid_amount"] += tax

	# Apply remittance status filter and build output
	status = filters.get("remittance_status")
	output = []
	for (party, period, account_head), b in sorted(buckets.items()):
		if status == "Outstanding" and flt(b["total_outstanding"]) <= 0:
			continue
		if status == "Remitted" and flt(b["total_outstanding"]) > 0:
			continue

		output.append(
			{
				"party": party,
				"period": period,
				"account_head": account_head,
				"total_collected": flt(b["total_collected"], 2),
				"customer_paid_amount": flt(b["customer_paid_amount"], 2),
				"total_remitted": flt(b["total_remitted"], 2),
				"total_outstanding": flt(b["total_outstanding"], 2),
			}
		)

	return output
