<template>
	<div>
		<div id="modeOfPaymentSummary" class="row">
			<div v-for="result in results" class="col">
				{{ result.qty }} {{ result.mode_of_payment}}: ${{ result.amount }}
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: 'ModeOfPaymentSummary',
	props: {
		transactions: {
			type: Array,
			required: true,
			default: () => [],
		},
	},
	data() {
		return {
			results: [],
		}
	},
	created() {
      	this.calculate_totals()
    },
	methods: {
		calculate_totals() {
			let modes_of_payments = this.aggregate(this.transactions, "mode_of_payment", "amount")
			var results = []

			frappe.db.get_value('Check Run Settings', {"bank_account": cur_frm.doc.bank_account, "pay_to_account": cur_frm.doc.pay_to_account}, 'number_of_invoices_per_voucher').then(r => {
				let number_of_invoices_per_voucher = r.message.number_of_invoices_per_voucher
				$(modes_of_payments).each(function(index) {
					var mode_of_payment = modes_of_payments[index]
				   	if (mode_of_payment.mode_of_payment == 'Check') {
				   		var qty = `(${mode_of_payment.amount.length}/${number_of_invoices_per_voucher})`
				   	} else {
				   		var qty = `(${mode_of_payment.amount.length})`
				   	}
				   	results.push({
				   		'mode_of_payment': mode_of_payment.mode_of_payment,
				        'qty': qty,
				        'amount': mode_of_payment.amount.reduce(function(acc, val) { return acc + val; }, 0)
				   	})
				});
				this.results = results
			})
		},
		aggregate(arr, on, who) {
			const agg = arr.reduce((a, b) => {
		    const onValue = b[on];
		    const whoValue = b[who];
		    
		    if (a[onValue]) {
		    	a[onValue] = {
		        	[on]: onValue,
		        	[who]: [...a[onValue][who], whoValue]
		      	}
		    }
		    else {
		   		a[onValue] = {
		        	[on]: onValue,
		        	[who]: [whoValue]
		      	}
		    }
		    return a;
		  }, {});
		  return Object.values(agg);
		}
	},
}
</script>
<style scoped>
#modeOfPaymentSummary {
	padding-bottom: 0.7rem;
}
</style>
