// Copyright (c) 2025, AgriTheory and contributors
// For license information, please see license.txt
/* eslint-disable */

let changedItems = {}

frappe.query_reports['ACH Prenote'] = {
	filters: [
		{
			fieldname: 'validated_date',
			label: __('Validated Date Before'),
			fieldtype: 'Date',
		},
		{
			fieldname: 'last_used_date',
			label: __('Last Used Date Before'),
			fieldtype: 'Date',
		},
		{
			fieldname: 'ach_account_type',
			label: __('ACH Account Type'),
			fieldtype: 'Select',
			options: ['', 'Checking', 'Savings'],
		},
	],
	onload: reportview => {
		frappe.query_report.page.add_button(
			'Generate File',
			() => {
				generate_ach_prenote()
			},
			{ btn_class: 'btn-success' }
		)
	},
	saveButton: null,
	get_datatable_options(options) {
		return Object.assign(options, {
			getEditor: this.get_editing_object.bind(this),
		})
	},
	get_editing_object(colIndex, rowIndex, value, parent) {
		const control = this.render_editing_input(colIndex, value, parent)
		if (!control) return false
		control.df.change = event => {
			frappe.query_report.page.set_indicator('Unsaved', 'orange')
			changedItems[rowIndex] = event?.currentTarget.value || null
			this.add_save_button(frappe.query_report)
			control.set_focus()
		}
		try {
			return {
				initValue: async value => {
					return control.set_value(value)
				},
				setValue: value => {
					if (!value) {
						return control.get_value()
					} else {
						return control.set_value(value)
					}
				},
				getValue: async () => {
					return control.get_value()
				},
			}
		} catch (error) {
			console.log(error)
		}
	},
	render_editing_input(colIndex, value, parent) {
		const col = frappe.query_report.datatable.getColumn(colIndex)
		let control = null
		control = frappe.ui.form.make_control({
			df: col,
			parent: parent,
			render_input: true,
		})
		control.set_value(value || '')
		control.toggle_label(false)
		control.toggle_description(false)
		return control
	},
	formatter: (value, row, column, data, default_formatter) => {
		value = default_formatter(value, row, column, data)
		if (data && column.fieldname == 'party_name') {
			value = `<a href="/app/${frappe.scrub(data.party_type, '-')}/${data.party}">${data.party_name}</a>`
		}
		return value
	},
	add_save_button: reportview => {
		if (reportview.saveButton) {
			return
		}
		reportview.saveButton = frappe.query_report.page.add_button(
			__('Save Changes'),
			() => {
				let data = []
				let row
				for (const [rowIndex, updated_date] of Object.entries(changedItems)) {
					row = frappe.query_report.data[rowIndex]
					row.account_details_validated = updated_date
					data.push(row)
				}
				frappe
					.xcall('check_run.check_run.report.ach_prenote.ach_prenote.update_validated_dates', { data: data })
					.then(r => {
						reportview.saveButton.remove()
						reportview.saveButton = null
						changedItems = {}
						reportview.data = []
						frappe.query_report.page.set_indicator('', '')
						// this.get_datatable_options(frappe.query_report.datatable.options)
						reportview.refresh()
						frappe.query_report.page.set_indicator('', '')
						frappe.show_alert(__('Updated Validated Dates'), 5)
					})
			},
			{ btn_class: 'btn-primary' }
		)
	},
}

function generate_ach_prenote() {
	return new Promise(resolve => {
		let dialog = new frappe.ui.Dialog({
			title: __('Please provide additional details'),
			fields: [
				{
					label: 'Check Run Settings',
					fieldname: 'check_run_settings',
					fieldtype: 'Link',
					options: 'Check Run Settings',
					reqd: 1,
				},
				{
					fieldtype: 'Currency',
					label: __('ACH Amount'),
					fieldname: 'ach_amount',
					default: 0.05,
					reqd: 1,
				},
				{
					fieldtype: 'Date',
					label: __('Date'),
					fieldname: 'date',
					default: moment().date(0).format(),
					reqd: 1,
				},
				{
					fieldtype: 'Select',
					label: __('Code'),
					fieldname: 'code',
					reqd: 1,
					options: [
						'Checking Credit Live',
						'Checking Credit Prenote',
						'Checking Credit Child Support prenote',
						'Checking Debit Live',
						'Checking Debit Prenote',
						'Checking Debit Child Support prenote',
						'Savings Credit Live',
						'Savings Credit Prenote',
						'Savings Credit Child Support prenote',
						'Savings Debit Live',
						'Savings Debit Prenote',
						'Savings Debit Child Support prenote',
						'Loan Credit Live',
						'Loan Credit Prenote',
					],
				},
			],
			primary_action: () => {
				let values = dialog.get_values()
				dialog.hide()
				frappe
					.xcall('check_run.check_run.report.ach_prenote.ach_prenote.prepare_ach_prenote', {
						check_run_settings: values.check_run_settings,
						ach_amount: values.ach_amount,
						date: values.date,
						code: values.code,
						data: frappe.query_report.data,
					})
					.then(r => {
						if (r && r.success) {
							let params = new URLSearchParams({
								check_run_settings: values.check_run_settings,
								ach_amount: values.ach_amount,
								date: values.date,
								code: values.code,
								request_id: r.request_id || '',
							}).toString()

							window.open(
								`/api/method/check_run.check_run.report.ach_prenote.ach_prenote.download_ach_prenote?${params}`
							)

							setTimeout(() => {
								resolve()
								frappe.query_report.refresh_report()
							}, 1000)
						} else {
							frappe.msgprint(__('Error preparing ACH prenote file'))
							resolve()
						}
					})
			},
			primary_action_label: __('Generate File'),
		})
		dialog.show()
		dialog.get_close_btn()
	})
}
