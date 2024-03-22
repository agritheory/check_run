import datetime
import types

import frappe
from frappe.utils.data import add_days, flt
from frappe.desk.page.setup_wizard.setup_wizard import setup_complete
from erpnext.setup.utils import enable_all_roles_and_domains, set_defaults_for_tests
from erpnext.accounts.doctype.account.account import update_account_number
from erpnext.accounts.doctype.purchase_invoice.purchase_invoice import make_debit_note


from check_run.tests.fixtures import (
	employees,
	suppliers,
	tax_authority,
	customers,
	sales_tax_templates,
)


def before_test():
	frappe.clear_cache()
	today = frappe.utils.getdate()
	setup_complete(
		{
			"currency": "USD",
			"full_name": "Administrator",
			"company_name": "Chelsea Fruit Co",
			"timezone": "America/New_York",
			"company_abbr": "CFC",
			"domains": ["Distribution"],
			"country": "United States",
			"fy_start_date": today.replace(month=1, day=1).isoformat(),
			"fy_end_date": today.replace(month=12, day=31).isoformat(),
			"language": "english",
			"company_tagline": "Chelsea Fruit Co",
			"email": "support@agritheory.dev",
			"password": "admin",
			"chart_of_accounts": "Standard with Numbers",
			"bank_account": "Primary Checking",
		}
	)
	enable_all_roles_and_domains()
	set_defaults_for_tests()
	frappe.db.commit()
	create_test_data()
	for modu in frappe.get_all("Module Onboarding"):
		frappe.db.set_value("Module Onboarding", modu, "is_complete", 1)
	frappe.set_value("Website Settings", "Website Settings", "home_page", "login")
	frappe.db.commit()


def create_test_data():
	setup_accounts()
	settings = frappe._dict(
		{
			"day": frappe.utils.getdate().replace(month=1, day=1),
			"company": frappe.defaults.get_defaults().get("company"),
			"company_account": frappe.get_value(
				"Account",
				{
					"account_type": "Bank",
					"company": frappe.defaults.get_defaults().get("company"),
					"is_group": 0,
				},
			),
		}
	)
	create_bank_and_bank_account(settings)
	create_payment_terms_templates(settings)
	create_suppliers(settings)
	create_items(settings)
	create_invoices(settings)
	config_expense_claim(settings)
	create_employees(settings)
	create_expense_claim(settings)
	create_manual_payment_entry(settings)
	create_customers(settings)
	modify_tax_templates(settings)
	create_sales_invoices(settings)
	for month in range(1, 13):
		create_payroll_journal_entry(settings)
		settings.day = settings.day.replace(month=month)


def create_bank_and_bank_account(settings):
	if not frappe.db.exists("Mode of Payment", "ACH/EFT"):
		mop = frappe.new_doc("Mode of Payment")
		mop.mode_of_payment = "ACH/EFT"
		mop.enabled = 1
		mop.type = "Electronic"
		mop.append(
			"accounts", {"company": settings.company, "default_account": settings.company_account}
		)
		mop.save()

	wire_transfer = frappe.get_doc("Mode of Payment", "Wire Transfer")
	wire_transfer.type = "General"
	wire_transfer.append(
		"accounts", {"company": settings.company, "default_account": settings.company_account}
	)
	wire_transfer.save()

	credit_card = frappe.get_doc("Mode of Payment", "Credit Card")
	credit_card.type = "General"
	credit_card.append(
		"accounts", {"company": settings.company, "default_account": settings.company_account}
	)
	credit_card.save()

	bank_draft = frappe.get_doc("Mode of Payment", "Bank Draft")
	bank_draft.type = "General"
	bank_draft.append(
		"accounts", {"company": settings.company, "default_account": settings.company_account}
	)
	bank_draft.save()

	check_mop = frappe.get_doc("Mode of Payment", "Check")
	check_mop.type = "Bank"
	check_mop.append(
		"accounts", {"company": settings.company, "default_account": settings.company_account}
	)
	check_mop.save()

	if not frappe.db.exists("Bank", "Local Bank"):
		bank = frappe.new_doc("Bank")
		bank.bank_name = "Local Bank"
		bank.aba_number = "07200091"
		bank.save()

	if not frappe.db.exists("Bank Account", "Primary Checking - Local Bank"):
		bank_account = frappe.new_doc("Bank Account")
		bank_account.account_name = "Primary Checking"
		bank_account.bank = bank.name
		bank_account.is_default = 1
		bank_account.is_company_account = 1
		bank_account.company = settings.company
		bank_account.account = settings.company_account
		bank_account.check_number = 2500
		bank_account.company_ach_id = "1381655417"
		bank_account.bank_account_no = "072000915"
		bank_account.branch_code = "07200091"
		bank_account.save()

	doc = frappe.new_doc("Journal Entry")
	doc.posting_date = settings.day
	doc.voucher_type = "Opening Entry"
	doc.company = settings.company
	opening_balance = 50000.00
	doc.append(
		"accounts", {"account": settings.company_account, "debit_in_account_currency": opening_balance}
	)
	retained_earnings = frappe.get_value(
		"Account", {"account_name": "Retained Earnings", "company": settings.company}
	)
	doc.append(
		"accounts", {"account": retained_earnings, "credit_in_account_currency": opening_balance}
	)
	doc.save()
	doc.submit()


