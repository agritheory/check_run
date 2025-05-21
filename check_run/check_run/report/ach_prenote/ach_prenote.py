# Copyright (c) 2025, AgriTheory and contributors
# For license information, please see license.txt

import json
from io import StringIO
from frappe.utils.password import get_decrypted_password

import frappe
from frappe.utils.data import getdate, flt, get_datetime
from frappe.query_builder.custom import ConstantColumn
from frappe.query_builder.functions import Coalesce
from frappe.permissions import has_permission

from atnacha import ACHEntry, ACHBatch, NACHAFile

from check_run.check_run.doctype.check_run_settings.check_run_settings import CheckRunSettings


def execute(filters=None):
	return get_columns(filters), get_data(filters)


def get_columns(filters):
	return [
		{
			"label": frappe._("Party Type"),
			"fieldname": "party_type",
			"fieldtype": "Data",
			"width": "150px",
		},
		{
			"label": frappe._("Party"),
			"fieldname": "party",
			"fieldtype": "Data",
			"width": "300px",
			"hidden": True,
		},
		{
			"label": frappe._("Party Name"),
			"fieldname": "party_name",
			"fieldtype": "Data",
			"width": "300px",
		},
		{
			"label": frappe._("Bank"),
			"fieldname": "bank",
			"fieldtype": "Link",
			"width": "200px",
			"options": "Bank",
		},
		{
			"label": frappe._("Account Type"),
			"fieldname": "ach_account_type",
			"fieldtype": "Data",
			"width": "150px",
		},
		{
			"label": frappe._("ACH Prenote Date"),
			"fieldname": "ach_prenote_date",
			"fieldtype": "Date",
			"width": "150px",
		},
		{
			"label": frappe._("Last Used Date"),
			"fieldname": "ach_last_used",
			"fieldtype": "Date",
			"width": "150px",
		},
		{
			"label": frappe._("Validated Date"),
			"fieldname": "account_details_validated",
			"fieldtype": "Date",
			"width": "200px",
			"editable": True,
		},
	]


def get_data(filters):
	Supplier = frappe.qb.DocType("Supplier")
	Employee = frappe.qb.DocType("Employee")
	supplier_query = (
		frappe.qb.from_(Supplier)
		.select(
			Supplier.ach_last_used,
			Supplier.account_details_validated,
			Supplier.bank,
			Supplier.ach_account_type,
			Supplier.ach_prenote_date,
			(Supplier.supplier_name).as_("party_name"),
			(Supplier.name).as_("party"),
			ConstantColumn("Supplier").as_("party_type"),
		)
		.where(Supplier.bank.isnotnull())
		.where(Coalesce(Supplier.ach_last_used, "1900-1-1") <= getdate(filters.last_used_date))
		.where(
			Coalesce(Supplier.account_details_validated, "1900-1-1") <= getdate(filters.validated_date)
		)
		.orderby(
			Supplier.ach_last_used,
			Supplier.account_details_validated,
		)
	)
	if filters.ach_account_type == "Checking":
		supplier_query = supplier_query.where(Supplier.ach_account_type == "Checking")
	elif filters.ach_account_type == "Savings":
		supplier_query = supplier_query.where(Supplier.ach_account_type == "Savings")
	suppliers = supplier_query.run(as_dict=True)
	employee_query = (
		frappe.qb.from_(Employee)
		.select(
			Employee.ach_last_used,
			Employee.account_details_validated,
			Employee.bank,
			Employee.ach_account_type,
			Employee.ach_prenote_date,
			(Employee.employee_name).as_("party_name"),
			(Employee.name).as_("party"),
			ConstantColumn("Employee").as_("party_type"),
		)
		.where(Employee.bank.isnotnull())
		.where(Coalesce(Employee.ach_last_used, "1900-1-1") <= getdate(filters.last_used_date))
		.where(
			Coalesce(Employee.account_details_validated, "1900-1-1") <= getdate(filters.validated_date)
		)
		.orderby(
			Employee.ach_last_used,
			Employee.account_details_validated,
		)
	)
	if filters.ach_account_type == "Checking":
		employee_query = employee_query.where(Employee.ach_account_type == "Checking")
	elif filters.ach_account_type == "Savings":
		employee_query = employee_query.where(Employee.ach_account_type == "Savings")
	employees = employee_query.run(as_dict=True)

	results = sorted(
		suppliers + employees,
		key=lambda x: tuple(
			[
				min(
					x.get("account_details_validated") or getdate("1900-1-1"),
					x.get("ach_last_used") or getdate("1900-1-1"),
				),
				x.get("party_name"),
			]
		),
	)
	return results


@frappe.whitelist()
def update_validated_dates(data):
	data = json.loads(data) if isinstance(data, str) else data
	for row in data:
		frappe.db.set_value(
			row.get("party_type"),
			row.get("party"),
			"account_details_validated",
			getdate(row.get("account_details_validated")),
		)


