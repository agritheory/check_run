// Copyright (c) 2022, AgriTheory and contributors
// For license information, please see license.txt

frappe.ui.form.on('Check Run Settings', {
	refresh: frm => {
		frm.set_query('pay_to_account', () => {
			return {
				filters: {
					company: frm.doc.company,
					account_type: 'Payable',
				},
			}
		})
		frm.set_query('bank_account', () => {
			return {
				filters: {
					is_company_account: 1,
					company: frm.doc.company,
				},
			}
		})
		frm.set_query('print_format', () => {
			return {
				filters: {
					disabled: 0,
					doc_type: 'Payment Entry',
				},
			}
		})
		frm.set_query('debtors_address', function () {
			return {
				query: 'frappe.contacts.doctype.address.address.address_query',
				filters: { link_doctype: 'Company', link_name: frm.doc.company },
			}
		})
	},
})
