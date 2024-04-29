frappe.ui.form.on('Purchase Invoice', {
	refresh: frm => {
		frm.trigger('stop_stand_alone_returns')
	},
	company: frm => {
		frm.trigger('stop_stand_alone_returns')
	},
	stop_stand_alon_returns: frm => {
		frappe.model.get_value('Company', frm.doc.company, 'allow_stand_alone_debit_notes', r => {
			if (r.allow_stand_alone_debit_notes == 'No') {
				frm.set_df_property('is_return', 'hidden', 1)
			}
			if (r.allow_stand_alone_debit_notes == 'Yes') {
				frm.set_df_property('is_return', 'hidden', 0)
			}
		})
	},
})
