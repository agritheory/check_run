import frappe
import datetime

suppliers = [
	("Exceptional Grid", "Electricity", "ACH/EFT", 150.00),
	("Liu & Loewen Accountants LLP", "Accounting Services", "ACH/EFT", 500.00),
	("Mare Digitalis", "Cloud Services", "ACH/EFT", 200.00),
	("AgriTheory", "ERPNext Consulting", "Check", 1000.00),
	("HIJ Telecom, Inc", "Internet Services", "Check", 150.00),
	("Sphere Cellular", "Phone Services", "ACH/EFT", 250.00),
	("Cooperative Ag Finance", "Financial Services", "Wire Transfer", 5000.00),
]

tax_authority = [
	("Local Tax Authority", "Payroll Taxes", "Check", 0.00),
]

day = datetime.date(int(frappe.defaults.get_defaults().get('fiscal_year')), 1 ,1)
company = frappe.defaults.get_defaults().get('company')
company_account = frappe.get_value("Account", {"account_type": "Bank", "company": company, "is_group": 0})

def create_test_data():
	create_bank_and_bank_account()
	create_suppliers()
	create_items()
	create_invoices()
	config_expense_claim()
	create_employees()
	create_expense_claim()
	create_payroll_journal_entry()


def create_bank_and_bank_account():
	if not frappe.db.exists('Mode of Payment', 'ACH/EFT'):
		mop = frappe.new_doc('Mode of Payment')
		mop.mode_of_payment = 'ACH/EFT'
		mop.enabled = 1
		mop.type = 'Bank'
		mop.append('accounts', {'company': company, 'default_account': company_account})
		mop.save()

	if not frappe.db.exists('Bank', 'Local Bank'):
		bank = frappe.new_doc('Bank')
		bank.bank_name = "Local Bank"
		bank.save()

	if not frappe.db.exists('Bank Account', 'Primary Checking - Local Bank'):
		bank_account = frappe.new_doc('Bank Account')
		bank_account.account_name = 'Checking'
		bank_account.bank = bank.name
		bank_account.is_default = 1
		bank_account.is_company_account = 1
		bank_account.company = company
		bank_account.account = company_account
		bank_account.check_number = 2500
		bank_account.save()

	doc = frappe.new_doc("Journal Entry")
	doc.posting_date = day
	doc.voucher_type = "Opening Entry"
	doc.company = company
	opening_balance = 10000.00
	doc.append("accounts", {"account": company_account, "debit_in_account_currency": opening_balance})
	retained_earnings = frappe.get_value('Account', {'account_name': "Retained Earnings"})
	doc.append("accounts", {"account": retained_earnings, "credit_in_account_currency": opening_balance})
	doc.save()
	doc.submit()

def create_suppliers():
	for supplier in suppliers + tax_authority:
		biz = frappe.new_doc("Supplier")
		biz.supplier_name = supplier[0]
		biz.supplier_group = "Services"
		biz.country = "United States"
		biz.supplier_default_mode_of_payment = supplier[2]
		biz.currency = "USD" 
		biz.default_price_list = "Standard Buying"
		biz.save()

def create_items():
	for supplier in suppliers + tax_authority:
		item = frappe.new_doc("Item")
		item.item_code = item.item_name = supplier[1]
		item.item_group = "Services"
		item.stock_uom = "Nos"
		item.maintain_stock = 0
		item.is_sales_item, item.is_sub_contracted_item, item.include_item_in_manufacturing = 0, 0, 0
		item.grant_commission = 0
		item.is_purchase_item = 1
		item.append("supplier_items", {"supplier": supplier[0]})
		item.append("item_defaults", {"company": company, "default_warehouse": "", "default_supplier": supplier[0]})
		item.save()

def create_invoices():
	# first month - already paid
	for supplier in suppliers:
		pi = frappe.new_doc('Purchase Invoice')
		pi.company = company
		pi.set_posting_time = 1
		pi.posting_date = day
		pi.supplier = supplier[0]
		pi.append('items', {
			'item_code': supplier[1],
			'rate': supplier[3],
			'qty': 1,
		})
		pi.save()
		pi.submit()
	# two electric meters / test invoice aggregation
	pi = frappe.new_doc('Purchase Invoice')
	pi.company = company
	pi.set_posting_time = 1
	pi.posting_date = day
	pi.supplier = suppliers[0][0]
	pi.append('items', {
		'item_code': suppliers[0][1],
		'rate': 75.00,
		'qty': 1,
	})
	pi.save()
	pi.submit()
	# second month - unpaid
	next_day = day + datetime.timedelta(days=31)

	for supplier in suppliers:
		pi = frappe.new_doc('Purchase Invoice')
		pi.company = company
		pi.set_posting_time = 1
		pi.posting_date = next_day
		pi.supplier = supplier[0]
		pi.append('items', {
			'item_code': supplier[1],
			'rate': supplier[3],
			'qty': 1,
		})
		pi.save()
		pi.submit()
	# two electric meters / test invoice aggregation
	pi = frappe.new_doc('Purchase Invoice')
	pi.company = company
	pi.set_posting_time = 1
	pi.posting_date = next_day
	pi.supplier = suppliers[0][0]
	pi.append('items', {
		'item_code': suppliers[0][1],
		'rate': 75.00,
		'qty': 1,
	})
	pi.save()
	pi.submit()


