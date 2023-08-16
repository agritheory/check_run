// Copyright (c) 2023, AgriTheory and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Payables Attachments"] = {
	"filters": [],
};

frappe.ui.addFilePreviewWrapper()

function pdf_preview(file_url) {
	if (localStorage.container_fullwidth != 'false') {
		$('#pdf-preview-wrapper').addClass('pdf-preview-wrapper-fw')
	} else {
		$('#pdf-preview-wrapper').removeClass('pdf-preview-wrapper-fw')
	}
	$('#pdf-preview-wrapper').append(`<iframe id="pdf-preview" src="${file_url}">`)
	$('.page-body').addClass('show-pdf-preview')
}
