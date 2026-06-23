# Copyright (c) 2026, AgriTheory and contributors
# For license information, please see license.txt

import datetime

import frappe

from check_run.check_run.doctype.check_run.check_run import (
	check_for_draft_check_run,
	get_check_run_settings,
	get_entries,
)

COMPANY = "Chelsea Fruit Co"
TAX_PAYABLE_ACCOUNT = "2320 - Sales Tax Payable - CFC"
year = datetime.date.today().year


def tax_payable_check_run_entries(
	include_tax_payable=1,
	include_journal_entries=0,
	include_purchase_invoices=0,
	include_expense_claims=0,
	end_date=None,
):
	end_date = end_date or datetime.date(year, 12, 31)
	cr_name = check_for_draft_check_run(
		company=COMPANY,
		bank_account="Primary Checking - Local Bank",
		payable_account=TAX_PAYABLE_ACCOUNT,
	)
	cr = frappe.get_doc("Check Run", cr_name)
	cr.flags.in_test = True
	cr.posting_date = cr.end_date = end_date
	cr.set_last_check_number()
	cr.save()
	crs = get_check_run_settings(cr)
	crs.include_tax_payable = include_tax_payable
	crs.include_journal_entries = include_journal_entries
	crs.include_purchase_invoices = include_purchase_invoices
	crs.include_expense_claims = include_expense_claims
	crs.tax_payable = "Check"
	crs.number_of_invoices_per_voucher = 100
	crs.save()
	return cr, get_entries(cr).get("transactions") or []


def process_tax_payable_check_run_for_rows(tax_row_names, end_date=None):
	end_date = end_date or datetime.date(year, 12, 31)
	cr_name = check_for_draft_check_run(
		company=COMPANY,
		bank_account="Primary Checking - Local Bank",
		payable_account=TAX_PAYABLE_ACCOUNT,
	)
	cr = frappe.get_doc("Check Run", cr_name)
	cr.flags.in_test = True
	cr.posting_date = cr.end_date = end_date
	cr.set_last_check_number()
	cr.set_default_payable_account()
	cr.save()
	crs = get_check_run_settings(cr)
	crs.include_tax_payable = 1
	crs.include_purchase_invoices = 0
	crs.include_journal_entries = 0
	crs.include_expense_claims = 0
	crs.tax_payable = "Check"
	crs.number_of_invoices_per_voucher = 100
	crs.save()
	tax_row_names = set(tax_row_names)
	entries = get_entries(cr)
	for row in entries.get("transactions"):
		row["pay"] = row.get("name") in tax_row_names
	cr.transactions = frappe.as_json(entries.get("transactions"))
	cr.save()
	cr.process_check_run()
	return cr
