<template>
	<div>
		<div id="modeOfPaymentSummary" class="row">
			<div v-for="result in results" class="col">
				({{ result.qty }}) {{ result.mode_of_payment}}: ${{ result.amount }}
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
			results: this.calculate_totals(),
		}
	},
	methods: {
		calculate_totals() {
			let modes_of_payments = this.aggregate(this.transactions, "mode_of_payment", "amount")
			var result = []
			$(modes_of_payments).each(function(index) {
			   	let mode_of_payment = modes_of_payments[index]
			   	result.push({
			   		'mode_of_payment': mode_of_payment.mode_of_payment,
			        'qty': mode_of_payment.amount.length,
			        'amount': mode_of_payment.amount.reduce(function(acc, val) { return acc + val; }, 0)
			   	})
			});
			return result
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
