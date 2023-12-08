import CheckRun from './CheckRun.vue'
import { createApp, reactive, ref, unref } from 'vue'

frappe.provide('check_run')

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
	if (frm.$check_run != undefined && frm.$check_run._isVue) {
		return
	}
	$(frm.fields_dict['check_run_table'].wrapper).html($("<div id='check-run-vue'></div>").get(0))
	frm.$check_run = createApp(CheckRun)
	frm.$check_run.mount('#check-run-vue')
	frm.$check_run.provide('$check_run', check_run)
}

check_run.total = frm => {
	let _frm = unref(frm)
	let r = Object.values(check_run.transactions).reduce((partialSum, t) => {
		return t.pay ? partialSum + t.amount : partialSum
	}, 0)
	_frm.set_value('amount_check_run', r)
	return r
}
