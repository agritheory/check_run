// Copyright (c) 2025, AgriTheory and contributors
// For license information, please see license.txt

import CheckRun from './CheckRun.vue'
import { createApp, reactive, ref, unref } from 'vue'

frappe.provide('check_run')

check_run.transactions = reactive({})
check_run.selectedRow = ref(-1)
check_run.modes_of_payment = ref([])
check_run.filters = reactive({
	key: 'posting_date',
	posting_date: 1,
	mode_of_payment: 1,
	amount: 1,
	due_date: 1,
	party: '',
})

check_run.get_entries = frm => {
	return new Promise(function (resolve, reject) {
		if (!frm) {
			resolve()
		}
		frappe.xcall('check_run.check_run.doctype.check_run.check_run.get_entries', { doc: frm.doc }).then(r => {
			r.transactions.forEach((row, index) => {
				check_run.transactions[row.name] = row
				check_run.transactions[row.name].idx = index
			})
			check_run.modes_of_payment = r.modes_of_payment
			resolve()
		})
	})
}

check_run.mount = frm => {
	return new Promise(async (resolve, reject) => {
		try {
			check_run.transactions = reactive({})
			check_run.modes_of_payment = ref([])
			check_run.filters = reactive({
				key: 'posting_date',
				posting_date: 1,
				mode_of_payment: 1,
				amount: 1,
				due_date: 1,
				party: '',
			})

			if (frm.$check_run != undefined && frm.$check_run._isVue) {
				frm.$check_run.unmount()
			}

			await check_run.get_entries(frm)
			$(frm.fields_dict['check_run_table'].wrapper).html($("<div id='check-run-vue'></div>").get(0))
			frm.$check_run = createApp(CheckRun)
			frm.$check_run.provide('$check_run', check_run)
			frm.$check_run.mount('#check-run-vue')

			const { nextTick } = await import('vue')
			await nextTick()
			await new Promise(resolve => requestAnimationFrame(resolve))

			resolve()
		} catch (error) {
			reject(error)
		}
	})
}

check_run.total = frm => {
	let _frm = unref(frm)
	let r = Object.values(check_run.transactions).reduce((partialSum, t) => {
		return t.pay ? partialSum + t.amount : partialSum
	}, 0)
	_frm.set_value('amount_check_run', r)
	return r
}
