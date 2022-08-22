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
from frappe.permissions import has_permission
from frappe.utils.file_manager import save_file, download_file
from frappe.utils.password import get_decrypted_password

from erpnext.accounts.utils import get_balance_on
from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import get_dimensions


from atnacha import ACHEntry, ACHBatch, NACHAFile

class CheckRun(Document):
	def onload(self):
		settings = get_check_run_settings(self)
		if not settings:
			self.set_onload('settings_missing', True)

	def validate(self):
		self.set_status()
		gl_account = frappe.get_value('Bank Account', self.bank_account, 'account')
		if not gl_account:
			frappe.throw(frappe._("This Bank Account is not associated with a General Ledger Account."))
		self.beg_balance = get_balance_on(gl_account, self.posting_date)
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
		if not self.posting_date:
			self.posting_date = getdate()
		if not self.end_date:
			self.end_date = getdate()

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
			frappe.db.set_value('Bank Account', self.bank_account, 'check_number', self.final_check_number)
		return self

	def build_nacha_file(self, settings=None):
		electronic_mop = frappe.get_all('Mode of Payment', {'type': 'Electronic', 'enabled': 1}, 'name', pluck="name")
		ach_payment_entries = list(set(
			[e.get('payment_entry') for e in json.loads(self.transactions) if e.get('mode_of_payment') in electronic_mop]
		))
		payment_entries = [frappe.get_doc('Payment Entry', pe) for pe in ach_payment_entries]
		nacha_file = build_nacha_file_from_payment_entries(self, payment_entries, settings)
		ach_file = StringIO(nacha_file())
		ach_file.seek(0)
		return ach_file


	@frappe.whitelist()
	def ach_only(self):
		transactions = json.loads(self.transactions) if self.transactions else []
		ach_only = frappe._dict({'ach_only': True, 'print_checks_only': True})
		if not self.transactions:
			ach_only.ach_only = False
			ach_only.print_checks_only = False
			return ach_only
		eft_mapping = {mop.name: mop.type for mop in frappe.get_all("Mode of Payment", {'enabled': True}, ['name', 'type'])}
		if any([eft_mapping.get(t.get('mode_of_payment')) == 'Bank' for t in transactions]):
			ach_only.ach_only = False
		if any([eft_mapping.get(t.get('mode_of_payment')) == 'Electronic' for t in transactions]):
			ach_only.print_checks_only = False
		return ach_only

	def create_payment_entries(self, transactions):
		settings = get_check_run_settings(self)
		split = 5
		if settings and settings.number_of_invoices_per_voucher:
			split = settings.number_of_invoices_per_voucher
		check_count = 0
		_transactions = []
		gl_account = frappe.get_value('Bank Account', self.bank_account, 'account')
		for party, _group in groupby(transactions, key=lambda x: x.party):
			_group = list(_group)
			if frappe.db.get_value('Mode of Payment', _group[0].mode_of_payment, 'type') == 'Bank':
				groups = list(zip_longest(*[iter(_group)] * split)) 
			else:
				groups = [_group]
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
				pe.reference_date = self.posting_date
				pe.party_type = group[0].party_type
				pe.party = group[0].party
				pe.check_run = self.name
				total_amount = 0
				if frappe.db.get_value('Mode of Payment', _group[0].mode_of_payment, 'type') == 'Bank':
					pe.reference_no = int(self.initial_check_number) + check_count
					check_count += 1
					self.final_check_number = pe.reference_no
				else:
					pe.reference_no = frappe._(f"via {_group[0].mode_of_payment} {self.get_formatted('posting_date')}")
				
				for reference in group:
					if not reference:
						continue
					pe.append('references', {
							"reference_doctype": reference.doctype,
							"reference_name": reference.name or reference.ref_number,
							"due_date": reference.get("due_date"),
							"outstanding_amount": flt(reference.amount),
							"allocated_amount": flt(reference.amount),
							"total_amount": flt(reference.amount),
					})
					total_amount += reference.amount
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


	@frappe.whitelist()
	def increment_print_count(self, reprint_check_number=None):
		self.print_count = self.print_count + 1
		self.set_status('Submitted')
		self.save()
		frappe.enqueue_doc(self.doctype, self.name, 'render_check_pdf',	reprint_check_number=reprint_check_number, queue='short', now=True)
		return


	@frappe.whitelist()
	def render_check_pdf(self, reprint_check_number=None):
		if not frappe.db.exists('File', 'Home/Check Run'):
			frappe.new_doc("File").update({"file_name":"Check Run", "is_folder": True, "folder":"Home"}).save()
		initial_check_number = int(self.initial_check_number)
		if reprint_check_number and reprint_check_number != 'undefined':
			self.initial_check_number = int(reprint_check_number)
		output = PdfFileWriter()
		transactions = json.loads(self.transactions)
		check_increment = 0
		_transactions = []
		for pe, group in groupby(transactions, key=lambda x: x.get('payment_entry')):
			group = list(group)
			mode_of_payment, docstatus = frappe.db.get_value('Payment Entry', pe, ['mode_of_payment', 'docstatus'])
			if docstatus == 1 and frappe.db.get_value('Mode of Payment', mode_of_payment, 'type') == 'Bank':
				output = frappe.get_print(
					'Payment Entry',
					pe,
					frappe.get_meta('Payment Entry').default_print_format,
					as_pdf=True,
					output=output,
					no_letterhead=0,
				)
				if initial_check_number != reprint_check_number:
					frappe.db.set_value('Payment Entry', pe, 'reference_no', self.initial_check_number + check_increment)
					for ref in group:
						ref['check_number'] = self.initial_check_number + check_increment
						_transactions.append(ref)
				check_increment += 1
		if _transactions and reprint_check_number:
			frappe.db.set_value('Check Run', self.name, 'transactions', json.dumps(_transactions))
			frappe.db.set_value('Check Run', self.name, 'initial_check_number', self.initial_check_number)
			frappe.db.set_value('Check Run', self.name, 'final_check_number', self.initial_check_number + check_increment -1)
			frappe.db.set_value('Bank Account', self.bank_account, 'check_number', self.final_check_number)
		
		frappe.db.set_value('Check Run', self.name, 'status', 'Ready to Print')
		save_file(f"{self.name}.pdf", read_multi_pdf(output), None, self.name, 'Home/Check Run', False, 0)


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
	if isinstance(doc.end_date, str):
		doc.end_date = getdate(doc.end_date) 
		doc.posting_date = getdate(doc.posting_date) 
	modes_of_payment = frappe.get_all('Mode of Payment', order_by='name')
	if frappe.db.exists('Check Run Settings', {'bank_account': doc.bank_account, 'pay_to_account': doc.pay_to_account}):
		settings = frappe.get_doc('Check Run Settings', {'bank_account': doc.bank_account, 'pay_to_account': doc.pay_to_account})
	else:
		settings = None
	if frappe.db.exists('Check Run', doc.name):
		db_doc = frappe.get_doc('Check Run', doc.name)
		if doc.end_date == db_doc.end_date and db_doc.transactions:
			return {'transactions': json.loads(db_doc.transactions), 'modes_of_payment': modes_of_payment}

	pi_select = """
		(
				SELECT
					'Purchase Invoice' as doctype,
					'Supplier' AS party_type,
					`tabPurchase Invoice`.name,
					`tabPurchase Invoice`.bill_no AS ref_number,
					`tabPurchase Invoice`.supplier_name AS party,
					`tabSupplier`.supplier_name AS party_name,
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
				AND `tabPurchase Invoice`.due_date <= %(end_date)s
			)
	"""
	ec_select = """
		(
			SELECT
				'Expense Claim' as doctype,
				'Employee' AS party_type,
				`tabExpense Claim`.name,
				`tabExpense Claim`.name AS ref_number,
				`tabExpense Claim`.employee_name AS party,
				`tabEmployee`.employee_name AS party_name,
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
			AND `tabExpense Claim`.posting_date <= %(end_date)s
		)
	"""

	je_select = """
		(
			SELECT
				'Journal Entry' AS doctype,
				`tabJournal Entry Account`.party_type,
				`tabJournal Entry`.name,
				`tabJournal Entry`.name AS ref_number,
				`tabJournal Entry Account`.party,
				`tabJournal Entry Account`.party AS party_name,
				`tabJournal Entry Account`.credit_in_account_currency AS amount,
				`tabJournal Entry`.due_date,
				`tabJournal Entry`.posting_date,
				COALESCE(`tabJournal Entry`.mode_of_payment, '\n') AS mode_of_payment
			FROM `tabJournal Entry`, `tabJournal Entry Account`
			WHERE `tabJournal Entry`.name = `tabJournal Entry Account`.parent
			AND `tabJournal Entry`.company = %(company)s
			AND `tabJournal Entry`.docstatus = 1
			AND `tabJournal Entry Account`.account = %(pay_to_account)s
			AND `tabJournal Entry`.due_date <= %(end_date)s
			AND `tabJournal Entry`.name NOT in (
				SELECT `tabPayment Entry Reference`.reference_name
				FROM `tabPayment Entry`, `tabPayment Entry Reference`
				WHERE `tabPayment Entry Reference`.parent = `tabPayment Entry`.name
				AND `tabPayment Entry Reference`.reference_doctype = 'Journal Entry'
				AND `tabPayment Entry`.docstatus = 1
			)
		)
	"""
	query = ""
	if not settings or settings.include_purchase_invoices:
		query += pi_select
	if not settings or settings.include_expense_claims:
		if len(query) > 1:
			query += "\nUNION\n"
		query += ec_select
	if not settings or settings.include_journal_entries:
		if len(query) > 1:
			query += "\nUNION\n"
		query += je_select
	query += "\nORDER BY due_date, name"

	transactions =  frappe.db.sql(query, {
		'company': doc.company, 'pay_to_account': doc.pay_to_account, 'end_date': doc.end_date
	}, as_dict=True)
	for transaction in transactions:
		if settings and settings.pre_check_overdue_items:
			print(transaction.due_date, doc.posting_date)
			if transaction.due_date < doc.posting_date:
				transaction.pay = 1
		if transaction.doctype == 'Journal Entry':
			if transaction.party_type == 'Supplier':
				transaction.party_name = frappe.get_value('Supplier', transaction.party, 'supplier_name')
				transaction.mode_of_payment = frappe.get_value('Supplier', transaction.party, 'supplier_default_mode_of_payment')
			if transaction.party_type == 'Employee':
				transaction.party_name = frappe.get_value('Employee', transaction.party, 'employee_name')
				transaction.mode_of_payment = frappe.get_value('Employee', transaction.party, 'mode_of_payment')

	return {'transactions': transactions, 'modes_of_payment': modes_of_payment}


