<template>
	<div>
		<ModeOfPaymentSummary :transactions="orderedTransactions" />
		<table class="table table-compact table-hover check-run-table" style="text-align: center; margin: 0">
			<thead>
				<tr>
					<th style="text-align: left" class="col col-sm-2" id="check-run-party-filter">
						<div>
							<span class="party-onclick party-display" v-if="!show_party_filter"
								>Party
								<span class="filter-icon">
									<svg class="icon icon-sm" style="" @click="show_party_filter = !show_party_filter">
										<use class="" href="#icon-filter"></use>
									</svg>
								</span>
							</span>
						</div>
						<div class="party-filter" v-if="show_party_filter">
							<input type="text" class="form-control" v-model="filters.party" />
						</div>
					</th>
					<th class="col col-sm-2">Document</th>
					<th class="col col-sm-2" style="white-space: nowrap; width: 12.49%">
						<span
							@click="
								filters.key = 'posting_date'
								filters.posting_date *= -1
							"
							class="check-run-sort-indicator"
							id="check-run-doc-date-sort">
							Document Date &#11021;</span
						>
					</th>
					<th class="col col-sm-2" tyle="white-space: nowrap; width: 12.49%">
						<span
							@click="
								filters.key = 'mode_of_payment'
								filters.mode_of_payment *= -1
							"
							class="check-run-sort-indicator"
							id="check-run-mop-sort">
							Mode of Payment &#11021;
						</span>
					</th>
					<th class="col col-sm-2">
						<span
							@click="
								filters.key = 'amount'
								filters.amount *= -1
							"
							class="check-run-sort-indicator"
							id="check-run-outstanding-sort">
							Outstanding Amount &#11021;</span
						>
					</th>
					<th class="col col-sm-1">
						<span
							@click="
								filters.key = 'due_date'
								filters.due_date *= -1
							"
							class="check-run-sort-indicator"
							id="check-run-due-date-sort"
							>Due Date &#11021;</span
						>
					</th>
					<th v-if="frm.doc.status == 'Draft'" class="col col-sm-1" style="text-align: left">
						<input
							type="checkbox"
							autocomplete="off"
							class="input-with-feedback reconciliation"
							data-fieldtype="Check"
							v-model="selectAll" /><span>Select All</span>
					</th>
					<th v-else class="col col-sm-1">Check Number | Reference</th>
				</tr>
			</thead>
			<tbody>
				<template v-for="(item, i) in orderedTransactions">
					<tr
						v-if="partyIsInFilter(item.party)"
						:key="i"
						class="checkrun-row-container"
						:class="{ selectedRow: selectedRow == i }"
						tabindex="1"
						@click="selectedRow = i">
						<td style="text-align: left">{{ item.party_name || item.party }}</td>
						<td style="text-align: left; white-space: nowrap">
							<a :href="transactionUrl(item)" target="_blank">
								{{ item.ref_number || item.name }}
							</a>
						</td>
						<td>{{ datetime.str_to_user(item.posting_date) }}</td>
						<td class="mop-onclick">
							<select class="form-control form-select form-select-lg mb-3" @change="onMOPChange($event, item.name)">
								<option v-for="mop in modes_of_payment" :selected="transactions[item.name].mode_of_payment == mop">
									{{ mop }}
								</option>
							</select>
						</td>
						<td>{{ format_currency(item.amount, frm.pay_to_account_currency, 2) }}</td>
						<td>{{ datetime.str_to_user(item.due_date) }}</td>
						<td v-if="frm.doc.status == 'Draft'" style="text-align: left">
							<input
								type="checkbox"
								class="input-with-feedback checkrun-check-box"
								data-fieldtype="Check"
								@change="onPayChange($event, item.name)"
								:checked="transactions[item.name].pay" />Pay
						</td>
						<td v-else>
							<a target="_blank" :href="paymentEntryUrl(item)"> {{ item.payment_entry }}</a>
						</td>
					</tr>
				</template>
			</tbody>
		</table>
	</div>
</template>
<script setup>
import { computed, onMounted, ref, reactive, watch, unref } from 'vue'
import ModeOfPaymentSummary from './ModeOfPaymentSummary.vue'

frappe.provide('check_run')

let transactions = reactive(window.check_run.transactions)
let filters = reactive(window.check_run.filters)
let show_party_filter = ref(false)
let selectAll = ref(false)
let selectedRow = ref()

onMounted(() => {
	window.check_run.get_entries(window.cur_frm)
})

let orderedTransactions = computed(() => {
	let r = unref(
		Object.keys(transactions)
			.sort()
			.reduce((r, k) => ((r[k] = transactions[k]), r), {})
	)
	return Object.values(r).sort((a, b) =>
		a[filters.key] > b[filters.key] ? filters[filters.key] : filters[filters.key] * -1
	)
})

let modes_of_payment = computed(() => {
	return unref(window.check_run.modes_of_payment)
})

let frm = computed(() => {
	return window.cur_frm
})

let datetime = computed(() => {
	return unref(window.frappe.datetime)
})

watch(selectAll, (val, oldVal) => {
	Object.values(transactions).forEach(row => {
		row.pay = val
	})
	check_run.total(frm)
})

function partyIsInFilter(party) {
	if (!party) {
		return
	}
	return filters.party.length < 1 || party.toLowerCase().includes(filters.party.toLowerCase())
}

function transactionUrl(transaction) {
	if (transaction.doctype !== 'Journal Entry') {
		return encodeURI(
			`${frappe.urllib.get_base_url()}/app/${transaction.doctype.toLowerCase().replace(' ', '-')}/${transaction.name}`
		)
	} else {
		return encodeURI(
			`${frappe.urllib.get_base_url()}/app/${transaction.doctype.toLowerCase().replace(' ', '-')}/${
				transaction.ref_number
			}`
		)
	}
}

function onPayChange(event, rowName) {
	transactions[rowName].pay = event.target.checked
	check_run.total(frm)
	if (transactions[rowName].pay && !transactions[rowName].mode_of_payment) {
		frappe.show_alert(__('Please add a Mode of Payment for this row'))
	}
}

function onMOPChange(event, rowName) {
	transactions[rowName].mode_of_payment = modes_of_payment.value[event.target.selectedIndex]
}

function format_currency(v2, currency, decimals) {
	return window.format_currency(v2, currency, decimals)
}

function paymentEntryUrl(transaction) {
	if (!transaction.payment_entry) {
		return ''
	}
	return encodeURI(`${frappe.urllib.get_base_url()}/app/payment-entry/${transaction.payment_entry}`)
}
</script>
<style scoped>
.party-filter {
	margin-top: 5px;
}
.table thead th {
	vertical-align: top;
}
.checkrun-check-box {
	vertical-align: sub; /* weird but this gives the best alignment */
}
.check-run-table td,
.check-run-table th {
	max-height: 1.5rem;
	padding: 0.4rem;
	vertical-align: middle;
}
.table tr.selectedRow {
	background-color: var(--yellow-highlight-color);
}
.table tr {
	height: 50px;
}
</style>
