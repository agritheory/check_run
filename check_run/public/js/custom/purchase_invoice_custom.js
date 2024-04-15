frappe.ui.form.on('Purchase Invoice', {
	refresh: frm => {
		frappe.call({
			method: 'check_run.overrides.purchase_invoice.get_buying_settings',
			args: {},
			callback: r => {
				if (r.message.allow_stand_alone_debit_notes == 'NO') {
					frm.set_df_property('is_return', 'hidden', 1)
				}
			},
		})
	},
})