def setup_accounts():
	frappe.rename_doc(
		"Account", "1000 - Application of Funds (Assets) - CFC", "1000 - Assets - CFC", force=True
	)
	frappe.rename_doc(
		"Account", "2000 - Source of Funds (Liabilities) - CFC", "2000 - Liabilities - CFC", force=True
	)
	frappe.rename_doc(
		"Account", "1310 - Debtors - CFC", "1310 - Accounts Receivable - CFC", force=True
	)
	frappe.rename_doc(
		"Account", "2110 - Creditors - CFC", "2110 - Accounts Payable - CFC", force=True
	)
	update_account_number("1110 - Cash - CFC", "Petty Cash", account_number="1110")
	update_account_number("ST 6% - CFC", "Sales Tax Payable", account_number="2320")
	frappe.set_value("Account", "2320 - Sales Tax Payable - CFC", "account_type", "Payable")


def create_payment_terms_templates(settings):
	if not frappe.db.exists("Payment Terms Template", "Net 30"):
		pt = frappe.new_doc("Payment Term")
		pt.payment_term_name = "Net 30"
		pt.due_date_based_on = "Day(s) after invoice date"
		pt.invoice_portion = 100
		pt.credit_days = 30
		pt.save()
		doc = frappe.new_doc("Payment Terms Template")
		doc.template_name = pt.name
		doc.append(
			"terms",
			{
				"payment_term": pt.name,
				"invoice_portion": pt.invoice_portion,
				"due_date_based_on": pt.due_date_based_on,
				"credit_days": pt.credit_days,
			},
		)
		doc.save()
	if not frappe.db.exists("Payment Terms Template", "Due on Receipt"):
		pt = frappe.new_doc("Payment Term")
		pt.payment_term_name = "Due on Receipt"
		pt.due_date_based_on = "Day(s) after invoice date"
		pt.invoice_portion = 100
		pt.credit_days = 0
		pt.save()
		doc = frappe.new_doc("Payment Terms Template")
		doc.template_name = pt.name
		doc.append(
			"terms",
			{
				"payment_term": pt.name,
				"invoice_portion": pt.invoice_portion,
				"due_date_based_on": pt.due_date_based_on,
				"credit_days": pt.credit_days,
			},
		)
		doc.save()
	if not frappe.db.exists("Payment Terms Template", "Net 14"):
		pt = frappe.new_doc("Payment Term")
		pt.payment_term_name = "Net 14"
		pt.due_date_based_on = "Day(s) after invoice date"
		pt.invoice_portion = 100
		pt.credit_days = 14
		pt.save()
		doc = frappe.new_doc("Payment Terms Template")
		doc.template_name = pt.name
		doc.append(
			"terms",
			{
				"payment_term": pt.name,
				"invoice_portion": pt.invoice_portion,
				"due_date_based_on": pt.due_date_based_on,
				"credit_days": pt.credit_days,
			},
		)
		doc.save()

	if not frappe.db.exists("Payment Terms Template", "18 Month Rental Agreement"):
		doc = frappe.new_doc("Payment Terms Template")
		doc.template_name = "18 Month Rental Agreement"
		for month in range(0, 18):
			pt = frappe.new_doc("Payment Term")
			pt.payment_term_name = f"Rental Installment {month+1}"
			pt.due_date_based_on = "Month(s) after the end of the invoice month"
			pt.invoice_portion = 5.555555555555556
			pt.credit_months = month
			pt.save()
			doc.append(
				"terms",
				{
					"payment_term": pt.name,
					"invoice_portion": pt.invoice_portion,
					"due_date_based_on": pt.due_date_based_on,
					"credit_months": pt.credit_months,
				},
			)
		doc.save()


