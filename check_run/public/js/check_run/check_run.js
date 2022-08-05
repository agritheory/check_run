import CheckRun from './CheckRun.vue'
import ADropdown from './ADropdown.vue'

frappe.provide('check_run')

check_run.mount_table = frm => {
	check_run.frm = frm
	frm.transactions.forEach(val => {
		val.mopIsOpen = false
		val.pay = val.pay ? val.pay : false
	})
	frm.check_run_state = Vue.observable({
		transactions: frm.transactions,
		party_filter: "",
		docstatus: frm.doc.docstatus,
		modes_of_payment: frm.modes_of_payment,
		show_party_filter: false,
		check_run_total: function() {
			return this.transactions.reduce((partialSum, t) => {
				return t.pay ? partialSum + t.amount : partialSum
			}, 0);
		},
		selectedRow: 0,
		mopsOpen: 0
	})
	if (frm.$check_run instanceof Vue) {
		frm.$check_run.$destroy()
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

check_run.keyDownHandler = e => {
	if(!check_run.frm) {
		return
	}

	if(e.keyCode == 40 && check_run.frm.check_run_state.selectedRow < (check_run.frm.check_run_state.transactions.length - 1)){
		for(let j=0;j<check_run.frm.check_run_state.transactions.length;j++) {
			if(check_run.frm.check_run_state.transactions[j].mopIsOpen) {
				return
			}
		}
		document.getElementById(`mop-input-${check_run.frm.check_run_state.selectedRow}`).blur()
		check_run.frm.check_run_state.selectedRow += 1
	}

	if(e.keyCode == 38 && check_run.frm.check_run_state.selectedRow > 0){
		for(let j=0;j<check_run.frm.check_run_state.transactions.length;j++) {
			if(check_run.frm.check_run_state.transactions[j].mopIsOpen) {
				return
			}
		}
		document.getElementById(`mop-input-${check_run.frm.check_run_state.selectedRow}`).blur()
		check_run.frm.check_run_state.selectedRow -= 1
	}

	if(e.keyCode == 32 && check_run.frm.check_run_state.selectedRow != null && check_run.frm.check_run_state.transactions.length){
		e.preventDefault()
		if(check_run.frm.check_run_component) {
			check_run.frm.check_run_component.checkPay()
		}
	}

	if(e.keyCode && e.keyCode >= 65 && e.keyCode <= 90 && check_run.frm.check_run_state.selectedRow != null && check_run.frm.check_run_state.transactions.length){
		check_run.frm.check_run_component.openMopWithSearch(e.keyCode)
	}

}

window.removeEventListener('keydown', check_run.keyDownHandler)
window.addEventListener('keydown', check_run.keyDownHandler)
