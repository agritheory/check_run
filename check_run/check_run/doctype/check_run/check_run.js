// Copyright (c) 2022, AgriTheory and contributors
// For license information, please see license.txt

frappe.provide('check_run')

frappe.ui.form.on('Check Run', {
	validate: frm => {
		validate_mode_of_payment_mandatory(frm)
		if (check_run.filters.party.length > 0) {
			check_run.filters.party = ''
			check_run.filters.show_party_filter = false
			return new Promise(function (resolve, reject) {
				reject(
					frappe.msgprint(
						__(
							'The document was not saved because a Party filter was present. The Party filter has now been cleared. Please review the document before saving.'
						)
					)
				)
			})
		}
		frm.doc.transactions = JSON.stringify(check_run.transactions)
	},
	refresh: frm => {
		frm.layout.show_message('')
		frm.trigger('update_primary_action')
		if (frm.doc.__onload && frm.doc.__onload.errors) {
			frm.set_intro(
				__('<a href="" style="color: var(--red)" id="check-run-error">This Check Run has errors, click to view.</a>'),
				'red'
			)
			$('#check-run-error')
				.off()
				.on('click', e => {
					frappe.route_options = { method: ['like', `%${frm.doc.name}%`] }
					frappe.set_route('list', 'Error Log')
					e.stopPropagation()
				})
		}
		settings_button(frm)
		permit_first_user(frm)
		get_defaults(frm)
		set_queries(frm)
		frappe.realtime.off('reload')
		frappe.realtime.on('reload', message => {
			frm.reload_doc()
		})
		if (frm.is_new()) {
			get_balance(frm)
		}
		ach_only(frm)
		get_entries(frm)
		confirm_print(frm)
		if (frm.doc.docstatus > 0) {
			frm.set_df_property('initial_check_number', 'read_only', 1)
			frm.set_df_property('final_check_number', 'read_only', 1)
		}
		check_settings(frm)
	},
	onload_post_render: frm => {
		frm.page.wrapper.find('.layout-side-section').hide()
		permit_first_user(frm)
		frm.trigger('update_primary_action')
		$(frm.wrapper).on('dirty', () => {
			frm.trigger('update_primary_action')
		})
		if (frm.doc.__onload && frm.doc.__onload.check_run_submitting == frm.doc.name) {
			frm.doc.status = 'Submitting'
			frm.page.set_indicator(__('Submitting'), 'orange')
			frm.disable_form()
			cur_frm.$check_run.$children[0].state.status = 'Submitting'
		} else if (frm.doc.__onload && frm.doc.__onload.check_run_submitting) {
			frm.set_intro(
				__(
					`<span style="color: var(--orange)" id="check-run-error">Check Run ${frm.doc.__onload.check_run_submitting} is processing. This Check Run cannot be processed until it completes.</span>`
				),
				'red'
			)
		}
	},
	end_date: frm => {
		get_entries(frm)
	},
	posting_date: frm => {
		get_entries(frm)
	},
	start_date: frm => {
		get_entries(frm)
		get_balance(frm)
	},
	onload: frm => {
		if (frm.doc.__onload.settings) {
			frm.settings = frm.doc.__onload.settings
			frm.pay_to_account_currency = frm.doc.__onload.pay_to_account_currency
		}
	},
	pay_to_account: frm => {
		get_entries(frm)
	},
	bank_account: frm => {
		get_balance(frm)
	},
	process_check_run: frm => {
		frm.layout.show_message('')
		frm.doc.status = 'Submitting'
		frm.page.set_indicator(__('Submitting'), 'orange')
		frm.disable_form()
		frappe.xcall('check_run.check_run.doctype.check_run.check_run.process_check_run', { docname: frm.doc.name })
	},
	update_primary_action: frm => {
		frm.disable_save()
		if (frm.is_dirty()) {
			frm.enable_save()
		} else if ((frm.doc.__onload && frm.doc.__onload.check_run_submitting) || frm.doc.status == 'Submitting') {
			frm.disable_save()
			frm.disable_form()
		} else if (frm.doc.status == 'Draft' && !(frm.doc.__onload && frm.doc.__onload.check_run_submitting)) {
			frm.page.set_primary_action(__('Process Check Run'), () => frm.trigger('process_check_run'))
		}
	},
})

