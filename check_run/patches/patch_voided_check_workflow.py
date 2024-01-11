import frappe
from check_run.customize import add_workflow_for_voided_check


def execute():
	add_workflow_for_voided_check()