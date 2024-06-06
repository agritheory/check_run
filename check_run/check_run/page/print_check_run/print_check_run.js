frappe.pages['print-check-run'].on_page_load = function (wrapper) {
	frappe.ui.make_app_page({
		parent: wrapper,
	})

	let print_view = new frappe.ui.form.PrintView(wrapper)

	$(wrapper).bind('show', () => {
		const route = frappe.get_route()
		const doctype = 'Check Run'
		const docname = route[1]
		if (!frappe.route_options || !frappe.route_options.frm) {
			frappe.model.with_doc(doctype, docname, () => {
				let frm = { doctype: doctype, docname: docname }
				frm.doc = frappe.get_doc(doctype, docname)
				frappe.model.with_doctype(doctype, () => {
					frm.meta = frappe.get_meta(route[1])
					print_view.show(frm)
				})
			})
		} else {
			print_view.frm = frappe.route_options.frm.doctype ? frappe.route_options.frm : frappe.route_options.frm.frm
			frappe.route_options.frm = null
			print_view.show(print_view.frm)
		}
	})
}

frappe.ui.form.PrintView = class {
	constructor(wrapper) {
		this.wrapper = $(wrapper)
		this.page = wrapper.page
		this.make()
	}

	make() {
		this.print_wrapper = this.page.main.empty().html(
			`<div class="print-preview-wrapper"><div class="print-preview">
			${frappe.render_template('print_skeleton_loading')}
				<iframe class="print-format-container" width="100%" height="0" frameBorder="0" scrolling="no">
				</iframe>
			</div>
			<div class="page-break-message text-muted text-center text-medium margin-top"></div>
		</div>
		`
		)

		this.print_settings = frappe.model.get_doc(':Print Settings', 'Print Settings')
		this.setup_menu()
		this.setup_toolbar()
		this.setup_sidebar()
		this.setup_keyboard_shortcuts()
	}

	set_title() {
		this.page.set_title(this.frm.docname)
	}

	setup_toolbar() {
		this.page.set_primary_action(__('Print'), () => this.printit(), 'printer')

		this.page.add_button(__('Full Page'), () => this.render_page('/print_check_run?'), {
			icon: 'full-page',
		})

		this.page.add_button(__('PDF'), () => this.render_pdf(), { icon: 'small-file' })

		this.page.add_button(__('Refresh'), () => this.refresh_print_format(), {
			icon: 'refresh',
		})

		this.page.add_action_icon(
			'file',
			() => {
				this.go_to_form_view()
			},
			'',
			__('Form')
		)
	}

	get_language_options() {
		return frappe.get_languages()
	}

	setup_sidebar() {
		this.sidebar = this.page.sidebar.addClass('print-preview-sidebar')

		this.doctype_to_print = this.add_sidebar_item({
			fieldtype: 'Select',
			fieldname: 'doctype',
			placeholder: 'Payment Entry',
			options: ['Check Run', 'Payment Entry', 'Payment Entry Secondary Format'],
			default: 'Payment Entry',
			change: () => {
				this.preview()
				this.refresh_print_options()
				this.preview()
			},
		}).$input

		this.print_sel = this.add_sidebar_item({
			fieldtype: 'Select',
			fieldname: 'print_format',
			label: 'Print Format',
			options: [this.get_default_option_for_select(__('Select Print Format'))],
			change: () => this.refresh_print_format(),
			default: __('Select Print Format'),
		}).$input

		this.invoices_per_voucher = this.add_sidebar_item({
			fieldtype: 'Int',
			fieldname: 'invoices_per_voucher',
			label: 'Invoices Per Voucher',
			change: () => this.refresh_print_format(),
			default: 5,
			read_only: 1,
		}).$input
	}

	add_sidebar_item(df, is_dynamic) {
		if (df.fieldtype == 'Select') {
			df.input_class = 'btn btn-default btn-sm text-left'
		}

		let field = frappe.ui.form.make_control({
			df: df,
			parent: is_dynamic ? this.sidebar_dynamic_section : this.sidebar,
			render_input: 1,
		})

		if (df.default != null) {
			field.set_input(df.default)
		}

		return field
	}

	get_default_option_for_select(value) {
		return {
			label: value,
			value: value,
			disabled: true,
		}
	}

	setup_menu() {
		this.page.clear_menu()

		this.page.add_menu_item(__('Print Settings'), () => {
			frappe.set_route('Form', 'Print Settings')
		})

		if (this.print_settings.enable_raw_printing == '1') {
			this.page.add_menu_item(__('Raw Printing Setting'), () => {
				this.printer_setting_dialog()
			})
		}

		if (cint(this.print_settings.enable_print_server)) {
			this.page.add_menu_item(__('Select Network Printer'), () => this.network_printer_setting_dialog())
		}
	}

	show(frm) {
		this.frm = frm
		this.set_title()

		let tasks = [this.refresh_print_options, this.preview].map(fn => fn.bind(this))

		return frappe.run_serially(tasks)
	}

	refresh_print_format() {
		this.preview()
	}

	setup_keyboard_shortcuts() {
		this.wrapper.find('.print-toolbar a.btn-default').each((i, el) => {
			frappe.ui.keys.get_shortcut_group(this.frm.page).add($(el))
		})
	}

	preview() {
		let print_format = this.get_print_format()
		if (print_format.print_format_builder_beta) {
			this.preview_beta()
			return
		}

		const $print_format = this.print_wrapper.find('iframe')
		this.$print_format_body = $print_format.contents()
		this.get_print_html(out => {
			if (!out.html) {
				out.html = this.get_no_preview_html()
			}

			this.setup_print_format_dom(out, $print_format)

			const print_height = $print_format.get(0).offsetHeight
			const $message = this.wrapper.find('.page-break-message')

			const print_height_inches = frappe.dom.pixel_to_inches(print_height)
			// if contents are large enough, indicate that it will get printed on multiple pages
			// Maximum height for an A4 document is 11.69 inches
			if (print_height_inches > 11.69) {
				$message.text(__('This may get printed on multiple pages'))
			} else {
				$message.text('')
			}
		})
	}

	get_letterhead() {
		return this.letterhead_selector.val()
	}

	preview_beta() {
		let print_format = this.get_print_format()
		const iframe = this.print_wrapper.find('.preview-beta-wrapper iframe')
		let params = new URLSearchParams({
			doctype: this.frm.doc.doctype,
			name: this.frm.doc.name,
			print_format: print_format.name,
		})
		iframe.prop('src', `/printpreview?${params.toString()}`)
	}

	setup_print_format_dom(out, $print_format) {
		this.print_wrapper.find('.print-format-skeleton').remove()
		let base_url = frappe.urllib.get_base_url()
		let print_css = frappe.assets.bundled_asset('print.bundle.css', frappe.utils.is_rtl(this.lang_code))
		this.$print_format_body.find('html').attr('dir', frappe.utils.is_rtl(this.lang_code) ? 'rtl' : 'ltr')
		this.$print_format_body.find('html').attr('lang', this.lang_code)
		this.$print_format_body.find('head').html(
			`<style type="text/css">${out.style}</style>
			<link href="${base_url}${print_css}" rel="stylesheet">`
		)
		if (this.doctype_to_print.val() == 'Check Run') {
			this.$print_format_body.find('body').html(`<div class="print-format print-format-preview">${out.html}</div>`)
		} else {
			this.$print_format_body.find('body').html(`<div class="print-format print-format-preview"></div>`)

			let $parentDiv = this.$print_format_body.find('.print-format-preview')

			// Use forEach to append each HTML string to the parent div
			out.html.forEach(function (htmlContent) {
				$parentDiv.append(htmlContent)
				$parentDiv.append(`<div class="page-break"></div>`)
			})
		}

		this.show_footer()

		this.$print_format_body.find('.print-format').css({
			display: 'flex',
			flexDirection: 'column',
		})

		this.$print_format_body.find('.page-break').css({
			display: 'flex',
			'flex-direction': 'column',
			flex: '1',
		})

		setTimeout(() => {
			$print_format.height(this.$print_format_body.find('.print-format').outerHeight())
		}, 500)
	}

	hide() {
		if (this.frm.setup_done && this.frm.page.current_view_name === 'print') {
			this.frm.page.set_view(
				this.frm.page.previous_view_name === 'print' ? 'main' : this.frm.page.previous_view_name || 'main'
			)
		}
	}

	go_to_form_view() {
		frappe.route_options = {
			frm: this,
		}
		frappe.set_route('Form', this.frm.doctype, this.frm.docname)
	}

	show_footer() {
		// footer is hidden by default as reqd by pdf generation
		// simple hack to show it in print preview

		this.$print_format_body.find('#footer-html').attr(
			'style',
			`
			display: block !important;
			order: 1;
			margin-top: auto;
			padding-top: var(--padding-xl)
		`
		)
	}

	printit() {
		let me = this

		if (cint(me.print_settings.enable_print_server)) {
			if (localStorage.getItem('network_printer')) {
				me.print_by_server()
			} else {
				me.network_printer_setting_dialog(() => me.print_by_server())
			}
		} else if (me.get_mapped_printer().length === 1) {
			// printer is already mapped in localstorage (applies for both raw and pdf )
			if (me.is_raw_printing()) {
				me.get_raw_commands(function (out) {
					frappe.ui.form
						.qz_connect()
						.then(function () {
							let printer_map = me.get_mapped_printer()[0]
							let data = [out.raw_commands]
							let config = qz.configs.create(printer_map.printer)
							return qz.print(config, data)
						})
						.then(frappe.ui.form.qz_success)
						.catch(err => {
							frappe.ui.form.qz_fail(err)
						})
				})
			} else {
				frappe.show_alert(
					{
						message: __('PDF printing via "Raw Print" is not supported.'),
						subtitle: __('Please remove the printer mapping in Printer Settings and try again.'),
						indicator: 'info',
					},
					14
				)
				//Note: need to solve "Error: Cannot parse (FILE)<URL> as a PDF file" to enable qz pdf printing.
			}
		} else if (me.is_raw_printing()) {
			// printer not mapped in localstorage and the current print format is raw printing
			frappe.show_alert(
				{
					message: __('Printer mapping not set.'),
					subtitle: __('Please set a printer mapping for this print format in the Printer Settings'),
					indicator: 'warning',
				},
				14
			)
			me.printer_setting_dialog()
		} else {
			me.render_page('/print_check_run?', true)
		}
	}

	print_by_server() {
		let me = this
		if (localStorage.getItem('network_printer')) {
			frappe.call({
				method: 'frappe.utils.print_format.print_by_server',
				args: {
					doctype: me.frm.doc.doctype,
					name: me.frm.doc.name,
					printer_setting: localStorage.getItem('network_printer'),
					print_format: me.selected_format(),
					no_letterhead: true,
					letterhead: null,
				},
				callback: function () {},
			})
		}
	}
	network_printer_setting_dialog(callback) {
		frappe.call({
			method: 'frappe.printing.doctype.network_printer_settings.network_printer_settings.get_network_printer_settings',
			callback: function (r) {
				if (r.message) {
					let d = new frappe.ui.Dialog({
						title: __('Select Network Printer'),
						fields: [
							{
								label: 'Printer',
								fieldname: 'printer',
								fieldtype: 'Select',
								reqd: 1,
								options: r.message,
							},
						],
						primary_action: function () {
							localStorage.setItem('network_printer', d.get_values().printer)
							if (typeof callback == 'function') {
								callback()
							}
							d.hide()
						},
						primary_action_label: __('Select'),
					})
					d.show()
				}
			},
		})
	}

	render_pdf() {
		let print_format = this.get_print_format()
		if (print_format.print_format_builder_beta) {
			let params = new URLSearchParams({
				doctype: this.frm.doc.doctype,
				name: this.frm.doc.name,
				print_format: print_format.name,
				letterhead: null,
			})
			let w = window.open(`/api/method/frappe.utils.weasyprint.download_pdf?${params}`)
			if (!w) {
				frappe.msgprint(__('Please enable pop-ups'))
				return
			}
		} else {
			this.render_check_run_pdf('/api/method/check_run.check_run.doctype.check_run.check_run.download_pdf?')
		}
	}

	set_user_lang() {
		console.log(this.language_sel.val())
		this.lang_code = this.language_sel.val()
	}

	render_check_run_pdf(method) {
		let base_url = frappe.urllib.get_base_url()
		let print_css = frappe.assets.bundled_asset('print.bundle.css', frappe.utils.is_rtl(this.lang_code))
		let w = window.open(
			frappe.urllib.get_full_url(`${method}
				doctype=${encodeURIComponent(this.frm.doc.doctype)}
				&name=${encodeURIComponent(this.frm.doc.name)}
				&formattype=${encodeURIComponent(this.doctype_to_print.val())}
				&print_format=${encodeURIComponent(this.print_sel.val())}
				&baseurl=${encodeURIComponent(base_url)}
				&printcss=${encodeURIComponent(print_css)}
				&lang=${encodeURIComponent('en')}`)
		)
	}

	render_page(method, printit = false) {
		let w = window.open(
			frappe.urllib.get_full_url(`${method}
					doctype=${encodeURIComponent(this.frm.doc.doctype)}
					&name=${encodeURIComponent(this.frm.doc.name)}
					&formattype=${encodeURIComponent(this.doctype_to_print)}
					&lang=${encodeURIComponent('en')}`)
		)

		this.get_print_html(out => {
			let base_url = frappe.urllib.get_base_url()
			let print_css = frappe.assets.bundled_asset('print.bundle.css', frappe.utils.is_rtl(this.lang_code))
			w.document.write(`<style type="text/css">.page-break { page-break-after: always; }${out.style}</style>
				<link href="${base_url}${print_css}" rel="stylesheet">`)
			w.document.write(`<div class="print-format print-format-preview">`)
			if (this.doctype_to_print != 'Check Run') {
				out.html.forEach(function (htmlContent) {
					w.document.write(`${htmlContent}`)
				})
			} else {
				w.document.write(`${out.html}`)
			}
			w.document.write(`</div>`)
			w.document.close()
			if (printit) {
				w.print()
			}
		})
		if (!w) {
			frappe.msgprint(__('Please enable pop-ups'))
			return
		}
	}

	get_print_html(callback) {
		let print_format = this.get_print_format()
		if (print_format.raw_printing) {
			callback({
				html: this.get_no_preview_html(),
			})
			return
		}
		if (this._req) {
			this._req.abort()
		}
		this._req = frappe.call({
			method: 'check_run.www.print_check_run.get_html_and_style',
			args: {
				doc: this.frm.doc,
				doctype_to_print: this.doctype_to_print.val(),
				print_format: this.selected_format(),
				no_letterhead: true,
				letterhead: null,
				settings: this.additional_settings,
				_lang: this.lang_code,
			},
			callback: function (r) {
				if (!r.exc) {
					callback(r.message)
				}
			},
		})
	}

	get_no_preview_html() {
		return `<div class="text-muted text-center" style="font-size: 1.2em;">
			${__('No Preview Available')}
		</div>`
	}

	get_mapped_printer() {
		// returns a list of "print format: printer" mapping filtered by the current print format
		let print_format_printer_map = this.get_print_format_printer_map()
		if (print_format_printer_map[this.frm.doctype]) {
			return print_format_printer_map[this.frm.doctype].filter(
				printer_map => printer_map.print_format == this.selected_format()
			)
		} else {
			return []
		}
	}

	get_print_format_printer_map() {
		// returns the whole object "print_format_printer_map" stored in the localStorage.
		try {
			let print_format_printer_map = JSON.parse(localStorage.print_format_printer_map)
			return print_format_printer_map
		} catch (e) {
			return {}
		}
	}

	async refresh_print_options() {
		this.print_formats = frappe.meta.get_print_formats(this.frm.doctype)
		if (this.doctype_to_print.val() == 'Payment Entry') {
			this.print_formats = await frappe.xcall('check_run.www.print_check_run.get_formats', { doctype: 'Payment Entry' })
		}
		if (this.doctype_to_print.val() == 'Payment Entry Secondary Format') {
			this.print_formats = await frappe.xcall('check_run.www.print_check_run.get_formats', {
				doctype: this.frm.docname,
			})
		}
		const print_format_select_val = this.print_sel.val()
		this.print_sel
			.empty()
			.add_options([this.get_default_option_for_select(__('Select Print Format')), ...this.print_formats])
		return this.print_formats.includes(print_format_select_val) && this.print_sel.val(print_format_select_val)
	}

	selected_format() {
		return this.print_sel.val()
	}

	is_raw_printing(format) {
		return this.get_print_format(format).raw_printing === 1
	}

	get_print_format(format) {
		let print_format = {}
		if (!format) {
			format = this.selected_format()
		}

		if (locals['Print Format'] && locals['Print Format'][format]) {
			print_format = locals['Print Format'][format]
		}

		return print_format
	}

	with_letterhead() {
		return cint(this.get_letterhead() !== __('No Letterhead'))
	}

	set_style(style) {
		frappe.dom.set_style(style || frappe.boot.print_css, 'print-style')
	}

	printer_setting_dialog() {
		// dialog for the Printer Settings
		this.print_format_printer_map = this.get_print_format_printer_map()
		this.data = this.print_format_printer_map[this.frm.doctype] || []
		this.printer_list = []
		frappe.ui.form.qz_get_printer_list().then(data => {
			this.printer_list = data
			const dialog = new frappe.ui.Dialog({
				title: __('Printer Settings'),
				fields: [
					{
						fieldtype: 'Section Break',
					},
					{
						fieldname: 'printer_mapping',
						fieldtype: 'Table',
						label: __('Printer Mapping'),
						in_place_edit: true,
						data: this.data,
						get_data: () => {
							return this.data
						},
						fields: [
							{
								fieldtype: 'Select',
								fieldname: 'print_format',
								default: 0,
								options: this.print_formats,
								read_only: 0,
								in_list_view: 1,
								label: __('Print Format'),
							},
							{
								fieldtype: 'Select',
								fieldname: 'printer',
								default: 0,
								options: this.printer_list,
								read_only: 0,
								in_list_view: 1,
								label: __('Printer'),
							},
						],
					},
				],
				primary_action: () => {
					let printer_mapping = dialog.get_values()['printer_mapping']
					if (printer_mapping && printer_mapping.length) {
						let print_format_list = printer_mapping.map(a => a.print_format)
						let has_duplicate = print_format_list.some((item, idx) => print_format_list.indexOf(item) != idx)
						if (has_duplicate) frappe.throw(__('Cannot have multiple printers mapped to a single print format.'))
					} else {
						printer_mapping = []
					}
					dialog.print_format_printer_map = this.get_print_format_printer_map()
					dialog.print_format_printer_map[this.frm.doctype] = printer_mapping
					localStorage.print_format_printer_map = JSON.stringify(dialog.print_format_printer_map)
					dialog.hide()
				},
				primary_action_label: __('Save'),
			})
			dialog.show()
			if (!(this.printer_list && this.printer_list.length)) {
				frappe.throw(__('No Printer is Available.'))
			}
		})
	}
}
