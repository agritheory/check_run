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
		// print is only accessible from custom buttom
		$('[data-original-title="Print"]').hide()
		render_page(frm)
		confirm_print(frm)
		if(frm.doc.docstatus > 0){
			frm.set_df_property('initial_check_number', 'read_only', 1)
			frm.set_df_property('final_check_number', 'read_only', 1)
		}
	},
	onload_post_render: frm => {
		frm.page.wrapper.find('.layout-side-section').hide()
		permit_first_user(frm)
		setup_keyboard_navigation(frm)
	},
	end_date: frm => {
		warn_on_field_reset().then(get_entries(frm, true))
	},
	start_date: frm => {
		warn_on_field_reset().then(() => {
			frappe.xcall("get_balance",{	doc: frm.doc})
			.then(() => {
				get_entries(frm, true)
				frm.refresh_field("beg_balance")
			}).fail((f) => {
				console.error(f)
			})
		})
	},
	onload: frm => {
		frm.$check_run = $(frm.fields_dict['html_10'].wrapper)
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
		warn_on_field_reset().then(get_entries(frm, true))
	}
})

function render_page(frm) {
	return new Promise((resolve) => {
		resolve(get_entries(frm, false))
	})
}

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

function get_entries(frm, reload){
	return new Promise((resolve) => {
		frappe.call({
			method: 'check_run.check_run.doctype.check_run.check_run.get_entries',
			args: { doc: frm.doc, reload: reload},
		}).done((r) => {
			// console.log("TRANSACTIONS", r.message.transactions)
			frm.transactions = r.message.transactions.slice(0, 10)
			frm.modes_of_payment = r.message.modes_of_payment
			check_run.mount_table(frm, frm.$check_run)
			if (!frappe.user.has_role(["Accounts Manager"])) {
				frm.disable_form()
				frm.$check_run.css({ 'pointer-events': 'none' })
			}
			resolve()
		}).fail((r) => {
			console.log(r)
			resolve()
		})
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
	if(frm.doc.__islocal && frm.doc.start_date){
		frappe.call({
			method: "set_last_check_number",
			doc: frm.doc,
		}).then((r) => {
			console.log(r)
			frm.refresh_field("last_check")
			frm.refresh_field("initial_check_number")
		}).fail((f) => {
			console.error(f)
		})
	}
}


function setup_keyboard_navigation (frm) {
	const focus_first_row = () => {
		let first_row = frm.$check_run.find(".checkrun-row-container:first")
		$(first_row[0]).focus()
	}
	let focus_next = () => {
		$(document.activeElement).next().focus()
	}
	let focus_prev = () => {
		$(document.activeElement).prev().focus()
	}
	let list_row_focused = () => {
		return $(document.activeElement).is(".checkrun-row-container")
	}
	let check_row = ($row) => {
		let $input = $row.find("input[type=checkbox]")
		$input.click()
	}

	let get_list_row_if_focused = () => list_row_focused() ? $(document.activeElement) : null

	let is_current_page = () => frm.page.wrapper.is(":visible")
	let is_input_focused = () => $(document.activeElement).is("input")

	let handle_navigation = (direction) => {
		if (!is_current_page() || is_input_focused()) return false;

		let $list_row = get_list_row_if_focused()
		if ($list_row) {
			direction === "down" ? focus_next() : focus_prev()
		} else {
			focus_first_row()
		}
	}

	frappe.ui.keys.add_shortcut({
		shortcut: "down",
		action: () => handle_navigation("down"),
		description: __("Navigate down"),
		page: frm.page,
	})

	frappe.ui.keys.add_shortcut({
		shortcut: "up",
		action: () => handle_navigation("up"),
		description: __("Navigate up"),
		page: frm.page,
	})

	frappe.ui.keys.add_shortcut({
		shortcut: "shift+down",
		action: () => {
			if (!is_current_page() || is_input_focused()) return false;
			let $list_row = get_list_row_if_focused();
			check_row($list_row);
			focus_next();
		},
		description: __("Select multiple list items"),
		page: frm.page,
	})

	frappe.ui.keys.add_shortcut({
		shortcut: "shift+up",
		action: () => {
			if (!is_current_page() || is_input_focused()) { return false }
			let $list_row = get_list_row_if_focused()
			check_row($list_row)
			focus_prev()
		},
		description: __("Select multiple list items"),
		page: frm.page,
	})

	frappe.ui.keys.add_shortcut({
		shortcut: "space",
		action: () => {
			let $list_row = get_list_row_if_focused()
			if ($list_row) {
				check_row($list_row)
				return true
			}
			return false
		},
		description: __("Select list item"),
		page: frm.page,
	})

	frappe.ui.keys.add_shortcut({
		shortcut: "c",
		action: () => {
			let $list_row = get_list_row_if_focused()
			if ($list_row) {
				let el = $list_row.find("[data-mop-index]")
				set_mop_input(frm, el, 'Check')
				return true
			}
			return false
		},
		description: __("Select list item"),
		page: frm.page,
	})

	frappe.ui.keys.add_shortcut({
		shortcut: "a",
		action: () => {
			let $list_row = get_list_row_if_focused()
			if ($list_row) {
				let el = $list_row.find("[data-mop-index]")
				set_mop_input(frm, el, 'ACH/EFT')
				return true
			}
			return false
		},
		description: __("Select list item"),
		page: frm.page,
	})

	frappe.ui.keys.add_shortcut({
		shortcut: "e",
		action: () => {
			let $list_row = get_list_row_if_focused()
			if ($list_row) {
				let el = $list_row.find("[data-mop-index]")
				set_mop_input(frm, el, 'ECheck')
				return true
			}
			return false
		},
		description: __("Select list item"),
		page: frm.page,
	})
}

function show_mop_input(frm, el) {
	if (el[0].tagName == "SPAN")
		el = $(el[0].parentNode)
	el.find("span").hide()
	el.find("select").show().focus()
	el.find("[data-mop]").unbind('change blur keyup').on("click", (e) => {
		set_mop_input(frm, el, el.children()[0].value)
	}).on("blur", () => {
		el.find("span").show()
		el.find("select").hide()
	})
}

function show_party_filter(frm, el) {
	if (el[0].tagName == "SPAN")
		el = $(el[0].parentNode)
	el.find("span").hide()
	el.find("input").show().focus()
	el.find("#party-input").unbind('change blur keyup').on("keyup", frappe.utils.debounce((e) => {
		if(e.target.value != ''){
			frm.check_run_sort.partyFilter = e.target.value
			let transactions = frm.check_run_state.transactions.filter(row => row.party.toLowerCase().search(e.target.value.toLowerCase()) !== -1)
			frm.$check_run.html(frappe.render_template("check_run", {
				"transactions": frm.check_run_state.transactions, 'modes_of_payment': frm.modes_of_payment
			}))
			//setup_sort_and_filter(frm)
		} else {
			frm.$check_run.html(frappe.render_template("check_run", {
				"transactions": frm.check_run_state.transactions, 'modes_of_payment': frm.modes_of_payment
			}))
			//setup_sort_and_filter(frm)
		}
	}, 400))
	el.on("blur", () => {
		if (!el.find("input").value){
			frm.check_run_sort.partyFilter = ''
			frm.$check_run.html(frappe.render_template("check_run", {
				"transactions": frm.check_run_state.transactions, 'modes_of_payment': frm.modes_of_payment
			}))
			//setup_sort_and_filter(frm)
			el.find("span").show()
			el.find("input").hide()
		}
	})
}

function set_mop_input(frm, el, value){
	frm.check_run_state.transactions[el.data('mopIndex')].mode_of_payment = value
	//$(el.children()[0]).html(value)
	frm.dirty()
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
			render_page(frm)
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


async function warn_on_field_reset(callback){
	await frappe.confirm(
		__("Changing this field will reload transactions"),
		callback
	)
}