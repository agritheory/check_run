// Copyright (c) 2026, AgriTheory and contributors
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
	before_workflow_action: async frm => {
		if (frm.selected_workflow_action == 'Void') {
			await set_void_as_of_date(frm)
		}
		return
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

async function set_void_as_of_date(frm) {
	let values = await void_as_of_date_dialog(frm)
	frm.set_value('voided_date', values.as_of_date)
	cur_dialog.hide()
}

function void_as_of_date_dialog(frm) {
	return new Promise(resolve => {
		let dialog = new frappe.ui.Dialog({
			title: __('Select the As-Of Date to Void Payment Entry'),
			fields: [
				{
					fieldtype: 'Date',
					label: __('Void As-Of Date'),
					fieldname: 'as_of_date',
					default: moment(),
				},
			],
			primary_action: function () {
				let as_of_date = dialog.get_value('as_of_date')
				if (!as_of_date) {
					as_of_date = moment()
				}

				if (as_of_date < frm.doc.posting_date) {
					frappe.throw(__("Void As Of Date cannot be before the Payment Entry's posting date."))
				}

				frappe
					.xcall('check_run.overrides.payment_entry.set_voided_date', {
						doctype: frm.doc.doctype,
						docname: frm.doc.name,
						voided_date: as_of_date,
					})
					.then(r => {
						resolve({
							as_of_date: as_of_date,
						})
					})
			},
			primary_action_label: __('Set Date'),
		})
		dialog.show()
		frappe.dom.unfreeze()
	})
}
