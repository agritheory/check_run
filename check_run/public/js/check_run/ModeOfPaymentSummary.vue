<template>
	<div>
		<div id="modeOfPaymentSummary" class="row">
			<div v-for="result in results" class="col">
				{{ result.qty }} {{ result.mode_of_payment }}: {{ format_currency(result.amount, pay_to_account_currency, 2) }}
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
		pay_to_account_currency: '',
		status,
	},
	data() {
		return {
			results: [],
		}
	},
	created() {
		this.calculate_totals()
	},
	watch: {
		transactions: {
			handler: function(newValue) {
				if (this.status == 'Draft') {
					this.calculate_totals()
				}
            },
            deep: true
		},
	},
	methods: {
		calculate_totals() {
			let modes_of_payments = this.aggregate(this.transactions, 'mode_of_payment', 'amount', 'pay')
			var results = []
			if(!(cur_frm.doc.bank_account && cur_frm.doc.pay_to_account)){
				return
			}
			frappe.xcall('check_run.check_run.doctype.check_run.check_run.get_check_run_settings', {doc: cur_frm.doc})
				.then(r => {
					if(!r){ return }
					let number_of_invoices_per_voucher = r.number_of_invoices_per_voucher
					$(modes_of_payments).each(function (index) {
						var mode_of_payment = modes_of_payments[index]
						var amounts = mode_of_payment.amount.filter(elements => { return elements !== null })
						if (mode_of_payment.mode_of_payment == 'Check') {
							var qty = `(${amounts.length}/${number_of_invoices_per_voucher})`
						} else {
							var qty = `(${amounts.length})`
						}
						results.push({
							mode_of_payment: mode_of_payment.mode_of_payment,
							qty: qty,
							amount: amounts.reduce(function (acc, val) {
								return acc + val
							}, 0),
						})
					})
					this.results = results.sort(function(a, b) {
						var keyA = a.mode_of_payment, keyB = b.mode_of_payment;
						if (keyA < keyB) return -1
						if (keyA > keyB) return 1
						return 0
					})
				})
		},
		aggregate(arr, on, who, filter) {
			const agg = arr.reduce((a, b) => {
				const onValue = b[on]
				if (b[filter]) {
					var whoValue = b[who]
				} else {
					var whoValue = null
				}

				if (a[onValue]) {
					a[onValue] = {
						[on]: onValue,
						[who]: [...a[onValue][who], whoValue],
					}
				} else {
					a[onValue] = {
						[on]: onValue,
						[who]: [whoValue],
					}
				}
				return a
			}, {})
			return Object.values(agg)
		},
	},
	beforeMount() {
		this.format_currency = format_currency
	},
}
</script>
<style scoped>
#modeOfPaymentSummary {
	padding-bottom: 0.7rem;
}
</style>