def create_suppliers(settings):
	addresses = frappe._dict({})
	for supplier in suppliers + tax_authority:
		biz = frappe.new_doc("Supplier")
		biz.supplier_name = supplier[0]
		biz.supplier_group = "Services"
		biz.country = "United States"
		biz.supplier_default_mode_of_payment = supplier[2]
		if biz.supplier_default_mode_of_payment == "ACH/EFT":
			biz.bank = "Local Bank"
			biz.bank_account = "123456789"
		biz.currency = "USD"
		biz.default_price_list = "Standard Buying"
		biz.payment_terms = supplier[4]
		if supplier[0] == "Tireless Equipment Rental, Inc":
			biz.number_of_invoices_per_check_voucher = 1
		biz.save()

		addr = frappe.new_doc("Address")
		addr.address_title = f"{supplier[0]} - {supplier[5]['city']}"
		addr.address_type = "Billing"
		addr.address_line1 = supplier[5]["address_line1"]
		addr.city = supplier[5]["city"]
		addr.state = supplier[5]["state"]
		addr.country = supplier[5]["country"]
		addr.pincode = supplier[5]["pincode"]
		addr.append("links", {"link_doctype": "Supplier", "link_name": supplier[0]})
		addr.save()

	addr = frappe.new_doc("Address")
	addr.address_type = "Billing"
	addr.address_title = "HIJ Telecom - Burlingame"
	addr.address_line1 = "167 Auto Terrace"
	addr.city = "Burlingame"
	addr.state = "ME"
	addr.country = "United States"
	addr.pincode = "79749"
	addr.append("links", {"link_doctype": "Supplier", "link_name": "HIJ Telecom, Inc"})
	addr.save()


def create_items(settings):
	for supplier in suppliers + tax_authority:
		if frappe.db.exists("Item", supplier[1]):
			continue
		item = frappe.new_doc("Item")
		item.item_code = item.item_name = supplier[1]
		item.item_group = "Services"
		item.stock_uom = "Nos"
		item.maintain_stock = 0
		item.is_sales_item, item.is_sub_contracted_item, item.include_item_in_manufacturing = 0, 0, 0
		item.grant_commission = 0
		item.is_purchase_item = 1
		item.append("supplier_items", {"supplier": supplier[0]})
		item.append(
			"item_defaults",
			{"company": settings.company, "default_warehouse": "", "default_supplier": supplier[0]},
		)
		item.save()


