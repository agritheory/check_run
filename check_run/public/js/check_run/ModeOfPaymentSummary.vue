<template>
	<div>
		<div id="modeOfPaymentSummary" class="row">
			<div v-for="result in results" class="col">
				{{ result.qty }} {{ result.mode_of_payment }}:
				{{ format_currency(result.amount, frm.pay_to_account_currency, 2) }}
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed, defineProps, unref } from 'vue'

frappe.provide('check_run')

let props = defineProps(['transactions'])

let frm = computed(() => {
	return window.cur_frm
})

let results = computed(() => {
	return calculate_totals()
})

function format_currency(v2, currency, decimals) {
	return window.format_currency(v2, currency, decimals)
}

function calculate_totals() {
	let modes_of_payments = aggregate(props.transactions, 'mode_of_payment', 'amount', 'pay')
	console.log(modes_of_payments)
	let results = []
	if (!(frm.value.doc && frm.value.settings)) {
		return
	}
	let number_of_invoices_per_voucher = frm.value.settings.number_of_invoices_per_voucher
	modes_of_payments.forEach(mop => {
		let amounts = mop.amount.filter(elements => {
			return elements !== null
		})
		let qty = `(${amounts.length})`
		if (mop.mode_of_payment == 'Check') {
			qty = `(${amounts.length}/${number_of_invoices_per_voucher})`
		}
		results.push({
			mode_of_payment: mop.mode_of_payment,
			qty: qty,
			amount: amounts.reduce((acc, val) => {
				return acc + val
			}, 0),
		})
	})
	return results.sort((a, b) => {
		let keyA = a.mode_of_payment,
			keyB = b.mode_of_payment
		if (keyA < keyB) return -1
		if (keyA > keyB) return 1
		return 0
	})
}

function aggregate(transactions, groupByField, valueField, filterField) {
	const groups = transactions
		.filter(transaction => transaction[filterField])
		.reduce((accumulator, transaction) => {
			let groupKey = transaction[groupByField]
			const value = transaction[valueField]
			if (!groupKey) {
				groupKey = 'None'
			}
			if (!accumulator[groupKey]) {
				accumulator[groupKey] = {
					[groupByField]: groupKey,
					[valueField]: [],
				}
			}
			accumulator[groupKey][valueField].push(value)
			return accumulator
		}, {})
	return Object.values(groups)
}
</script>
<style scoped>
#modeOfPaymentSummary {
	padding-bottom: 0.7rem;
}
</style>