@frappe.whitelist()
def get_balance(doc):
	doc = frappe._dict(json.loads(doc)) if isinstance(doc, str) else doc
	if not doc.bank_account or not doc.posting_date:
		return
	gl_account = frappe.get_value('Bank Account', doc.bank_account, 'account')
	return get_balance_on(gl_account, doc.posting_date)


@frappe.whitelist()
def download_checks(docname):
	has_permission('Payment Entry', ptype="print", verbose=False, user=frappe.session.user, raise_exception=True)
	file_name = frappe.get_value('File', {'attached_to_name': docname})
	frappe.db.set_value('Check Run', docname, 'status', "Confirm Print")
	return frappe.get_value('File', file_name, 'file_url')


@frappe.whitelist()
def download_nacha(docname):
	has_permission('Payment Entry', ptype="print", verbose=False, user=frappe.session.user, raise_exception=True)
	doc = frappe.get_doc('Check Run', docname)
	settings = get_check_run_settings(doc)
	ach_file = doc.build_nacha_file(settings)
	file_ext = settings.ach_file_extension if settings and settings.ach_file_extension else "ach"
	frappe.local.response.filename = f'{docname.replace(" ", "-").replace("/", "-")}.{file_ext}'
	frappe.local.response.type = "download"
	frappe.local.response.filecontent = ach_file.read()
	comment = frappe.new_doc('Comment')
	comment.owner = "Administrator"
	comment.comment_type = 'Info'
	comment.reference_doctype = 'Check Run'
	comment.reference_name = doc.name
	comment.published = 1
	comment.content = f"{frappe.session.user} created a NACHA file on {now()}"
	comment.flags.ignore_permissions = True
	comment.save()
	frappe.db.commit()