def create_invoices(settings):
	pi = frappe.new_doc("Purchase Invoice")
	pi.company = settings.company
	pi.set_posting_time = 1
	pi.posting_date = settings.day
	pi.supplier = "Tireless Equipment Rental, Inc"
	pi.append(
		"items",
		{
			"item_code": "Equipment Rental",
			"rate": 30000.00,
			"qty": 1,
		},
	)
	pi.payment_terms = "18 Month Rental Agreement"
	pi.save()
	pi.submit()

	# first month - already paid
	for supplier in suppliers:
		if supplier[0].startswith("Tireless"):
			continue
		pi = frappe.new_doc("Purchase Invoice")
		pi.company = settings.company
		pi.set_posting_time = 1
		pi.posting_date = settings.day
		pi.supplier = supplier[0]
		pi.append(
			"items",
			{
				"item_code": supplier[1],
				"rate": supplier[3],
				"qty": 1,
			},
		)
		pi.save()
		pi.submit()
	# two electric meters / test invoice aggregation
	pi = frappe.new_doc("Purchase Invoice")
	pi.company = settings.company
	pi.set_posting_time = 1
	pi.posting_date = settings.day
	pi.supplier = suppliers[0][0]
	pi.append(
		"items",
		{
			"item_code": suppliers[0][1],
			"rate": 75.00,
			"qty": 1,
		},
	)
	pi.save()
	pi.submit()

	# two phone bills / test address splitting
	pi = frappe.new_doc("Purchase Invoice")
	pi.company = settings.company
	pi.set_posting_time = 1
	pi.posting_date = settings.day
	pi.supplier = suppliers[4][0]
	pi.append(
		"items",
		{
			"item_code": suppliers[4][1],
			"rate": 122.50,
			"qty": 1,
		},
	)
	pi.supplier_address = "HIJ Telecom - Burlingame-Billing"
	pi.save()
	pi.submit()

	# second month - unpaid
	next_day = settings.day + datetime.timedelta(days=31)

	for supplier in suppliers:
		if supplier[0].startswith("Tireless"):
			continue
		pi = frappe.new_doc("Purchase Invoice")
		pi.company = settings.company
		pi.set_posting_time = 1
		pi.posting_date = next_day
		pi.supplier = supplier[0]
		pi.append(
			"items",
			{
				"item_code": supplier[1],
				"rate": supplier[3],
				"qty": 1,
			},
		)
		pi.save()
		pi.submit()
	# two electric meters / test invoice aggregation
	pi = frappe.new_doc("Purchase Invoice")
	pi.company = settings.company
	pi.set_posting_time = 1
	pi.posting_date = next_day
	pi.supplier = suppliers[0][0]
	pi.append(
		"items",
		{
			"item_code": suppliers[0][1],
			"rate": 75.00,
			"qty": 1,
		},
	)
	pi.save()
	pi.submit()

	# two phone bills / test address splitting
	pi = frappe.new_doc("Purchase Invoice")
	pi.company = settings.company
	pi.set_posting_time = 1
	pi.posting_date = settings.day
	pi.supplier = suppliers[4][0]
	pi.append(
		"items",
		{
			"item_code": suppliers[4][1],
			"rate": 122.50,
			"qty": 1,
		},
	)
	pi.supplier_address = "HIJ Telecom - Burlingame-Billing"
	pi.save()
	pi.submit()

	# test on-hold invoice
	pi = frappe.new_doc("Purchase Invoice")
	pi.company = settings.company
	pi.set_posting_time = 1
	pi.posting_date = settings.day
	pi.supplier = suppliers[1][0]
	pi.append(
		"items",
		{
			"item_code": suppliers[1][1],
			"rate": 4000.00,
			"qty": 1,
		},
	)
	pi.on_hold = 1
	pi.release_date = settings.day + datetime.timedelta(days=60)
	pi.hold_comment = "Testing for on hold invoices"
	pi.validate_release_date = types.MethodType(
		validate_release_date, pi
	)  # allow date to be backdated for testing
	pi.save()
	pi.submit()

	spi = frappe.get_value(
		"Purchase Invoice",
		{"supplier": "Cooperative Ag Finance"},
		order_by="posting_date DESC",
	)
	rpi = make_debit_note(spi)
	rpi.return_against = (
		None  # this approach isn't best practice but it allows us to see a negative PI in the check run
	)
	rpi.items[0].rate = 500
	rpi.save()
	rpi.submit()


def validate_release_date(self):
	pass


def config_expense_claim(settings):
	try:
		travel_expense_account = frappe.get_value(
			"Account", {"account_name": "Travel Expenses", "company": settings.company}
		)
		travel = frappe.get_doc("Expense Claim Type", "Travel")
		travel.append(
			"accounts", {"company": settings.company, "default_account": travel_expense_account}
		)
		travel.save()
	except Exception as e:
		pass

	payroll_payable = frappe.db.get_value(
		"Account", {"account_name": "Payroll Payable", "company": settings.company}
	)
	if payroll_payable:
		frappe.db.set_value("Account", payroll_payable, "account_type", "Payable")

	if frappe.db.exists("Account", {"account_name": "Payroll Taxes", "company": settings.company}):
		return
	pta = frappe.new_doc("Account")
	pta.account_name = "Payroll Taxes"
	pta.account_number = (
		max(
			int(a.account_number or 1)
			for a in frappe.get_all("Account", {"is_group": 0}, ["account_number"])
		)
		+ 1
	)
	pta.account_type = "Expense Account"
	pta.company = settings.company
	pta.parent_account = frappe.get_value(
		"Account", {"account_name": "Indirect Expenses", "company": settings.company}
	)
	pta.save()


