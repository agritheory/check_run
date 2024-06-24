frappe.provide('frappe.ui.form')

$(document).on('page-change', function (e) {
	frappe.ui.closeFilePreview()
})

$(document).on('click', function (e) {
	if (!$(e.target).get(0).hasAttribute('data-pdf-preview')) {
		frappe.ui.closeFilePreview()
	}
})

$(document).on('keydown', e => {
	if (e.which === frappe.ui.keyCode.ESCAPE) {
		frappe.ui.closeFilePreview()
	}
	if (e.which === frappe.ui.keyCode.SPACE && cur_frm && cur_frm.doctype == 'Check Run') {
		frappe.ui.closeFilePreview()
	}
})

$('#close-pdf-button').on('click', event => {
	frappe.ui.closeFilePreview()
})

frappe.ui.form.Attachments.prototype.add_attachment = attachment => {
	const me = frappe.ui.form.Attachments.prototype
	let file_name = attachment.file_name
	var file_url = me.get_file_url(attachment)
	var fileid = attachment.name
	if (!file_name) {
		file_name = file_url
	}
	let file_label = `
			<a href="${file_url}" target="_blank" title="${file_name}" class="ellipsis" style="max-width: calc(100% - 43px);">
				<span>${file_name}</span>
			</a>`
	let remove_action = null
	if (frappe.model.can_write(cur_frm.doctype, cur_frm.name)) {
		remove_action = function (target_id) {
			frappe.confirm(__('Are you sure you want to delete the attachment?'), function () {
				cur_frm.attachments.remove_attachment(target_id)
			})
			return false
		}
	}

	let icon = `<a href="/app/file/${fileid}">
				${frappe.utils.icon(attachment.is_private ? 'lock' : 'unlock', 'sm ml-0')}
			</a>`

	if (file_name.toLowerCase().endsWith('.pdf')) {
		icon += `<i class="fa fa-file-pdf-o" data-pdf-preview="${file_url}"></i>`
	}

	$(`<li class="attachment-row">`)
		.append(frappe.get_data_pill(file_label, fileid, remove_action, icon))
		.insertAfter(cur_frm.attachments.attachments_label.addClass('has-attachments'))

	$('.fa-file-pdf-o').on('click', event => {
		frappe.ui.pdfPreview(cur_frm, event.currentTarget.dataset.pdfPreview)
	})

	if (file_name.toLowerCase().endsWith('.pdf')) {
		frappe.ui.addFilePreviewWrapper(cur_frm)
	}
}

frappe.ui.addFilePreviewWrapper = frm => {
	$('#pdf-preview-wrapper').remove()
	let targetDiv = document.querySelector(`[id='page-${frm.doctype}']`)
	if (targetDiv) {
		let page_body = targetDiv.querySelector('.page-body')
		if (page_body) {
			let page_wrapper = page_body.querySelector('.page-wrapper')

			if (page_wrapper) {
				$(page_wrapper).append(`<div id="pdf-preview-wrapper">
			<button class="btn btn-secondary btn-default btn-sm" id='close-pdf-button'>Close PDF Preview</button>
			</div>`)
			}
		}
	}
}

frappe.ui.closeFilePreview = () => {
	if ($('#pdf-preview').length != 0) {
		$('#pdf-preview').remove()
		$('.page-body').removeClass('show-pdf-preview')
		if (cur_frm !== null && cur_frm.doctype != 'Check Run') {
			cur_frm.page.wrapper.find('.layout-side-section').show()
		}
	}
}

frappe.ui.pdfPreview = (frm, file_url) => {
	if (frm !== null) {
		frm.page.wrapper.find('.layout-side-section').hide()
	}
	if (localStorage.container_fullwidth != 'false') {
		$('#pdf-preview-wrapper').addClass('pdf-preview-wrapper-fw')
	} else {
		$('#pdf-preview-wrapper').removeClass('pdf-preview-wrapper-fw')
	}
	$('#pdf-preview-wrapper').append(`<iframe id="pdf-preview" src="${file_url}">`)
	$('.page-body').addClass('show-pdf-preview')
}
