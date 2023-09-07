// Copyright (c) 2023, AgriTheory and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports['Payables Attachments'] = {
	filters: [],
}

frappe.ui.addFilePreviewWrapper()

function pdf_preview(file_url) {
	frappe.ui.pdfPreview(cur_frm, file_url)
}
