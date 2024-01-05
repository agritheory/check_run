
frappe.listview_settings['Payment Entry'] = {
    has_indicator_for_draft: 1,
	has_indicator_for_cancelled: 1,
	get_indicator: function (doc) {
		if (doc.status) {
			return [__(doc.status), {
				"Draft": "orange",
				"Submitted": "green",
				"Cancelled": "gray",
				"Voided": "purple"
			}[doc.status], "status,=," + doc.status]
		} else {
			return [__("Not Set"), "blue", "status,=,'Not Set'"]
		}
	}
}