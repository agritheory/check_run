frappe.ui.form.on('Payment Entry', {
	mode_of_payment: frm => {
		get_next_check_number(frm)
	},
	bank_account: frm => {
		get_next_check_number(frm)
	}
})

function get_next_check_number(frm){
	if (!frm.doc.bank_account) { return }
	if (!frm.doc.mode_of_payment) { return }
	frappe.db.get_value('Bank Account', frm.doc.bank_account, 'check_number')
	.then(r => {
		let check_number = Number(r.message.check_number) + 1
		frm.set_value('reference_no', check_number)
	})
}