// Copyright (c) 2025, AgriTheory and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Entry', {
	mode_of_payment: frm => {
		get_next_check_number(frm)
	},
	bank_account: frm => {
		get_next_check_number(frm)
	},
	onload: frm => {
		load_supplier_default_mode_of_payment(frm)
	},
	refresh: frm => {
		setup_remove_from_check_run(frm)
	},
})

function get_next_check_number(frm) {
	if (!(frm.doc.bank_account || frm.doc.mode_of_payment) || frm.doc.payment_type != 'Pay') {
		return
	}

	frappe.db.get_value('Bank Account', frm.doc.bank_account, 'check_number').then(r => {
		let check_number = Number(r.message.check_number) + 1
		frm.set_value('reference_no', check_number)
	})
}

function load_supplier_default_mode_of_payment(frm) {
	if (frm.doc.dostatus != 0) {
		return
	}
	if (!(frm.is_new() || frm.doc.party_type != 'Supplier')) {
		return
	}
	frappe.db
		.get_value('Supplier', frm.doc.party, 'supplier_default_mode_of_payment')
		.then(async r => {
			frm.set_value('mode_of_payment', r.message.supplier_default_mode_of_payment)
		})
		.then(() => {
			frappe.db
				.get_list(
					'Bank Account',
					{ filters: { is_company_account: 1, allow_quick_check: 1, account: frm.doc.paid_from } },
					'name'
				)
				.then(r => {
					if (r.length) {
						frm.set_value('bank_account', r[0].name)
					}
				})
		})
}

function setup_remove_from_check_run(frm) {
	if (frm.doc.docstatus > 0 && frm.doc.check_run && frm.doc.bank_account) {
		let _doc = frm.doc
		_doc.pay_to_account = frm.doc.paid_to
		frappe.xcall('check_run.check_run.doctype.check_run.check_run.get_check_run_settings', { doc: _doc }).then(r => {
			if (r.allow_removal) {
				frm.add_custom_button(
					__('Remove from Check Run'),
					() => {
						frappe
							.xcall('check_run.overrides.payment_entry.remove_from_check_run', {
								check_run: frm.doc.check_run,
								payment_entry: frm.doc.name,
							})
							.then(r => {
								frm.reload_doc()
							})
					},
					'Actions'
				)
			}
		})
	}
}
