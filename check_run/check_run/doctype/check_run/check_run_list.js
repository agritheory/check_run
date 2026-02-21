// Copyright (c) 2026, AgriTheory and contributors
// For license information, please see license.txt

frappe.listview_settings['Check Run'] = {
	add_fields: ['status'],
	hide_name_column: true,
	has_indicator_for_draft: 1,
	get_indicator: doc => {
		return [
			__(doc.status),
			{
				Draft: 'red',
				'Pending Approval': 'grey',
				Approved: 'green',
				Submitting: 'orange',
				Submitted: 'blue',
				'Ready to Print': 'purple',
				'Confirm Print': 'yellow',
				Printed: 'green',
			}[doc.status],
			'status,=,' + doc.status,
		]
	},
}
