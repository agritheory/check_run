frappe.ui.form.on('Supplier', {
	onload_post_render: frm => {
		frm.fields_dict.bank_account.$wrapper.find('#bank-account').on('click', () => {
			show_bank_account_number(frm)
		})
	},
})

function show_bank_account_number(frm) {
	frappe.xcall('check_run.check_run.show_bank_account_number', { doctype: frm.doc.doctype, docname: frm.doc.name })
	.then(r => {
		let msg = `Routing Number ${r.routing_number}<br>Account Number: ${r.account_number}`
		frappe.msgprint(msg, "Bank Information")
	})
}