def create_employees(settings):
	for employee_number, employee in enumerate(employees, start=10):
		emp = frappe.new_doc("Employee")
		emp.first_name = employee[0].split(" ")[0]
		emp.last_name = employee[0].split(" ")[1]
		emp.employment_type = "Full-time"
		emp.company = settings.company
		emp.status = "Active"
		emp.gender = employee[1]
		emp.date_of_birth = employee[2]
		emp.date_of_joining = employee[3]
		emp.mode_of_payment = "Check" if employee_number % 3 == 0 else "ACH/EFT"
		emp.mode_of_payment = "Cash" if employee_number == 10 else emp.mode_of_payment
		emp.mode_of_payment = None if employee_number % 4 == 0 else emp.mode_of_payment
		emp.expense_approver = "Administrator"
		if emp.mode_of_payment == "ACH/EFT":
			emp.bank = "Local Bank"
			emp.bank_account = f"{employee_number}12345"
		emp.save()


def create_expense_claim(settings):
	cost_center = frappe.get_value("Company", settings.company, "cost_center")
	payable_acct = frappe.get_value("Company", settings.company, "default_payable_account")
	# first month - paid
	ec = frappe.new_doc("Expense Claim")
	ec.employee = "HR-EMP-00002"
	ec.expense_approver = "Administrator"
	ec.approval_status = "Approved"
	ec.append(
		"expenses",
		{
			"expense_date": settings.day,
			"expense_type": "Travel",
			"amount": 50.0,
			"sanctioned_amount": 50.0,
			"cost_center": cost_center,
		},
	)
	ec.posting_date = settings.day
	ec.company = settings.company
	ec.payable_account = payable_acct
	ec.save()
	ec.submit()
	# second month - open
	next_day = settings.day + datetime.timedelta(days=31)

	ec = frappe.new_doc("Expense Claim")
	ec.employee = "HR-EMP-00002"
	ec.expense_approver = "Administrator"
	ec.approval_status = "Approved"
	ec.append(
		"expenses",
		{
			"expense_date": next_day,
			"expense_type": "Travel",
			"amount": 50.0,
			"sanctioned_amount": 50.0,
			"cost_center": cost_center,
		},
	)
	ec.posting_date = next_day
	ec.company = settings.company
	ec.payable_account = payable_acct
	ec.save()
	ec.submit()
	# two expense claims to test aggregation
	ec = frappe.new_doc("Expense Claim")
	ec.employee = "HR-EMP-00002"
	ec.expense_approver = "Administrator"
	ec.approval_status = "Approved"
	ec.append(
		"expenses",
		{
			"expense_date": next_day,
			"expense_type": "Travel",
			"amount": 50.0,
			"sanctioned_amount": 50.0,
			"cost_center": cost_center,
		},
	)
	ec.posting_date = next_day
	ec.company = settings.company
	ec.payable_account = payable_acct
	ec.save()
	ec.submit()


