# Copyright (c) 2022, AgriTheory and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import datetime
import json
from itertools import groupby, zip_longest
from io import StringIO
import types

from PyPDF2 import PdfFileWriter

import frappe
from frappe.model.document import Document
from frappe.utils.data import flt
from frappe.utils.data import date_diff, add_days, nowdate, getdate, now, get_datetime
from frappe.utils.print_format import read_multi_pdf
from frappe.permissions import has_permission
from frappe.utils.file_manager import save_file, remove_all, download_file
from frappe.utils.password import get_decrypted_password
from frappe.contacts.doctype.address.address import	get_default_address
from frappe.query_builder.custom import ConstantColumn
from frappe.query_builder.functions import Coalesce

from erpnext.accounts.utils import get_balance_on
from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import get_dimensions

from atnacha import ACHEntry, ACHBatch, NACHAFile
from check_run.check_run.doctype.check_run_settings.check_run_settings import create


class CheckRun(Document):
	def onload(self):
		if self.is_new():
			return
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
				self.set_last_check_number()
				self.set_default_payable_account()
				self.set_default_dates()
		else:
			self.validate_transactions()
			self.validate_last_check_number()

	def on_cancel(self):
		settings = get_check_run_settings(self)
		if not settings.allow_cancellation:
			frappe.throw(frappe._('The settings for this Check Run do not allow cancellation'))
		if settings.allow_cancellation and settings.cascade_cancellation:
			# cancel all PEs linked to this check run
			pes = frappe.get_all('Payment Entry', {'check_run': self.name, 'docstatus': 1})
			for pe in pes:
				frappe.get_doc('Payment Entry', pe).cancel()
		if settings.allow_cancellation and not settings.cascade_cancellation:
			# unlink all PE's linked to this check run
			pes = frappe.get_all('Payment Entry', {'check_run': self.name, 'docstatus': 1})
			for pe in pes:
				frappe.db.set_value('Payment Entry', pe, 'check_run', '')

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

	def set_last_check_number(self):
		if self.ach_only().ach_only:
			return
		check_number = frappe.get_value('Bank Account', self.bank_account, "check_number")
		self.initial_check_number = int(check_number or 0) + 1

	def set_default_payable_account(self):
		if not self.pay_to_account:
			self.pay_to_account = frappe.get_value('Company', self.company, "default_payable_account")

	def set_default_dates(self):
		if not self.posting_date:
			self.posting_date = getdate()
		if not self.end_date:
			self.end_date = getdate()

	def validate_transactions(self):
		if not self.get('transactions'):
			return
		selected = [txn for txn in json.loads(self.get('transactions')) if txn['pay']]
		wrong_status = []
		for t in selected:
			if not t['mode_of_payment']:
				frappe.throw(frappe._(f"Mode of Payment Required: {t['party_name']} {t['ref_number']}"))
			filters = {'name': t['name'] if t['doctype'] != 'Journal Entry' else t['ref_number']}
			if frappe.get_value(t['doctype'], filters, 'docstatus') != 1:
				wrong_status.append({'party_name': t['party_name'], 'ref_number': t['ref_number'] or '', 'name': t['name']})
		if len(wrong_status) < 1:
			return
		invalid_records = ''
		for invalid_record in wrong_status:
			invalid_records += ' '.join(invalid_record.values()) + '<br>'
		frappe.throw(frappe._(
			f"The following document(s) have been cancelled, please remove them from Check Run to continue:<br>{invalid_records}"
		))

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
		transactions = self.transactions
		transactions = json.loads(transactions)
		if len(transactions) < 1:
			frappe.throw("You must select at least one Invoice to pay.")
		self.print_count = 0
		if self.ach_only().ach_only:
			self.initial_check_number = ""
			self.final_check_number = ""

		if len(transactions) < 25:
			self._before_submit()
		else:
			self.status = 'Submitting'
			frappe.enqueue_doc(self.doctype, self.name, "_before_submit", save=True, queue="short", timeout=3600)

	def _before_submit(self, save=False):
		try:
			transactions = self.transactions
			transactions = json.loads(transactions)
			transactions = sorted([frappe._dict(item) for item in transactions if item.get("pay")], key=lambda x: x.party)
			_transactions = self.create_payment_entries(transactions)
			
			self.db_set('transactions', json.dumps(_transactions))
			self.db_set('status', 'Submitted')
			if self.final_check_number:
				frappe.db.set_value('Bank Account', self.bank_account, 'check_number', self.final_check_number)
			frappe.db.commit()
			frappe.publish_realtime('reload', '{}', doctype=self.doctype, docname=self.name)
		except Exception as e:
			frappe.log_error(title=f"{self.name} Check Run Error", message=e)

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
		key_lookup = lambda x: x.party
		if settings and settings.split_by_address:
			key_lookup = lambda x: (x.get('party'), x.get('address'))
			for transaction in transactions:
				transaction['address'] = get_address(
					transaction.get('party'), transaction.get('party_type'), transaction.get('doctype'), transaction.get('name')
				)
		for party, _group in groupby(transactions, key=key_lookup):
			_group = list(_group)
			if frappe.db.get_value('Mode of Payment', _group[0].mode_of_payment, 'type') == 'Bank':
				groups = list(zip_longest(*[iter(_group)] * split)) 
			else:
				groups = [_group]
			if not groups:
				continue
			for group in groups:
				_references = []
				if group[0].doctype == 'Purchase Invoice':
					party = frappe.db.get_value('Purchase Invoice', group[0].name, 'supplier')
				elif group[0].doctype == 'Expense Claim':
					party = frappe.db.get_value('Expense Claim', group[0].name, 'employee')
				elif group[0].doctype == 'Journal Entry':
					party = frappe.db.get_value('Journal Entry Account', group[0].name, 'party')
				pe = frappe.new_doc("Payment Entry")
				pe.payment_type = "Pay"
				pe.posting_date = nowdate()
				pe.mode_of_payment = group[0].mode_of_payment
				pe.company = self.company
				pe.bank_account = self.bank_account
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
					if settings.automatically_release_on_hold_invoices and reference.doctype == 'Purchase Invoice':
						if frappe.get_value(reference.doctype, reference.name, 'on_hold'):
							frappe.db.set_value(reference.doctype, reference.name, 'on_hold', 0)
					if reference.doctype == 'Journal Entry':
						reference_name = reference.ref_number
					else:
						reference_name = reference.name or reference.ref_number
					pe.append('references', {
							"reference_doctype": reference.doctype,
							"reference_name": reference_name,
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
				pe.base_grand_total = total_amount
				pe.save()
				pe.submit()
				for reference in _references:
					reference.payment_entry = pe.name
					_transactions.append(reference)
		return _transactions


	@frappe.whitelist()
	def increment_print_count(self, reprint_check_number=None):
		self.load_from_db()
		frappe.enqueue_doc(self.doctype, self.name, 'render_check_pdf',	reprint_check_number=reprint_check_number, queue='short', now=True)


	@frappe.whitelist()
	def render_check_pdf(self, reprint_check_number=None):
		self.load_from_db()
		self.print_count = self.print_count + 1
		self.set_status('Submitted')
		if not frappe.db.exists('File', 'Home/Check Run'):
			try: 
				cr_folder = frappe.new_doc("File")
				cr_folder.update({"file_name":"Check Run", "is_folder": True, "folder":"Home"})
				cr_folder.save()
			except Exception as e:
				pass
		settings = get_check_run_settings(self)
		initial_check_number = int(self.initial_check_number)
		if reprint_check_number and reprint_check_number != 'undefined':
			self.initial_check_number = int(reprint_check_number)
		output = PdfFileWriter()
		transactions = json.loads(self.transactions)
		check_increment = 0
		_transactions = []
		for pe, group in groupby(transactions, key=lambda x: x.get('payment_entry')):
			group = list(group)
			mode_of_payment, docstatus = frappe.db.get_value('Payment Entry', pe, ['mode_of_payment', 'docstatus']) or (None, None)
			if docstatus == 1 and frappe.db.get_value('Mode of Payment', mode_of_payment, 'type') == 'Bank':
				output = frappe.get_print(
					'Payment Entry',
					pe,
					settings.print_format or frappe.get_meta('Payment Entry').default_print_format,
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
			elif docstatus == 1:
				for ref in group:
					_transactions.append(ref)

		if _transactions and reprint_check_number:
			self.db_set('transactions', json.dumps(_transactions))
		self.db_set('final_check_number', self.initial_check_number + (check_increment - 1))
		self.db_set('status', 'Ready to Print')
		self.db_set('print_count', self.print_count)
		frappe.db.set_value('Bank Account', self.bank_account, 'check_number', self.final_check_number)
		save_file(f"{self.name}.pdf", read_multi_pdf(output), 'Check Run', self.name, 'Home/Check Run', False, 0)
		frappe.db.commit()
		frappe.publish_realtime('reload', '{}', doctype=self.doctype, docname=self.name)


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
	# Remove PDF file(s)
	remove_all('Check Run', docname, from_delete=False, delete_permanently=False)
	
	# Reset status
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

	company = doc.company
	pay_to_account = doc.pay_to_account
	end_date = doc.end_date

	# Build purchase invoices query
	purchase_invoices = frappe.qb.DocType('Purchase Invoice')
	suppliers = frappe.qb.DocType('Supplier')
	pi_qb = (
		frappe.qb.from_(purchase_invoices)
			.inner_join(suppliers)
			.on(purchase_invoices.supplier == suppliers.name)
			.select(
				ConstantColumn('Purchase Invoice').as_('doctype'),
				ConstantColumn('Supplier').as_('party_type'),
				purchase_invoices.name,
				(purchase_invoices.bill_no).as_('ref_number'),
				(purchase_invoices.supplier_name).as_('party'),
				(suppliers.supplier_name).as_('party_name'),
				(purchase_invoices.outstanding_amount).as_('amount'),
				purchase_invoices.due_date,
				purchase_invoices.posting_date,
				Coalesce(purchase_invoices.supplier_default_mode_of_payment, suppliers.supplier_default_mode_of_payment, '\n').as_('mode_of_payment')
			)
			.where(purchase_invoices.outstanding_amount > 0)
			.where(purchase_invoices.company == company)
			.where(purchase_invoices.docstatus == 1)
			.where(purchase_invoices.credit_to == pay_to_account)
			.where(purchase_invoices.due_date <= end_date)
			.where(Coalesce(purchase_invoices.release_date, datetime.date(1900, 1, 1)) <= end_date)
	)

	# Build expense claims query
	exp_claims = frappe.qb.DocType('Expense Claim')
	employees = frappe.qb.DocType('Employee')
	ec_qb = (
		frappe.qb.from_(exp_claims)
			.inner_join(employees)
			.on(exp_claims.employee == employees.name)
			.select(
				ConstantColumn('Expense Claim').as_('doctype'),
				ConstantColumn('Employee').as_('party_type'),
				exp_claims.name,
				(exp_claims.name).as_('ref_number'),
				(exp_claims.employee).as_('party'),
				(employees.employee_name).as_('party_name'),
				(exp_claims.grand_total).as_('amount'),
				(exp_claims.posting_date).as_('due_date'),
				exp_claims.posting_date,
				Coalesce(exp_claims.mode_of_payment, employees.mode_of_payment, '\n').as_('mode_of_payment')
			)
			.where(exp_claims.grand_total > exp_claims.total_amount_reimbursed)
			.where(exp_claims.company == company)
			.where(exp_claims.docstatus == 1)
			.where(exp_claims.payable_account == pay_to_account)
			.where(exp_claims.posting_date <= end_date)
	)

	# Build journal entries query
	journal_entries = frappe.qb.DocType('Journal Entry')
	je_accounts = frappe.qb.DocType('Journal Entry Account')
	payment_entries = frappe.qb.DocType('Payment Entry')
	pe_ref = frappe.qb.DocType('Payment Entry Reference')
	
	sub_q = (
		frappe.qb.from_(payment_entries)
			.inner_join(pe_ref)
			.on(payment_entries.name == pe_ref.parent)
			.select(pe_ref.reference_name)
			.where(pe_ref.reference_doctype == 'Journal Entry')
			.where(payment_entries.party == je_accounts.party)
			.where(payment_entries.docstatus == 1)
	)

	je_qb = (
		frappe.qb.from_(journal_entries)
			.inner_join(je_accounts)
			.on(journal_entries.name == je_accounts.parent)
			.select(
				ConstantColumn('Journal Entry').as_('doctype'),
				je_accounts.party_type,
				je_accounts.name,
				(journal_entries.name).as_('ref_number'),
				je_accounts.party,
				(je_accounts.party).as_('party_name'),
				(je_accounts.credit_in_account_currency).as_('amount'),
				journal_entries.due_date,
				journal_entries.posting_date,
				Coalesce(journal_entries.mode_of_payment, '\n').as_('mode_of_payment')
			)
			.where(journal_entries.company == company)
			.where(journal_entries.docstatus == 1)
			.where(je_accounts.account == pay_to_account)
			.where(journal_entries.due_date <= end_date)
			.where((journal_entries.name).notin(sub_q))
	)
	
	if not settings:
		query = pi_qb.union(ec_qb).union(je_qb)
	else:
		query = ""
		flags = (settings.include_purchase_invoices, settings.include_expense_claims, settings.include_journal_entries)
		for flag, qb in zip(flags, (pi_qb, ec_qb, je_qb)):
			if not flag:
				continue
			if not query:
				query = qb
			else:
				query = query.union(qb)
	if query:
		query = query.orderby('due_date', 'name').get_sql()

	transactions =  frappe.db.sql(query, {
		'company': company, 'pay_to_account': pay_to_account, 'end_date': end_date
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
				exceptions.append(f'{pe.party_type} Bank Routing Number missing for {pe.party_name}')
		ach_entry = ACHEntry(
			transaction_code=22, # checking account 
			receiving_dfi_identification=party_bank_routing_number,
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
		standard_class_code=settings.ach_standard_class_code,
		company_entry_description=settings.ach_description or "",
		company_descriptive_date=None,
		effective_entry_date=getdate(),
		settlement_date=None,
		originator_status_code=1,
		originating_dfi_id=company_bank_account_no,
		entries=ach_entries
	)
	nacha_file = NACHAFile(
		priority_code=1,
		immediate_destination=company_bank_aba_number if not settings.omit_destination else "",
		immediate_origin=company_bank_aba_number,
		file_creation_date=getdate(),
		file_creation_time=get_datetime(),
		file_id_modifier='0',
		blocking_factor=10,
		format_code=1,
		immediate_destination_name=company_bank,
		immediate_origin_name=doc.company,
		reference_code='',
		batches=[batch]
	)
	return nacha_file


@frappe.whitelist()
def get_check_run_settings(doc):
	doc = frappe._dict(json.loads(doc)) if isinstance(doc, str) else doc
	if frappe.db.exists('Check Run Settings', {'bank_account': doc.bank_account, 'pay_to_account': doc.pay_to_account}):
		return frappe.get_doc('Check Run Settings', {'bank_account': doc.bank_account, 'pay_to_account': doc.pay_to_account})
	else:
		return create(doc.company, doc.bank_account, doc.pay_to_account)
	

def get_address(party, party_type, doctype, name):
	if doctype == 'Purchase Invoice':
		return frappe.get_value('Purchase Invoice', name, 'supplier_address')
	elif doctype == 'Expense Claim':
		return frappe.get_value('Employee', name, 'permanent_address')
	elif doctype == 'Journal Entry':
		if party_type == 'Supplier':
			return get_default_address('Supplier', party)
		elif party_type == 'Employee':
			return frappe.get_value('Employee', name, 'permanent_address')


@frappe.whitelist()
def ach_only(docname):
	if not frappe.db.exists('Check Run', docname):
		return {'ach_only': False, 'checks_only': False}
	cr = frappe.get_doc('Check Run', docname)
	return cr.ach_only()