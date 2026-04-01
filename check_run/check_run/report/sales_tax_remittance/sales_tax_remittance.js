// Copyright (c) 2026, AgriTheory and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports['Sales Tax Remittance'] = {
	filters: [
		{
			fieldname: 'company',
			label: __('Company'),
			fieldtype: 'Link',
			options: 'Company',
			default: frappe.defaults.get_user_default('Company'),
			reqd: 1,
		},
		{
			fieldname: 'to_date',
			label: __('Up To Date'),
			fieldtype: 'Date',
			default: frappe.datetime.get_today(),
			reqd: 1,
		},
		{
			fieldname: 'tax_authority',
			label: __('Tax Authority'),
			fieldtype: 'Link',
			options: 'Supplier',
		},
		{
			fieldname: 'tax_account',
			label: __('Tax Account'),
			fieldtype: 'Link',
			options: 'Account',
			get_query: () => {
				const company = frappe.query_report.get_filter_value('company')
				return {
					filters: {
						account_type: 'Tax',
						company: company,
						is_group: 0,
					},
				}
			},
		},
		{
			fieldname: 'remittance_status',
			label: __('Remittance Status'),
			fieldtype: 'Select',
			options: '\nAll\nOutstanding\nRemitted',
			default: 'All',
		},
		{
			fieldname: 'show_detail',
			label: __('Show Detail'),
			fieldtype: 'Check',
			default: 0,
		},
	],
}