def create_payroll_journal_entry(settings):
	emps = frappe.get_list("Employee", {"company": settings.company})
	cost_center = frappe.get_value("Company", settings.company, "cost_center")
	payroll_account = frappe.get_value(
		"Account", {"company": settings.company, "account_name": "Payroll Payable", "is_group": 0}
	)
	salary_account = frappe.get_value(
		"Account", {"company": settings.company, "account_name": "Salary", "is_group": 0}
	)
	payroll_expense = frappe.get_value(
		"Account", {"company": settings.company, "account_name": "Payroll Taxes", "is_group": 0}
	)
	payable_account = frappe.get_value("Company", settings.company, "default_payable_account")
	je = frappe.new_doc("Journal Entry")
	je.entry_type = "Journal Entry"
	je.company = settings.company
	je.posting_date = settings.day
	je.due_date = settings.day
	total_payroll = 0.0
	for idx, emp in enumerate(emps):
		employee_name = frappe.get_value(
			"Employee", {"company": settings.company, "name": emp.name}, "employee_name"
		)
		je.append(
			"accounts",
			{
				"account": payroll_account,
				"bank_account": frappe.get_value("Bank Account", {"account": settings.company_account}),
				"party_type": "Employee",
				"party": emp.name,
				"cost_center": cost_center,
				"account_currency": "USD",
				"credit": 1000.00,
				"credit_in_account_currency": 1000.00,
				"debit": 0.00,
				"debit_in_account_currency": 0.00,
				"user_remark": employee_name + " Paycheck",
				"idx": idx + 2,
			},
		)
		total_payroll += 1000.00
	je.append(
		"accounts",
		{
			"account": salary_account,
			"cost_center": cost_center,
			"account_currency": "USD",
			"credit": 0.00,
			"credit_in_account_currency": 0.00,
			"debit": total_payroll,
			"debit_in_account_currency": total_payroll,
			"idx": 1,
		},
	)
	je.append(
		"accounts",
		{
			"account": payroll_expense,
			"cost_center": cost_center,
			"account_currency": "USD",
			"credit": 0.00,
			"credit_in_account_currency": 0.00,
			"debit": total_payroll * 0.15,
			"debit_in_account_currency": total_payroll * 0.15,
		},
	)
	je.append(
		"accounts",
		{
			"account": payable_account,
			"cost_center": cost_center,
			"party_type": "Supplier",
			"party": tax_authority[0][0],
			"account_currency": "USD",
			"credit": total_payroll * 0.15,
			"credit_in_account_currency": total_payroll * 0.15,
			"debit": 0.00,
			"debit_in_account_currency": 0.0,
		},
	)
	je.save()
	je.submit()


"""
Set in check run settings
check_run.test_setup.example_post_processing_hook
"""


def example_post_processing_hook(check_run, settings, nacha) -> str:
	# 	check_run: "CheckRun", settings: "CheckRun Settings", nacha: "NACHAFile" # noqa: F722
	b = "$$AAPAACH0094[TEST[NL$$\n"
	a = str(nacha)
	return b + a


def create_extra_invoices(settings):
	day = settings.day
	for next_day in range(0, 365):
		_day = settings.day + datetime.timedelta(days=next_day)
		print(_day)
		if _day.weekday in (5, 6):
			continue

		for supplier in suppliers:
			if supplier[0].startswith("Tireless"):
				continue
			if frappe.get_value("Purchase Invoice", {"posting_date": _day, "supplier": supplier[0]}):
				continue
			pi = frappe.new_doc("Purchase Invoice")
			pi.company = settings.company
			pi.set_posting_time = 1
			pi.posting_date = _day
			pi.supplier = supplier[0]
			pi.append(
				"items",
				{
					"item_code": supplier[1],
					"rate": supplier[3],
					"qty": 1,
				},
			)
			pi.save()
			pi.submit()


