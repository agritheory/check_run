// Copyright (c) 2022, AgriTheory and contributors
// For license information, please see license.txt
frappe.ui.form.on("Check Run", {
	validate: frm => {
		if(frm.check_run_state.party_filter.length > 0) {
			frm.check_run_state.party_filter = ""
			frm.check_run_state.show_party_filter = false
			return new Promise(function(resolve, reject) {
				reject(
					frappe.msgprint(__(
							'The document was not saved because a Party filter was present. The Party filter has now been cleared. Please review the document before saving.'
					))
				)
			})
		}
		frm.doc.transactions = JSON.stringify(frm.check_run_state.transactions)
		frm.doc.amount_check_run = frm.check_run_state.check_run_total()
	},
	refresh: frm => {
		frm.layout.show_message('')
		permit_first_user(frm)
		get_defaults(frm)
		set_queries(frm)
		frappe.call({
			method: "ach_only",
			doc: frm.doc,
		}).done(r => {
			if(!r.message.ach_only){
				if(frm.doc.docstatus == 1) {
					if(frm.doc.print_count > 0){
						frm.add_custom_button("Re-Print Checks", () => { reprint_checks(frm) })
					} else {
						frm.add_custom_button("Print Checks", () => { print_checks(frm) })
					}
				}
			}
		})
		get_entries(frm)
		confirm_print(frm)
		if(frm.doc.docstatus > 0){
			frm.set_df_property('initial_check_number', 'read_only', 1)
			frm.set_df_property('final_check_number', 'read_only', 1)
		}
	},
	onload_post_render: frm => {
		frm.page.wrapper.find('.layout-side-section').hide()
		permit_first_user(frm)
	},
	end_date: frm => {
		get_entries(frm)
	},
	start_date: frm => {
		frappe.xcall('check_run.check_run.doctype.check_run.check_run.get_balance',{ doc: frm.doc })
		.then(r => {
			frm.set_value('beg_balance', r)
			get_entries(frm)
		})
	},
	onload: frm => {
		frm.$check_run = undefined
		frm.transactions = []
		frm.check_run_sort = {
			partyInput: '',
			docDate: false,
			mop: false,
			outstanding: false,
			dueDate: false,
		}
	},
	pay_to_account: frm => {
		get_entries(frm)
	}
})

function set_queries(frm){
	frm.set_query("bank_account", function() {
		return {
			"filters": {
				"company": frm.doc.company,
			}
		}
	})
	frm.set_query("pay_to_account", function() {
		return {
			"filters": {
				"account_type": "Payable",
				"is_group": 0
			}
		}
	})
}

function get_entries(frm){
	frappe.xcall('check_run.check_run.doctype.check_run.check_run.get_entries', { doc: frm.doc}
	).then((r) => {
		frm.transactions = r.transactions
		frm.modes_of_payment = r.modes_of_payment
		check_run.mount_table(frm)
		if (!frappe.user.has_role(["Accounts Manager"])) {
			frm.disable_form()
			frm.$check_run.css({ 'pointer-events': 'none' })
		}
	})
}

function total_check_run(frm){
	var total = 0
	for (const [index, row] of frm.check_run_state.transactions.entries()){
		if(row.pay) {
			total += row.amount
		}
	}
	frm.set_value("amount_check_run", Number(total))
}

function get_defaults(frm){
	if(!frm.is_new()){ return }
	frm.set_value('start_date', moment().startOf('week').format())
	frm.set_value('end_date', moment().endOf('week').format())
	frappe.db.get_value('Company', frm.doc.company, ['default_bank_account', 'default_payable_account'])
	.then(r => {
		frm.set_value('bank_account', r.message.default_bank_account)
		frm.set_value('pay_to_account', r.message.default_payable_account)
	})
}

function get_last_check_number(frm){
	//  TODO: refactor to xcall
	if(frm.doc.__islocal && frm.doc.start_date){
		frappe.call({
			method: "set_last_check_number",
			doc: frm.doc,
		}).then((r) => {
			frm.refresh_field("last_check")
			frm.refresh_field("initial_check_number")
		})
	}
}

function permit_first_user(frm){
	let viewers = frm.get_docinfo()['viewers']
	if(!viewers){
		return
	} else if (viewers.current.length == 1 && viewers.current.includes(frappe.session.user)){
		frm.user_lock = frappe.session.user
		return
	} else if(frappe.session.user == frm.user_lock) {
		return
	} else if (frm.user_lock && frappe.session.user != frm.user_lock){
		frm.disable_form()
		frm.$check_run.css({'pointer-events': 'none'})
	}
}

function confirm_print(frm){
	if(frm.doc.status != 'Confirm Print') {return}
	let d = new frappe.ui.Dialog({
		title: __("Confirm Print"),
		fields: [
			{ fieldname: 'ht', fieldtype: 'HTML', options:
			`<button id="confirm-print" class="btn btn-sm btn-success" style="width: 48%">Confirm Print</button>
			<button id="reprint" class="btn btn-sm btn-warning" style="width: 48%; color: white;">Re-Print Checks</button>
			<br><br>`
			},
			{
				fieldname: 'reprint_check_number',
				fieldtype: 'Data',
				label: "New Intial Check Number",
			}
		],
		minimizable: false,
		static: true,
	})
	d.wrapper.find('#confirm-print').on('click', () => {
		frappe.xcall("check_run.check_run.doctype.check_run.check_run.confirm_print", {docname: frm.doc.name})
		.then(() => {
			d.hide()
			frm.reload_doc()
		})
	})
	d.wrapper.find('#reprint').on('click', () => {
		d.fields_dict.reprint_check_number.df.reqd = 1
		let values = cur_dialog.get_values()
		print_checks(frm, values.reprint_check_number || undefined)
		d.hide()
	})
	d.show()
}

function reprint_checks(frm){
	let d = new frappe.ui.Dialog({
		title: __("Re-Print"),
		fields: [
			{
				fieldname: 'ht', fieldtype: 'HTML', options:
					`<button id="reprint" class="btn btn-sm btn-warning" style="width: 48%; color: white;">Re-Print Checks</button><br><br>`
			},
			{
				fieldname: 'reprint_check_number',
				fieldtype: 'Data',
				label: "New Intial Check Number",
			}
		],
		minimizable: false,
		static: true,
	})
	d.wrapper.find('#reprint').on('click', () => {
		d.fields_dict.reprint_check_number.df.reqd = 1
		let values = cur_dialog.get_values()
		print_checks(frm, values.reprint_check_number || undefined)
		d.hide()
	})
	d.show()
}
