<template>
	<div>
		<ul>
			<li v-for="result in results">
				({{ result.qty }}) {{ result.mode_of_payment}}: ${{ result.amount }}
			</li>
		</ul>
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
			let modes_of_payments = aggregate(this.transactions, "mode_of_payment", "amount")
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
	},
}

const aggregate = (arr, on, who) => {
  // using reduce() method to aggregate 
  const agg = arr.reduce((a, b) => {
    // get the value of both the keys 
    const onValue = b[on];
    const whoValue = b[who];
    
    // if there is already a key present
    // merge its value
    if(a[onValue]){
      a[onValue] = {
        [on]: onValue,
        [who]: [...a[onValue][who], whoValue]
      }
    }
    // create a new entry on the key
    else{
      a[onValue] = {
        [on]: onValue,
        [who]: [whoValue]
      }
    }
    
    // return the aggregation
    return a;
  }, {});
  
  
  // return only values after aggregation 
  return Object.values(agg);
}

</script>

<style>
</style>
