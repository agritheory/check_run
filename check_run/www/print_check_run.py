import json

import frappe
from frappe.www.printview import (
	get_html_and_style as frappe_get_html_and_style,
	get_print_style,
	escape_html,
)


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