def create_manual_payment_entry(settings):
	frappe.db.commit()
	party = "Cooperative Ag Finance"
	to_pay = 1000.00
	docs = frappe.get_all(
		"Purchase Invoice",
		{"supplier": party, "grand_total": [">=", to_pay]},
		order_by="name ASC",
		limit=1,
	)
	pi = frappe.get_doc("Purchase Invoice", docs[0])
	# pi = frappe.get_doc(
	# 	"Purchase Invoice",
	# 	{"supplier": party, "grand_total": [">=", 5000], "posting_date": ["<=", settings.day]}
	# )  # posting date filter not working in runtime
	pe = frappe.new_doc("Payment Entry")
	pe.payment_type = "Pay"
	pe.posting_date = add_days(settings.day, 2)
	pe.mode_of_payment = "Bank Draft"
	pe.company = settings.company
	pe.bank_account = frappe.get_value("Bank Account", {"account": settings.company_account})
	pe.paid_from = settings.company_account
	pe.paid_to = frappe.get_value(
		"Account", {"company": settings.company, "name": ["like", "%Accounts Payable%"]}
	)
	pe.paid_to_account_currency = frappe.get_value(
		"Account", settings.company_account, "account_currency"
	)
	pe.paid_from_account_currency = pe.paid_to_account_currency
	pe.reference_no = "via Bank Draft " + str(pe.posting_date)
	pe.reference_date = pe.posting_date
	pe.party_type = "Supplier"
	pe.party = party
	pe.paid_amount = to_pay

	pe.append(
		"references",
		{
			"reference_doctype": pi.doctype,
			"reference_name": pi.name,
			"due_date": pi.due_date,
			"total_amount": flt(pi.grand_total),
			"outstanding_amount": flt(pi.outstanding_amount),
			"allocated_amount": to_pay,
		},
	)
	pe.received_amount = to_pay
	pe.base_received_amount = to_pay
	pe.paid_amount = to_pay
	pe.base_paid_amount = to_pay
	pe.base_grand_total = to_pay

	pe.save()
	pe.submit()


def create_customers(settings=None):
	for customer in customers:
		c = frappe.new_doc("Customer")
		c.customer_name = customer[0]
		c.customer_group = "Commercial"
		c.customer_type = "Company"
		c.territory = "United States"
		c.save()

		addr = frappe.new_doc("Address")
		addr.address_title = f"{customer[0]} - {customer[1]['city']}"
		addr.address_type = "Billing"
		addr.address_line1 = customer[1]["address_line1"]
		addr.city = customer[1]["city"]
		addr.state = customer[1]["state"]
		addr.country = customer[1]["country"]
		addr.pincode = customer[1]["pincode"]
		addr.append("links", {"link_doctype": "Customer", "link_name": c.name})
		addr.save()


def modify_tax_templates(settings=None):
	frappe.db.sql_ddl("truncate `tabSales Taxes and Charges Template`")
	frappe.db.sql_ddl("truncate `tabPurchase Taxes and Charges Template`")
	frappe.db.sql_ddl("truncate `tabItem Tax Template`")
	# frappe.delete_doc("Account", "ST 6.25% - CFC")
	# frappe.delete_doc("Account", "ST 4% - CFC")
	for st in sales_tax_templates:
		frappe.get_doc(**st).insert()


def create_sales_invoices(settings):
	item = frappe.new_doc("Item")
	item.item_code = "Cloudberry"
	item.item_group = "Products"
	item.stock_uom = "Nos"
	item.maintain_stock = 1
	item.is_sales_item = 1
	item.is_sub_contracted_item, item.include_item_in_manufacturing = 0, 0
	item.grant_commission = 0
	item.is_purchase_item = 1
	item.append(
		"item_defaults",
		{"company": settings.company, "default_warehouse": ""},
	)
	item.save()

	se = frappe.new_doc("Stock Entry")
	se.posting_date = settings.day
	se.set_posting_time = 1
	se.stock_entry_type = "Material Receipt"
	se.append(
		"items",
		{
			"item_code": "Cloudberry",
			"t_warehouse": "Stores - CFC",
			"qty": 1000,
			"uom": "Nos",
			"stock_uom": "Nos",
			"conversion_factor": 1,
			"basic_rate": 0.65,
			"expense_account": "1910 - Temporary Opening - CFC",
		},
	)
	se.save()
	se.submit()

	for customer in customers:
		si = frappe.new_doc("Sales Invoice")
		si.customer = customer[0]
		si.set_posting_time = 1
		si.company = settings.company
		si.posting_date = settings.day
		si.append("items", {"item_code": "Cloudberry", "qty": 100, "rate": 1.30})
		si.taxes_and_charges = "MA Sales Tax - CFC"
		# this API is typically only called from the browser
		taxes = frappe.call(
			"erpnext.controllers.accounts_controller.get_taxes_and_charges",
			**{
				"master_doctype": "Sales Taxes and Charges Template",
				"master_name": si.taxes_and_charges,
			},
		)
		for tax in taxes:
			si.append("taxes", tax)
		si.save()
		# si.submit()
