import json

import frappe
from frappe.www.printview import get_html_and_style as frappe_get_html_and_style, get_print_style
from frappe.printing.page.print.print import (
	get_print_settings_to_show as frappe_get_print_settings_to_show,
)

from check_run.check_run.doctype.check_run.check_run import get_check_run_settings


@frappe.whitelist()
def get_html_and_style(
	doc,
	name=None,
	print_format=None,
	meta=None,
	no_letterhead=None,
	letterhead=None,
	trigger_print=False,
	style=None,
	settings=None,
	templates=None,
):
	if isinstance(doc, str) and isinstance(name, str):
		doc = frappe.get_doc(doc, name)

	if isinstance(doc, str):
		doc = frappe.get_doc(json.loads(doc))
	if doc.doctype == "Check Run":
		return get_check_run_format(
			doc,
			name,
			print_format,
			meta,
			no_letterhead,
			letterhead,
			trigger_print,
			style,
			settings,
			templates,
		)
	return frappe_get_html_and_style(
		doc,
		name,
		print_format,
		meta,
		no_letterhead,
		letterhead,
		trigger_print,
		style,
		settings,
		templates,
	)


def get_check_run_format(
	doc,
	name=None,
	print_format=None,
	meta=None,
	no_letterhead=None,
	letterhead=None,
	trigger_print=False,
	style=None,
	settings=None,
	templates=None,
):
	settings = json.loads(settings) if isinstance(doc, str) else settings
	check_run_settings = get_check_run_settings(doc)
	if not settings:
		settings = {}
		settings["payment_entry_format"] = check_run_settings.print_format
		settings["secondary_print_format"] = check_run_settings.secondary_print_format

	html = doc.render_check_run(pdf=False)
	return {"html": html, "style": get_print_style(style=style)}


@frappe.whitelist()
def get_print_settings_to_show(doctype, docname):
	settings = get_check_run_settings(frappe.get_doc("Check Run", docname))
	if doctype == "Check Run":
		return [
			{
				"fieldname": "payment_entry_format",
				"label": frappe._("Payment Entry Format"),
				"fieldtype": "Link",
				"options": "Print Format",
				"default": settings.print_format,
				"value": settings.print_format,
				# set get_query field with filter for Payment Entry Doctype
			},
			{
				"fieldname": "secondary_print_format",
				"label": frappe._("Secondary Print Format"),
				"fieldtype": "Link",
				"options": "Print Format",
				"default": settings.secondary_print_format,
				"value": settings.secondary_print_format,
			},
		]
	return frappe_get_print_settings_to_show(doctype, docname)
