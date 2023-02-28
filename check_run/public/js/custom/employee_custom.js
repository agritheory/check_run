frappe.ui.form.on('Employee', {
	onload_post_render: frm => {
		frm.fields_dict.bank_account.$wrapper.find('#bank-account').off().on('click', () => {
			show_bank_account_number(frm)
		})
	},
	refresh: frm => {
		set_required_banking_fields(frm)
	},
	mode_of_payment: frm => {
		set_required_banking_fields(frm)
	}
})

function show_bank_account_number(frm) {
	if (!frm.doc.bank || !frm.doc.bank_account) {
		let msg = `Banking Information has not been set up for this ${frm.doc.doctype}`
		frappe.msgprint(msg, "Bank Information")
	} else {
		frappe.xcall('check_run.check_run.show_bank_account_number', { doctype: frm.doc.doctype, docname: frm.doc.name })
		.then(r => {
			let msg = `Routing Number ${r.routing_number}<br>Account Number: ${r.account_number}`
			frappe.msgprint(msg, "Bank Information")
		})
	}
}

function set_required_banking_fields(frm){
	if(!frm.doc.mode_of_payment){ return }
	frappe.db.get_value('Mode of Payment', frm.doc.mode_of_payment, 'type')
	.then(r => {
		if(r.message.type == 'Electronic'){
			frm.set_df_property('bank', 'reqd', 1)
			frm.set_df_property('bank', 'hidden', 0)
			frm.set_df_property('bank_account', 'reqd', 1)
			frm.set_df_property('bank_account', 'hidden', 0)
		} else {
			frm.set_df_property('bank', 'reqd', 0)
			frm.set_df_property('bank', 'hidden', 1)
			frm.set_df_property('bank_account', 'reqd', 0)
			frm.set_df_property('bank_account', 'hidden', 1)
		}
	})
}