function get_balance(frm) {
	frappe.xcall('check_run.check_run.doctype.check_run.check_run.get_balance', { doc: frm.doc }).then(r => {
		frm.set_value('beg_balance', r)
	})
}

function set_queries(frm) {
	frm.set_query('bank_account', function () {
		return {
			filters: {
				company: frm.doc.company,
			},
		}
	})
	frm.set_query('pay_to_account', function () {
		return {
			filters: {
				account_type: 'Payable',
				is_group: 0,
			},
		}
	})
}

function get_entries(frm) {
	return new Promise(function (resolve, reject) {
		resolve(window.check_run.mount(frm))
	})
}

function total_check_run(frm) {
	var total = 0
	for (const [index, row] of frm.transactions.entries()) {
		if (row.pay) {
			total += row.amount
		}
	}
	frm.set_value('amount_check_run', Number(total))
}

function get_defaults(frm) {
	if (!frm.is_new()) {
		return
	}
	frm.set_value('start_date', moment().startOf('week').format())
	frm.set_value('end_date', moment().endOf('week').format())
}

function get_last_check_number(frm) {
	//  TODO: refactor to xcall
	if (frm.doc.__islocal && frm.doc.start_date) {
		frappe
			.call({
				method: 'set_last_check_number',
				doc: frm.doc,
			})
			.then(r => {
				frm.refresh_field('last_check')
				frm.refresh_field('initial_check_number')
			})
	}
}

function permit_first_user(frm) {
	let viewers = frm.get_docinfo()['viewers']
	if (!viewers) {
		return
	} else if (viewers.current.length == 1 && viewers.current.includes(frappe.session.user)) {
		frm.user_lock = frappe.session.user
		return
	} else if (frappe.session.user == frm.user_lock) {
		return
	} else if (frm.user_lock && frappe.session.user != frm.user_lock) {
		frm.disable_form()
		frm.$check_run.css({ 'pointer-events': 'none' })
	}
}

function confirm_print(frm) {
	if (frm.doc.status != 'Confirm Print') {
		return
	}
	let d = new frappe.ui.Dialog({
		title: __('Confirm Print'),
		fields: [
			{
				fieldname: 'ht',
				fieldtype: 'HTML',
				options: `<button id="confirm-print" class="btn btn-sm btn-success" style="width: 48%">${__(
					'Confirm Print'
				)}</button>
			<button id="reprint" class="btn btn-sm btn-warning" style="width: 48%; color: white;">${__('Re-Print Checks')}</button>
			<br><br>`,
			},
			{
				fieldname: 'reprint_check_number',
				fieldtype: 'Data',
				label: __('New Initial Check Number'),
			},
		],
		minimizable: false,
		static: true,
	})
	d.wrapper.find('#confirm-print').on('click', () => {
		frappe
			.xcall('check_run.check_run.doctype.check_run.check_run.confirm_print', {
				docname: frm.doc.name,
			})
			.then(() => {
				d.hide()
				frm.reload_doc()
			})
	})
	d.wrapper.find('#reprint').on('click', () => {
		d.fields_dict.reprint_check_number.df.reqd = 1
		let values = cur_dialog.get_values()
		render_checks(frm, values.reprint_check_number || undefined)
		frm.doc.status = 'Submitted'
		frm.page.set_indicator(__('Submitted'), 'blue')
		d.hide()
	})
	d.show()
}

function reprint_checks(frm) {
	frm.set_value('status', 'Submitted')
	let d = new frappe.ui.Dialog({
		title: __('Re-Print'),
		fields: [
			{
				fieldname: 'ht',
				fieldtype: 'HTML',
				options: `<button id="reprint" class="btn btn-sm btn-warning" style="width: 48%; color: white;">${__(
					'Re-Print Checks'
				)}</button><br><br>`,
			},
			{
				fieldname: 'reprint_check_number',
				fieldtype: 'Data',
				label: __('New Initial Check Number'),
			},
		],
		minimizable: false,
		static: true,
	})
	d.wrapper.find('#reprint').on('click', () => {
		d.fields_dict.reprint_check_number.df.reqd = 1
		let values = cur_dialog.get_values()
		render_checks(frm, values.reprint_check_number || undefined)
		d.hide()
		frm.reload_doc()
		frm.set_value('status', 'Submitted')
	})
	d.show()
}