def config_expense_claim():
	try:
		travel_expense_account = frappe.get_value('Account', {'account_name': 'Travel Expenses', 'company': company})
		travel = frappe.get_doc('Expense Claim Type', 'Travel')
		travel.append('accounts', {'company': company, 'default_account': travel_expense_account})
		travel.save()
	except:
		pass

	if frappe.db.exists('Account', {'account_name': 'Payroll Taxes', 'company': company}):
		return
	pta = frappe.new_doc('Account')
	pta.account_name = "Payroll Taxes"
	pta.account_number = max([int(a.account_number or 1) for a in frappe.get_all('Account', {'is_group': 0},['account_number'])]) + 1
	pta.account_type = "Expense Account"
	pta.company = company
	pta.parent_account = frappe.get_value('Account', {'account_name': 'Indirect Expenses', 'company': company})
	pta.save()


def create_employees():
	for employee_number in range(1, 13):
		emp = frappe.new_doc('Employee')
		emp.first_name = "Test"
		emp.last_name = f"Employee {employee_number}"
		emp.employment_type = "Full-time"
		emp.company = company
		emp.status = "Active"
		emp.gender = "Other"
		emp.date_of_birth = datetime.date(1990, 1, 1)
		emp.date_of_joining = datetime.date(2020, 1, 1)
		emp.mode_of_payment = 'Check' if employee_number % 3 == 0 else 'ACH/EFT'
		emp.expense_approver = 'Administrator'
		if emp.mode_of_payment == 'ACH/EFT':
			emp.bank = 'Local Bank'
			emp.bank_account = f'{employee_number}123456'
		emp.save()


def create_expense_claim():
	# first month - paid
	ec = frappe.new_doc('Expense Claim')
	ec.employee = "Test Employee 2"
	ec.expense_approver = "Administrator"
	ec.approval_status = 'Approved'
	ec.append('expenses', {
		'expense_date': day,
		'expense_type': 'Travel',
		'amount': 50.0
	})
	ec.posting_date = day
	ec.company = company
	ec.payable_account = frappe.get_value('Company', company, 'default_payable_account')
	ec.save()
	ec.submit()
	# second month - open
	next_day = day + datetime.timedelta(days=31)

	ec = frappe.new_doc('Expense Claim')
	ec.employee = "Test Employee 2"
	ec.expense_approver = "Administrator"
	ec.approval_status = 'Approved'
	ec.append('expenses', {
		'expense_date': next_day,
		'expense_type': 'Travel',
		'amount': 50.0
	})
	ec.posting_date = next_day
	ec.company = company
	ec.payable_account = frappe.get_value('Company', company, 'default_payable_account')
	ec.save()
	ec.submit()
	# two expense claims to test aggregation
	ec = frappe.new_doc('Expense Claim')
	ec.employee = "Test Employee 2"
	ec.expense_approver = "Administrator"
	ec.approval_status = 'Approved'
	ec.append('expenses', {
		'expense_date': next_day,
		'expense_type': 'Travel',
		'amount': 50.0
	})
	ec.posting_date = next_day
	ec.company = company
	ec.payable_account = frappe.get_value('Company', company, 'default_payable_account')
	ec.save()
	ec.submit()


def create_payroll_journal_entry():
	emps = frappe.get_list('Employee', {'company': company})
	cost_center = frappe.get_value('Company', company, 'cost_center')
	payroll_account = frappe.get_value('Account', {'company': company, 'account_name': 'Payroll Payable', 'is_group': 0})
	salary_account = frappe.get_value('Account', {'company': company, 'account_name': 'Salary', 'is_group': 0})
	payroll_expense = frappe.get_value('Account', {'company': company, 'account_name': 'Payroll Taxes', 'is_group': 0})
	payable_account= frappe.get_value('Company', company, 'default_payable_account')
	je = frappe.new_doc('Journal Entry')
	je.entry_type = 'Journal Entry'
	je.company = company
	je.posting_date = day
	je.due_date = day
	total_payroll = 0.0
	for idx, emp in enumerate(emps):
		employee_name = frappe.get_value('Employee', {'company': company, 'name': emp.name}, 'employee_name')
		je.append('accounts', {
			'account': payroll_account,
			'bank_account': frappe.get_value("Bank Account", {'account': company_account}),
			'party_type': 'Employee',
			'party': emp.name,
			'cost_center': cost_center,
			'account_currency': 'USD',
			'credit': 1000.00,
			'credit_in_account_currency': 1000.00,
			'debit': 0.00,
			'debit_in_account_currency': 0.00,
			'user_remark': employee_name + ' Paycheck',
			'idx': idx + 2
		})
		total_payroll += 1000.00
	je.append('accounts', {
		'account': salary_account,
		'cost_center': cost_center,
		'account_currency': 'USD',
		'credit': 0.00,
		'credit_in_account_currency': 0.00,
		'debit': total_payroll,
		'debit_in_account_currency': total_payroll,
		'idx': 1,
	})
	je.append('accounts', {
		'account': payroll_expense,
		'cost_center': cost_center,
		'account_currency': 'USD',
		'credit': 0.00,
		'credit_in_account_currency': 0.00,
		'debit': total_payroll * 0.15,
		'debit_in_account_currency': total_payroll * 0.15,
	})
	je.append('accounts', {
		'account': payable_account,
		'cost_center': cost_center,
		'party_type': 'Supplier',
		'party': tax_authority[0][0],
		'account_currency': 'USD',
		'credit': total_payroll * 0.15,
		'credit_in_account_currency':total_payroll * 0.15,
		'debit': 0.00,
		'debit_in_account_currency': 0.0,
	})
	je.save()
	je.submit()