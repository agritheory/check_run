import json
from pathlib import Path

import frappe


def load_customizations():
	customizations_directory = (
		Path().cwd().parent / "apps" / "check_run" / "check_run" / "check_run" / "custom"
	)
	files = list(customizations_directory.glob("**/*.json"))
	for file in files:
		customizations = json.loads(Path(file).read_text())
		for field in customizations.get("custom_fields"):
			if field.get("module") != "Check Run":
				continue
			existing_field = frappe.get_value("Custom Field", field.get("name"))
			custom_field = (
				frappe.get_doc("Custom Field", field.get("name"))
				if existing_field
				else frappe.new_doc("Custom Field")
			)
			field.pop("modified")
			{custom_field.set(key, value) for key, value in field.items()}
			custom_field.flags.ignore_permissions = True
			custom_field.flags.ignore_version = True
			custom_field.save()
		for prop in customizations.get("property_setters"):
			if prop.get("module") != "Check Run":
				continue
			property_setter = frappe.get_doc(
				{
					"name": prop.get("name"),
					"doctype": "Property Setter",
					"doctype_or_field": prop.get("doctype_or_field"),
					"doc_type": prop.get("doc_type"),
					"field_name": prop.get("field_name"),
					"property": prop.get("property"),
					"value": prop.get("value"),
					"property_type": prop.get("property_type"),
				}
			)
			property_setter.flags.ignore_permissions = True
			property_setter.insert()


def add_workflow_for_voided_check():

	workflow_actions = [
		{
			"docstatus": 0,
			"doctype": "Workflow Action Master",
			"name": "Submit",
			"workflow_action_name": "Submit",
		},
		{
			"docstatus": 0,
			"doctype": "Workflow Action Master",
			"name": "Void",
			"workflow_action_name": "Void",
		},
		{
			"docstatus": 0,
			"doctype": "Workflow Action Master",
			"name": "Cancel",
			"workflow_action_name": "Cancel",
		},
		{
			"docstatus": 0,
			"doctype": "Workflow Action Master",
			"name": "Save",
			"workflow_action_name": "Save",
		},
	]

	for action in workflow_actions:
		if not frappe.db.exists("Workflow Action Master", action["name"]):
			act = frappe.new_doc("Workflow Action Master")
			act.update(action)
			act.insert()

	workflow_states = [
		{
			"docstatus": 0,
			"icon": "",
			"name": "Submitted",
			"style": "Primary",
			"workflow_state_name": "Submitted",
		},
		{
			"docstatus": 0,
			"icon": "",
			"name": "Voided",
			"style": "Inverse",
			"workflow_state_name": "Voided",
		},
		{
			"docstatus": 0,
			"doctype": "Workflow State",
			"icon": "",
			"name": "Cancelled",
			"style": "Inverse",
			"workflow_state_name": "Cancelled",
		},
		{
			"docstatus": 0,
			"doctype": "Workflow State",
			"icon": "",
			"name": "Draft",
			"style": "Warning",
			"workflow_state_name": "Draft",
		},
	]

	for state in workflow_states:
		if not frappe.db.exists("Workflow State", state["name"]):
			ws = frappe.new_doc("Workflow State")
			ws.update(state)
			ws.insert()

	workflow_data = {
		"docstatus": 0,
		"doctype": "Workflow",
		"document_type": "Payment Entry",
		"is_active": 0,
		"name": "Void Payment Entry",
		"override_status": 0,
		"send_email_alert": 0,
		"states": [
			{
				"allow_edit": "Accounts User",
				"doc_status": "0",
				"is_optional_state": 0,
				"parent": "Payment Entry",
				"parentfield": "states",
				"parenttype": "Workflow",
				"state": "Draft",
			},
			{
				"allow_edit": "Accounts User",
				"doc_status": "1",
				"is_optional_state": 0,
				"parent": "Payment Entry",
				"parentfield": "states",
				"parenttype": "Workflow",
				"state": "Submitted",
			},
			{
				"allow_edit": "Accounts User",
				"doc_status": "2",
				"is_optional_state": 0,
				"parent": "Payment Entry",
				"parentfield": "states",
				"parenttype": "Workflow",
				"state": "Cancelled",
			},
			{
				"allow_edit": "Accounts User",
				"doc_status": "2",
				"is_optional_state": 0,
				"parent": "Payment Entry",
				"parentfield": "states",
				"parenttype": "Workflow",
				"state": "Voided",
				"update_field": "status",
				"update_value": "Voided",
			},
		],
		"transitions": [
			{
				"action": "Save",
				"allow_self_approval": 1,
				"allowed": "Accounts User",
				"next_state": "Draft",
				"parent": "Payment Entry",
				"parentfield": "transitions",
				"parenttype": "Workflow",
				"state": "Draft",
			},
			{
				"action": "Submit",
				"allow_self_approval": 1,
				"allowed": "Accounts User",
				"next_state": "Submitted",
				"parent": "Payment Entry",
				"parentfield": "transitions",
				"parenttype": "Workflow",
				"state": "Draft",
			},
			{
				"action": "Cancel",
				"allow_self_approval": 1,
				"allowed": "Accounts User",
				"next_state": "Cancelled",
				"parent": "Payment Entry",
				"parentfield": "transitions",
				"parenttype": "Workflow",
				"state": "Submitted",
			},
			{
				"action": "Void",
				"allow_self_approval": 1,
				"allowed": "Accounts User",
				"next_state": "Voided",
				"parent": "Payment Entry",
				"parentfield": "transitions",
				"parenttype": "Workflow",
				"state": "Submitted",
			},
		],
		"workflow_name": "Voidable Payment Entry",
		"workflow_state_field": "status",
	}
	if not frappe.db.exists("Workflow", workflow_data["workflow_name"]):
		workflow = frappe.new_doc("Workflow")
		workflow.update(workflow_data)
		workflow.insert()


def after_install():
	if not frappe.db.exists("File", "Home/Check Run"):
		try:
			cr_folder = frappe.new_doc("File")
			cr_folder.update({"file_name": "Check Run", "is_folder": True, "folder": "Home"})
			cr_folder.save()
		except Exception as e:
			pass

	add_workflow_for_voided_check()
