# Copyright (c) 2022, AgriTheory and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import json
from itertools import groupby, zip_longest
from io import StringIO

from PyPDF2 import PdfFileWriter

import frappe
from frappe.model.document import Document
from frappe.utils.data import flt
from frappe.utils.data import date_diff, add_days, nowdate, getdate, now, get_datetime
from frappe.utils.print_format import read_multi_pdf

from erpnext.accounts.utils import get_balance_on
from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import get_dimensions


class CheckRun(Document):
	def validate(self):
		self.set_status()
		gl_account = frappe.get_value('Bank Account', self.bank_account, 'account')
		if not gl_account:
			frappe.throw(frappe._("This Bank Account is not associated with a General Ledger Account."))
		self.beg_balance = get_balance_on(gl_account, self.check_run_date)
		if self.flags.in_insert:
			if self.initial_check_number is None:
				self.get_last_check_number()
				self.get_default_payable_account()
				self.set_default_dates()
		else:
			self.validate_last_check_number()

	def set_status(self, status=None):
		if status:
			self.status = status
		elif self.status == 'Confirm Print':
			pass
		elif self.docstatus == 0:
			self.status = 'Draft'
		elif self.docstatus == 1 and self.print_count > 0:
			self.status = 'Printed'
		elif self.docstatus == 1:
			self.status = 'Submitted'

	def get_last_check_number(self):
		if self.ach_only().ach_only:
			return
		check_number = frappe.get_value('Bank Account', self.bank_account, "check_number")
		self.initial_check_number = int(check_number or 0) + 1

	def get_default_payable_account(self):
		self.pay_to_account = frappe.get_value('Company', self.company, "default_payable_account")

	def set_default_dates(self):
		if not self.check_run_date:
			self.check_run_date = getdate()
			self.start_date = add_days(getdate(), -(getdate().weekday()) -1)
			self.end_date = add_days(self.start_date, 6)

	@frappe.whitelist()
	def validate_last_check_number(self, check_number=None):
		if self.ach_only().ach_only:
			return
		check_number = check_number if check_number else (self.initial_check_number or 0)
		account_check_number = frappe.get_value('Bank Account', self.bank_account, "check_number") or 0
		if int(check_number) < int(account_check_number):
			frappe.throw(f'Initial Check Number cannot be lower than the last used check number <b>{account_check_number}</b> for <b>{self.bank_account}</b>')

	@frappe.whitelist()
	def before_submit(self):
		self.payment_entries = []
		self.dt_pes = []
		transactions = self.transactions
		transactions = json.loads(transactions)
		if len(transactions) < 1:
			frappe.throw("You must select at least one Invoice to pay.")
		transactions = sorted([frappe._dict(item) for item in transactions if item.get("pay")], key=lambda x: x.party)
		_transactions = self.create_payment_entries(transactions)
		self.print_count = 0
		self.transactions = json.dumps(_transactions)
		if self.ach_only().ach_only:
			self.initial_check_number = ""
			self.final_check_number = ""
		else:
			self.final_check_number = _transactions[-1].check_number
			frappe.db.set_value('Bank Account', self.bank_account, 'check_number', self.final_check_number)
		return self

	@frappe.whitelist()
	def ach_only(self):
		transactions = json.loads(self.transactions) if self.transactions else []
		ach_only = frappe._dict({'ach_only': True, 'print_checks_only': True})
		if not self.transactions:
			ach_only.ach_only = False
			ach_only.print_checks_only = False
			return ach_only
		if any([t.get('mode_of_payment') == 'Check' for t in transactions]):
			ach_only.ach_only = False
		if any([t.get('mode_of_payment') in ('ACH/EFT', 'ECheck') for t in transactions]):
			ach_only.print_checks_only = False
		return ach_only

	def create_payment_entries(self, transactions):
		check_count = 0
		_transactions = []
		gl_account = frappe.get_value('Bank Account', self.bank_account, 'account')
		for party_ref, _group in groupby(transactions, key=lambda x: x.party_ref):
			_group = list(_group)
			# split checks in groups of 5 if first reference is a check
			groups = list(zip_longest(*[iter(_group)] * 5)) if _group[0].mode_of_payment == 'Check' else [_group]
			if not groups:
				continue
			for group in groups:
				_references = []
				pe = frappe.new_doc("Payment Entry")
				pe.payment_type = "Pay"
				pe.posting_date = nowdate()
				pe.mode_of_payment = group[0].mode_of_payment
				pe.company = self.company
				pe.paid_from = gl_account
				pe.paid_to = self.pay_to_account
				pe.paid_to_account_currency = frappe.db.get_value("Account", self.bank_account, "account_currency")
				pe.paid_from_account_currency = pe.paid_to_account_currency
				pe.reference_date = self.check_run_date
				pe.party = party_ref
				pe.party_type = 'Supplier' if group[0].doctype == 'Purchase Invoice' else 'Employee'
				pe.check_run = self.name
				total_amount = 0
				if pe.mode_of_payment == 'Check':
					pe.reference_no = int(self.initial_check_number) + check_count
					check_count += 1
				else:
					pe.reference_no = self.name
				
				for reference in group:
					if not reference:
						continue
					pe.append('references', {
							"reference_doctype": reference.doctype,
							"reference_name": reference.name or reference.ref_number,
							"due_date": reference.get("due_date"),
							"outstanding_amount": flt(reference.outstanding_amount),
							"allocated_amount": flt(reference.outstanding_amount),
							"total_amount": flt(reference.outstanding_amount),
					})
					total_amount += reference.outstanding_amount
					reference.check_number = pe.reference_no
					_references.append(reference)
				pe.received_amount = total_amount
				pe.base_received_amount = total_amount
				pe.paid_amount = total_amount
				pe.base_paid_amount = total_amount
				pe.save()
				pe.submit()
				for reference in _references:
					reference.payment_entry = pe.name
					_transactions.append(reference)
		return _transactions


	def get_dimensions_from_references(self, references, dimension):
		dimensions, default_dimensions = get_dimensions(with_cost_center_and_project=True)
		parents = [reference.get('name') for reference in references if reference]
		purchase_invoice_items = frappe.get_all('Purchase Invoice Item', {'parent': ['in', parents]})
		expense_claim_details = frappe.get_all('Expense Claim Detail', {'parent': ['in', parents]})
		children = purchase_invoice_items + expense_claim_details
		return mode_dimensions(children, dimension)


	@frappe.whitelist()
	def increment_print_count(self):
		self.print_count = self.print_count + 1
		self.set_status('Confirm Print')
		self.save()
		return


