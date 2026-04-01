# Copyright (c) 2022, AgriTheory and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CheckRunSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		ach_description: DF.Data | None
		ach_file_extension: DF.Data | None
		ach_service_class_code: DF.Literal["200", "220", "225"]
		ach_standard_class_code: DF.Literal["PPD"]
		allow_cancellation: DF.Check
		allow_only_verified_accounts_in_nacha_generation: DF.Check
		allow_stand_alone_debit_notes: DF.Literal["Yes", "No"]
		approver_role: DF.Link | None
		attach_positive_pay: DF.Check
		automatically_release_on_hold_invoices: DF.Check
		bank_account: DF.Link
		cascade_cancellation: DF.Check
		company: DF.Link
		company_discretionary_data: DF.Data | None
		csv_delimiter: DF.Data | None
		csv_quoting: DF.Literal["Minimal", "All", "Non-numeric", "None"]
		custom_post_processing_hook: DF.Data | None
		expense_claim: DF.Link | None
		file_preview_threshold: DF.Int
		immediate_origin: DF.Data | None
		include_expense_claims: DF.Check
		include_journal_entries: DF.Check
		include_purchase_invoices: DF.Check
		include_tax_payable: DF.Check
		journal_entry: DF.Link | None
		number_of_invoices_per_voucher: DF.Int
		pay_to_account: DF.Link
		payment_discount_account: DF.Link | None
		positive_pay_file_format: DF.Literal["CSV", "Excel"]
		pre_check_overdue_items: DF.Check
		print_format: DF.Link | None
		purchase_invoice: DF.Link | None
		role_allowed_to_download_ach_file_multiple_times: DF.Link | None
		set_payment_entry_posting_date: DF.Literal["Use Today's Date", "Use Check Run's Posting Date"]
		show_due_date: DF.Literal["Show Due Date", "Show Days Past Due"]
		split_by_address: DF.Check
		tax_payable: DF.Link | None
		validate_unique_check_number: DF.Check

	# end: auto-generated types

	pass


@frappe.whitelist()
def create(company: str, bank_account: str, pay_to_account: str) -> str:
	crs = frappe.new_doc("Check Run Settings")
	crs.company = company
	crs.bank_account = bank_account
	crs.pay_to_account = pay_to_account
	crs.save()
	return crs
