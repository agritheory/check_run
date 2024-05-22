import json

import frappe
from frappe.www.printview import (
	get_html_and_style as frappe_get_html_and_style,
	get_print_style,
	escape_html,
)
from frappe.www.printview import set_link_titles, get_rendered_template, get_print_format_doc

from check_run.check_run.doctype.check_run.check_run import get_check_run_settings


def get_context(context):
	"""Build context for print"""
	if not ((frappe.form_dict.doctype and frappe.form_dict.name) or frappe.form_dict.doc):
		return {
			"body": f"""
				<h1>Error</h1>
				<p>Parameters doctype and name required</p>
				<pre>{escape_html(frappe.as_json(frappe.form_dict, indent=2))}</pre>
				"""
		}
	if frappe.form_dict.doc:
		doc = frappe.form_dict.doc
	else:
		doc = frappe.get_doc(frappe.form_dict.doctype, frappe.form_dict.name)


@frappe.whitelist()
def get_html_and_style(
	doc,
	name=None,
	doctype_to_print=None,
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
			doctype_to_print,
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
	doctype_to_print=None,
	print_format=None,
	meta=None,
	no_letterhead=None,
	letterhead=None,
	trigger_print=False,
	style=None,
	settings=None,
	templates=None,
):
	check_run_settings = get_check_run_settings(doc)
	if not settings:
		settings = {}
		settings["payment_entry_format"] = check_run_settings.print_format
		settings["secondary_print_format"] = check_run_settings.secondary_print_format

	if doctype_to_print == "Check Run":
		print_format = get_print_format_doc(print_format, meta=meta or frappe.get_meta("Check Run"))
		set_link_titles(doc)
		try:
			html = get_rendered_template(
				doc,
				name=name,
				print_format=print_format,
				meta=meta,
				no_letterhead=no_letterhead,
				letterhead=letterhead,
				trigger_print=trigger_print,
				settings=frappe.parse_json(settings),
			)
		except frappe.TemplateNotFoundError:
			frappe.clear_last_message()
			html = None

		return {"html": html, "style": get_print_style(style=style, print_format=print_format)}

	transaction = json.loads(doc.transactions) if isinstance(doc.transactions, str) else None
	html = []
	pe = []
	for row in transaction:
		pe.append(row.get("payment_entry"))

	payment_entry = list(set(pe))
	for row in payment_entry:
		pe_doc = frappe.get_doc("Payment Entry", row)

		settings = json.loads(settings) if isinstance(doc, str) else settings

		if doctype_to_print == "Payment Entry":
			print_format = (
				check_run_settings.print_format or check_run_settings.secondary_print_format or ""
			)
		if doctype_to_print == "Payment Entry Secondary Format":
			print_format = (
				check_run_settings.secondary_print_format or check_run_settings.print_format or ""
			)

		print_format = get_print_format_doc(print_format, meta=meta or frappe.get_meta("Payment Entry"))

		set_link_titles(pe_doc)

		try:
			html_ = []
			html_.append(
				get_rendered_template(
					pe_doc,
					name=name,
					print_format=print_format,
					meta=meta,
					no_letterhead=no_letterhead,
					letterhead=letterhead,
					trigger_print=trigger_print,
					settings=frappe.parse_json(settings),
				)
			)
			html.append(html_)
		except frappe.TemplateNotFoundError:
			frappe.clear_last_message()
			html = None

	return {"html": html, "style": get_print_style(style=style, print_format=print_format)}