function ach_only(frm) {
	frappe
		.xcall('check_run.check_run.doctype.check_run.check_run.ach_only', {
			docname: frm.doc.name,
		})
		.then(r => {
			if (!r.ach_only) {
				if (frm.doc.docstatus == 1) {
					if (frm.doc.print_count > 0 && frm.doc.status != 'Ready to Print') {
						frm.add_custom_button(__('Re-Print Checks'), () => {
							reprint_checks(frm)
						})
					} else if (frm.doc.print_count == 0 && frm.doc.status == 'Submitted') {
						render_checks(frm)
					}
				}
				if (frm.doc.status == 'Ready to Print') {
					frm.add_custom_button(__('Download Checks'), () => {
						download_checks(frm)
					})
				}
			}
			if (!r.print_checks_only) {
				if (frm.doc.docstatus == 1) {
					frm.add_custom_button(__('Download NACHA File'), () => {
						download_nacha(frm)
					})
				}
			}
		})
}

function validate_mode_of_payment_mandatory(frm) {
	let mode_of_payment_required = []
	for (const index in frm.transactions) {
		let row = frm.transactions[index]
		if (row.pay && row.mode_of_payment.length < 2) {
			mode_of_payment_required.push({ row: index + 1, party: row.party, ref_name: row.ref_number || row.name })
		}
	}
	if (mode_of_payment_required.length == 0) {
		return
	}
	let message = ''
	for (const index in mode_of_payment_required) {
		let row = mode_of_payment_required[index]
		message += `<li>Row ${row.row}: ${row.party} - ${row.ref_name}</li>`
	}
	frappe.msgprint({
		message: `<br><br><ul>${message}</ul>`,
		indicator: 'red',
		title: __('Mode of Payment Required'),
		raise_exception: true,
	})
}

function render_checks(frm, reprint_check_number = undefined) {
	frappe
		.call({
			method: 'increment_print_count',
			doc: frm.doc,
			args: { reprint_check_number: reprint_check_number },
		})
		.done(() => {
			frm.reload_doc()
			frm.add_custom_button('Re-Print Checks', () => {
				reprint_checks(frm)
			})
		})
		.fail(r => {
			frm.reload_doc()
		})
}

function download_checks(frm) {
	frappe.xcall('check_run.check_run.doctype.check_run.check_run.download_checks', { docname: frm.doc.name }).then(r => {
		if (r) {
			frm.reload_doc()
			window.open(r)
		}
	})
}

function download_nacha(frm) {
	window.open(`/api/method/check_run.check_run.doctype.check_run.check_run.download_nacha?docname=${frm.doc.name}`)
	window.setTimeout(() => {
		frm.reload_doc()
	}, 1000)
}

function settings_button(frm) {
	frm.add_custom_button('Modify Settings', () => {
		frappe.xcall('check_run.check_run.doctype.check_run.check_run.get_check_run_settings', { doc: frm.doc }).then(r => {
			frappe.set_route('Form', 'Check Run Settings', r.name)
		})
	})
}

function check_settings(frm) {
	if (frm.doc.docstatus < 1 && frm.doc.__onload && frm.doc.__onload.settings_missing) {
		frappe.xcall('check_run.check_run.doctype.check_run.check_run.get_check_run_settings', { doc: frm.doc }).then(r => {
			if (r == undefined) {
				frappe.confirm(
					__(
						`No settings found for <b>${frm.doc.bank_account}</b> and <b>${frm.doc.pay_to_account}</b>. Would you like to review these settings?`
					),
					() => {
						frappe.set_route('Form', 'Check Run Settings', r)
					},
					() => {} //stay on this page
				)
			} else {
				frm.doc.__onload.settings_missing = false
			}
		})
	}
}
