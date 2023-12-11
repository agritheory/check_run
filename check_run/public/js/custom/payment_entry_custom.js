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
	if (!(frm.is_new() || frm.doc.dostatus == 0 || frm.doc.party_type != 'Supplier')) {
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