@frappe.whitelist()
def print_checks(docname, reprint_check_number=None):
	doc = frappe.get_doc('Check Run', docname)
	initial_check_number = int(doc.initial_check_number)
	if reprint_check_number != 'undefined':
		doc.initial_check_number = int(reprint_check_number)
	output = PdfFileWriter()
	transactions = json.loads(doc.transactions)
	check_increment = 0
	_transactions = []
	for pe, group in groupby(transactions, key=lambda x: x['payment_entry']):
		group = list(group)
		if frappe.db.get_value('Payment Entry', pe, 'docstatus') == 1:
			output = frappe.get_print(
				'Payment Entry',
				pe,
				frappe.get_meta('Payment Entry').default_print_format,
				as_pdf=True,
				output=output,
				no_letterhead=0,
			)
		if initial_check_number != reprint_check_number:
			frappe.db.set_value('Payment Entry', pe, 'reference_no', doc.initial_check_number + check_increment)
			for ref in group:
				ref['check_number'] = doc.initial_check_number + check_increment
				_transactions.append(ref)
		check_increment += 1
	if _transactions:
		frappe.db.set_value('Check Run', doc.name, 'transactions', json.dumps(_transactions))
		frappe.db.set_value('Check Run', doc.name, 'initial_check_number', doc.initial_check_number)
		frappe.db.set_value('Check Run', doc.name, 'final_check_number', doc.initial_check_number + check_increment -1)
		frappe.db.set_value('Bank Account', doc.bank_account, 'check_number', doc.final_check_number)

	frappe.local.response.filename = f'{docname.replace(" ", "-").replace("/", "-")}.pdf'
	frappe.local.response.filecontent = read_multi_pdf(output)
	frappe.local.response.type = "download"
	comment = frappe.new_doc('Comment')
	comment.owner = "Administrator"
	comment.comment_type = 'Info'
	comment.reference_doctype = 'Check Run'
	comment.reference_name = doc.name
	comment.published = 1
	comment.content = f"{frappe.session.user} printed checks starting with {doc.initial_check_number} on {now()}"
	comment.save()
	frappe.db.commit()


@frappe.whitelist()
def check_for_draft_check_run(company, bank_account, payable_account):
	existing = frappe.get_value(
		'Check Run', {
			'company': company,
			'bank_account': bank_account,
			'pay_to_account': payable_account,
			'status': ['in', ['Draft', 'Submitted']],
			'initial_check_number': ['!=', 0]
		}
	)
	if existing:
		return existing
	cr = frappe.new_doc('Check Run')
	cr.company = company
	cr.bank_account = bank_account
	cr.pay_to_account = payable_account
	cr.save()
	return cr.name


@frappe.whitelist()
def confirm_print(docname):
	return frappe.db.set_value('Check Run', docname, 'status', 'Printed')


