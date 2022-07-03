import CheckRun from './CheckRun.vue'

frappe.provide('check_run')

check_run.mount_table = (frm, wrapper) => {
	if (frm.$check_run instanceof Vue) { return }
	window.Vue.component('CheckRun', CheckRun)
	const state = Vue.observable({
		transactions: frm.transactions,
		party_filter: "",
		docstatus: frm.doc.docstatus,
		modes_of_payment: frm.modes_of_payment,
		show_party_filter: false
	})
	if (frm.$check_run instanceof Vue) {
		frm.check_run_state.docstatus = frm.doc.docstatus;
		frm.check_run_state.transactions = frm.transactions;
		frm.check_run_state.modes_of_payment = state.modes_of_payment;
		frm.check_run_state.state = state;
		frm.$check_run_vue.$forceUpdate();
		return;
	}

	frm.check_run_state = state;
	frm.$check_run = new window.Vue({
		el: wrapper.get(0),
		render: h => h(
			CheckRun,
			{ props: {
				transactions: state.transactions, //list of transtactions
				modes_of_payment:  state.modes_of_payment, // populate modes_of_payment select. doesn't get updated
				docstatus: state.docstatus, // used to conditionally render column inputs based on submission status. doesn't get updated
				state: state
			} 
		}),
	})
}
// })