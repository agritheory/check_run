// Copyright (c) 2023, AgriTheory and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Payables Attachments"] = {
	"filters": [

	],
	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (data && column.fieldname == 'attachments') {
			value = `<a onclick="pdf_preview('${data['file_url']}')">${value}</a>`
		}
		return value
	},
};

if ($('#pdf-preview-wrapper').length == 0) {
	$('.page-body .page-wrapper').append(`<div id="pdf-preview-wrapper">
	<button class="btn btn-secondary btn-default btn-sm" id='close-pdf-button'>Close PDF Preview</button>
	</div>`)

	$('#close-pdf-button').on('click', event => {
		$('#pdf-preview').remove()
		$('.page-body').removeClass('show-pdf-preview')
	})
}

function pdf_preview(file_url) {
	if (localStorage.container_fullwidth != 'false') {
		$('#pdf-preview-wrapper').addClass('pdf-preview-wrapper-fw')
	} else {
		$('#pdf-preview-wrapper').removeClass('pdf-preview-wrapper-fw')
	}
	$('#pdf-preview-wrapper').append(`<iframe id="pdf-preview" src="${file_url}">`)
	$('.page-body').addClass('show-pdf-preview')
}