def build_nacha_file(ach_amount, date, data, settings: CheckRunSettings) -> NACHAFile:
	ach_entries = []
	company_bank = frappe.db.get_value("Bank Account", settings.bank_account, "bank")
	company_bank_aba_number = frappe.db.get_value("Bank", company_bank, "aba_number")
	company_ach_id = frappe.db.get_value("Bank Account", settings.bank_account, "company_ach_id")

	for row in data:
		row = frappe._dict(row)
		party_bank_account = get_decrypted_password(
			row.party_type, row.party, fieldname="bank_account", raise_exception=False
		)
		party_bank = frappe.db.get_value(row.party_type, row.party, "bank")
		party_bank_routing_number = frappe.db.get_value("Bank", party_bank, "aba_number")
		print(row.party_type, row.party, "ach_prenote_date", getdate())
		frappe.db.set_value(str(row.party_type), str(row.party), "ach_prenote_date", str(getdate()))
		ach_entry = ACHEntry(
			transaction_code=23,  # checking prenote
			receiving_dfi_identification=party_bank_routing_number,
			dfi_account_number=party_bank_account,
			amount=int(ach_amount * 100),
			individual_id_number="",
			individual_name=row.party_name,
			discretionary_data="",
			addenda_record_indicator=0,
		)
		ach_entries.append(ach_entry)

	company_discretionary_data = settings.get("company_discretionary_data") or ""
	ach_description = settings.get("ach_description") or ""
	batch = ACHBatch(
		service_class_code=settings.ach_service_class_code,
		company_name=settings.company,
		company_discretionary_data=company_discretionary_data[:20],
		company_id=company_ach_id,
		standard_class_code=settings.ach_standard_class_code,
		company_entry_description=ach_description[:10] or "",
		company_descriptive_date=None,
		effective_entry_date=date,
		settlement_date=None,
		originator_status_code=1,
		originating_dfi_id=company_bank_aba_number,
		entries=ach_entries,
	)
	nacha_file = NACHAFile(
		priority_code=1,
		immediate_destination=company_bank_aba_number,
		immediate_origin=settings.immediate_origin or "",
		file_creation_date=getdate(),
		file_creation_time=get_datetime(),
		file_id_modifier="0",
		blocking_factor=10,
		format_code=1,
		immediate_destination_name=company_bank,
		immediate_origin_name=settings.company,
		reference_code="",
		batches=[batch],
	)
	return nacha_file


@frappe.whitelist()
def prepare_ach_prenote(check_run_settings, ach_amount, date, data):
	try:
		data = json.loads(data) if isinstance(data, str) else data
		errors = []
		if not data or len(data) == 0:
			errors.append("No data found to generate ACH prenote")

		if errors:
			return {"success": False, "errors": errors}

		request_id = frappe.generate_hash(length=16)
		frappe.cache().set_value(
			f"ach_prenote_data_{request_id}",
			{
				"check_run_settings": check_run_settings,
				"ach_amount": ach_amount,
				"date": date,
				"data": data,
			},
			expires_in_sec=300,  # Cache for 5 minutes
		)

		return {"success": True, "request_id": request_id}
	except Exception as e:
		frappe.log_error(f"Error preparing ACH prenote: {str(e)}", "ACH Prenote Generation")
		return {"success": False, "errors": [str(e)]}


@frappe.whitelist()
def download_ach_prenote():
	try:
		check_run_settings = frappe.form_dict.get("check_run_settings")
		ach_amount = frappe.form_dict.get("ach_amount")
		date = frappe.form_dict.get("date")
		request_id = frappe.form_dict.get("request_id")

		if request_id:
			cached_data = frappe.cache().get_value(f"ach_prenote_data_{request_id}")
			if cached_data:
				check_run_settings = cached_data.get("check_run_settings")
				ach_amount = cached_data.get("ach_amount")
				date = cached_data.get("date")
				data = cached_data.get("data")
		else:
			frappe.throw("Download session expired. Please try again.")

		date = getdate(date)
		ach_amount = flt(ach_amount, 2)

		has_permission(
			"Payment Entry", ptype="print", verbose=False, user=frappe.session.user, raise_exception=True
		)

		settings = frappe.get_doc("Check Run Settings", check_run_settings)
		ach_file = build_nacha_file(ach_amount, date, data, settings)
		ach_file = ach_file()
		ach_file = StringIO(ach_file)
		ach_file.seek(0)
		file_ext = settings.ach_file_extension if settings and settings.ach_file_extension else "ach"

		frappe.response["filename"] = f"ach_prenote.{file_ext}"
		frappe.response["filecontent"] = ach_file.read()
		frappe.response["type"] = "download"
		frappe.response["content_type"] = "text/plain"

		if request_id:
			frappe.cache().delete_key(f"ach_prenote_data_{request_id}")
		frappe.db.commit()
	except Exception as e:
		frappe.log_error(f"Error generating ACH prenote file: {str(e)}", "ACH Prenote Generation")
		frappe.throw(str(e))
