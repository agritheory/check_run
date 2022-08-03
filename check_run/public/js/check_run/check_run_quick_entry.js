frappe.provide('frappe.ui.form')

frappe.ui.form.CheckRunQuickEntryForm = frappe.ui.form.QuickEntryForm.extend({
	init: function (doctype, after_insert) {
		this._super(doctype, after_insert)
	},
	render_dialog: function() {
		this.mandatory = this.get_fields()
		this._super()
		this.dialog.$wrapper.find('.btn-secondary').hide()
		this.dialog.fields_dict["bank_account"].get_query = () => {
			return {
				"filters": {
					"company": this.dialog.get_field("company").value,
				}
			}
		}
		this.dialog.fields_dict["pay_to_account"].get_query = () => {
			return {
				"filters": {
					"company": this.dialog.get_field("company").value,
					'account_type': 'Payable'
				}
			}
		}
		this.dialog.fields_dict["company"].df.onchange = () => {
			this.default_accounts()
		}
		this.default_accounts()
	},
	get_fields: function() {
		return [
			{
				label: __("Company"),
				fieldname: "company",
				fieldtype: "Link",
				options: "Company",
				reqd: 1,
			},
			{
				label: __("Paid From (Bank Account"),
				fieldname: "bank_account",
				fieldtype: "Link",
				options: "Bank Account",
				reqd: 1
			},
			{
				label: __("Payable Account"),
				fieldname: "pay_to_account",
				fieldtype: "Link",
				options: "Account",
				reqd: 1
			}
		]
	},
	register_primary_action: function() {
		const me = this
		this.dialog.set_primary_action(__('Start Check Run'), () => {
			let values = me.dialog.get_values()
			frappe.xcall("check_run.check_run.doctype.check_run.check_run.check_for_draft_check_run",
				{ company: values.company, bank_account: values.bank_account }
			).then(r => {
				frappe.set_route("Form", "Check Run", r)
			})
		})
	},
	default_accounts: function() {
		let company = this.dialog.fields_dict.company.get_value()
		frappe.db.get_value('Company', company, 'default_payable_account')
		.then(r => {
			this.dialog.fields_dict["pay_to_account"].set_value(r.message.default_payable_account)
		})
		frappe.db.get_value('Bank Account', {company: company, is_default: 1, is_company_account: 1}, 'name')
		.then(r => {
			this.dialog.fields_dict["bank_account"].set_value(r.message.name)
		})
	}
})
