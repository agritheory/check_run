import CheckRun from './CheckRun.vue'

frappe.provide('check_run')

check_run.mount_table = frm => {
	frm.check_run_state = Vue.observable({
		transactions: frm.transactions,
		party_filter: "",
		docstatus: frm.doc.docstatus,
		modes_of_payment: frm.modes_of_payment,
		show_party_filter: false
	})
	if (frm.$check_run instanceof Vue) {
		frm.$check_run.$destroy();
	}
	$('#check-run-vue').remove()
	$(frm.fields_dict['check_run_table'].wrapper).html($("<div id='check-run-vue'></div>").get(0));
	frm.$check_run = new window.Vue({
		el: $("#check-run-vue").get(0),
		render: h => h(
			CheckRun,
			{ props: {
				transactions: frm.check_run_state.transactions, //list of transtactions
				modes_of_payment: frm.check_run_state.modes_of_payment, // populate modes_of_payment select. doesn't get updated
				docstatus: frm.check_run_state.docstatus, // used to conditionally render column inputs based on submission status. doesn't get updated
				state: frm.check_run_state
			}
		})
	})


}