def build_nacha_file_from_payment_entries(doc, payment_entries, settings):
	ach_entries = []
	exceptions = []
	company_bank = frappe.db.get_value('Bank Account', doc.bank_account, 'bank')
	if not company_bank:
		exceptions.append(f'Company Bank missing for {doc.company}')
	if company_bank:
		company_bank_aba_number = frappe.db.get_value('Bank Account', doc.bank_account, 'branch_code')
		company_bank_account_no = frappe.db.get_value('Bank Account', doc.bank_account, 'bank_account_no')
		company_ach_id = frappe.db.get_value('Bank Account', doc.bank_account, 'company_ach_id')
	if company_bank and not company_bank_aba_number:
		exceptions.append(f'Company Bank ABA Number missing for {doc.bank_account}')
	if company_bank and not company_bank_account_no:
		exceptions.append(f'Company Bank Account Number missing for {doc.bank_account}')
	if company_bank and not company_ach_id:
		exceptions.append(f'Company Bank ACH ID missing for {doc.bank_account}')
	for pe in payment_entries:
		party_bank_account = get_decrypted_password(pe.party_type, pe.party, fieldname='bank_account', raise_exception=False)
		if not party_bank_account:
			exceptions.append(f'{pe.party_type} Bank Account missing for {pe.party_name}')
		party_bank = frappe.db.get_value(pe.party_type, pe.party, 'bank')
		if not party_bank:
			exceptions.append(f'{pe.party_type} Bank missing for {pe.party_name}')
		if party_bank:
			party_bank_routing_number = frappe.db.get_value('Bank', party_bank, 'aba_number')
		if not party_bank_routing_number:
			exceptions.append(f'{pe.party_type} Bank Routing Number missing for {pe.party_name}/{employee_bank}')
		ach_entry = ACHEntry(
			transaction_code=22, # checking account 
			receiving_dfi_identification=party_bank_routing_number,
			check_digit=5,
			dfi_account_number=party_bank_account,
			amount=int(pe.paid_amount * 100),
			individual_id_number='',
			individual_name=pe.party_name,
			discretionary_data='',
			addenda_record_indicator=0,
		)
		ach_entries.append(ach_entry)
	
	if exceptions:
		frappe.throw('<br>'.join(e for e in exceptions))

	batch = ACHBatch(
		service_class_code=settings.ach_service_class_code,
		company_name=doc.get('company'),
		company_discretionary_data='',
		company_id=company_ach_id,
		standard_class_code=settings.standard_class_code,
		company_entry_description=settings.ach_description,
		company_descriptive_date=None,
		effective_entry_date=getdate(),
		settlement_date=None,
		originator_status_code=1,
		originating_dfi_id=company_bank_account_no,
		entries=ach_entries
	)
	nacha_file = NACHAFile(
		priority_code=1,
		immediate_destination=company_bank_aba_number,
		immediate_origin=company_bank_aba_number,
		file_creation_date=getdate(),
		file_creation_time=get_datetime(),
		file_id_modifier='0',
		blocking_factor=10,
		format_code=1,
		immediate_destination_name=company_bank,
		immediate_origin_name=company_bank,
		reference_code='',
		batches=[batch]
	)
	return nacha_file


@frappe.whitelist()
def get_check_run_settings(doc):
	doc = frappe._dict(json.loads(doc)) if isinstance(doc, str) else doc
	if frappe.db.exists('Check Run Settings', {'bank_account': doc.bank_account, 'pay_to_account': doc.pay_to_account}):
		return frappe.get_doc('Check Run Settings', {'bank_account': doc.bank_account, 'pay_to_account': doc.pay_to_account})