@frappe.whitelist()
def get_entries(doc):
	doc = frappe._dict(json.loads(doc)) if isinstance(doc, str) else doc
	modes_of_payment = frappe.get_all('Mode of Payment', order_by='name')
	if frappe.db.exists('Check Run', doc.name):
		db_doc = frappe.get_doc('Check Run', doc.name)
		if db_doc.transactions and json.loads(db_doc.transactions):
			return {'transactions': json.loads(db_doc.transactions), 'modes_of_payment': modes_of_payment}
	transactions =  frappe.db.sql("""
	(
		SELECT
			'Purchase Invoice' as doctype,
			'Supplier' AS party_type,
			`tabPurchase Invoice`.name,
			`tabPurchase Invoice`.bill_no AS ref_number,
			`tabPurchase Invoice`.supplier_name AS party,
			`tabPurchase Invoice`.supplier AS party_ref,
			`tabPurchase Invoice`.outstanding_amount AS amount,
			`tabPurchase Invoice`.due_date,
			`tabPurchase Invoice`.posting_date,
			COALESCE(`tabPurchase Invoice`.supplier_default_mode_of_payment, `tabSupplier`.supplier_default_mode_of_payment, '\n') AS mode_of_payment
		FROM `tabPurchase Invoice`, `tabSupplier`
		WHERE `tabPurchase Invoice`.outstanding_amount > 0
		AND `tabPurchase Invoice`.supplier = `tabSupplier`.name
		AND `tabPurchase Invoice`.company = %(company)s
		AND `tabPurchase Invoice`.docstatus = 1
		AND `tabPurchase Invoice`.credit_to = %(pay_to_account)s
		AND `tabPurchase Invoice`.status != 'On Hold'
	)
	UNION
	(
		SELECT
			'Expense Claim' as doctype,
			'Employee' AS party_type,
			`tabExpense Claim`.name,
			`tabExpense Claim`.name AS ref_number,
			`tabExpense Claim`.employee_name AS party,
			`tabExpense Claim`.employee AS party_ref,
			`tabExpense Claim`.grand_total AS amount,
			`tabExpense Claim`.posting_date AS due_date,
			`tabExpense Claim`.posting_date,
			COALESCE(`tabExpense Claim`.mode_of_payment, `tabEmployee`.mode_of_payment, '\n') AS mode_of_payment
		FROM `tabExpense Claim`, `tabEmployee`
		WHERE `tabExpense Claim`.grand_total > `tabExpense Claim`.total_amount_reimbursed
		AND `tabExpense Claim`.employee = `tabEmployee`.name
		AND `tabExpense Claim`.company = %(company)s
		AND `tabExpense Claim`.docstatus = 1
		AND `tabExpense Claim`.payable_account = %(pay_to_account)s
	)
	UNION (
		SELECT
			'Journal Entry' AS doctype,
			`tabJournal Entry`.name,
			`tabJournal Entry`.name AS ref_number,
			`tabJournal Entry Account`.party AS party,
			`tabJournal Entry Account`.party AS party_ref,
			`tabJournal Entry Account`.party_type,
			`tabJournal Entry Account`.credit_in_account_currency AS amount,
			`tabJournal Entry`.due_date AS due_date,
			`tabJournal Entry`.posting_date,
			COALESCE(`tabJournal Entry`.mode_of_payment, '\n') AS mode_of_payment
		FROM `tabJournal Entry`, `tabJournal Entry Account`
		WHERE `tabJournal Entry`.name = `tabJournal Entry Account`.parent
		AND `tabJournal Entry`.company = %(company)s
		AND `tabJournal Entry`.docstatus = 1
		AND `tabJournal Entry Account`.account = %(pay_to_account)s
		AND `tabJournal Entry`.name NOT in (
			SELECT `tabPayment Entry Reference`.reference_name
			FROM `tabPayment Entry`, `tabPayment Entry Reference`
			WHERE `tabPayment Entry Reference`.parent = `tabPayment Entry`.name
			AND `tabPayment Entry Reference`.reference_doctype = 'Journal Entry'
			AND `tabPayment Entry`.docstatus = 1
		)
	)
	ORDER BY due_date
	""", {
		'company': doc.company, 'pay_to_account': doc.pay_to_account
	}, as_dict=True)
	return {'transactions': transactions, 'modes_of_payment': modes_of_payment}


@frappe.whitelist()
def get_balance(doc):
	doc = frappe._dict(json.loads(doc)) if isinstance(doc, str) else doc
	if not doc.bank_account or not doc.check_run_date:
		return
	gl_account = frappe.get_value('Bank Account', doc.bank_account, 'account')
	return get_balance_on(gl_account, doc.check_run_date)


def mode_dimensions_from_doc_items(doc, dimension='cost_center'):
	return mode_dimensions(doc.items, dimension)

def mode_dimensions(data, dimension='cost_center'):
	dimensions = frappe._dict()
	for row in data:
		if row.get(dimension) in dimensions:
			if not row.get('amount'):
				amount = frappe.get_value("Item", row.get('item_code'), 'last_purchase_rate') or 0
			dimensions[row.get(dimension, 'None')] += row.get('amount') if row.get('amount') else amount
		else:
			if not row.get('amount'):
				amount = frappe.get_value("Item", row.get('item_code'), 'last_purchase_rate') or 0
			dimensions[row.get(dimension, 'None')] = row.get('amount') if row.get('amount') else amount
	if not dimensions:
		return
	try:
		return max(dimensions)
	except TypeError:
		return
