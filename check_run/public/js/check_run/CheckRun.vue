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
						<span @click="update_sort('posting_date')" class="check-run-sort-indicator" id="check-run-doc-date-sort">
							Document Date &#11021;</span
						>
					</th>
					<th class="col col-sm-2" style="white-space: nowrap; width: 12.49%">
						<span @click="update_sort('mode_of_payment')" class="check-run-sort-indicator" id="check-run-mop-sort">
							Mode of Payment &#11021;
						</span>
					</th>
					<th class="col col-sm-2">
						<span @click="update_sort('amount')" class="check-run-sort-indicator" id="check-run-outstanding-sort">
							Outstanding Amount &#11021;</span
						>
					</th>
					<th class="col col-sm-1">
						<span @click="update_sort('due_date')" class="check-run-sort-indicator" id="check-run-due-date-sort"
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
						:id="i"
						class="checkrun-row-container"
						tabindex="-1"
						@keydown.prevent.down="moveNext"
						@keydown.prevent.up="movePrev"
						@keydown.prevent.space="updateSelectedRow"
						@click="selectedRow = i">
						<td style="text-align: left">{{ item.party_name || item.party }}</td>
						<td style="text-align: left; white-space: nowrap">
							<a :href="transactionUrl(item)" target="_blank">
								{{ item.ref_number || item.name }}
							</a>
							<div v-if="item.attachments && item.attachments.length > 1" style="float: right" class="dropdown show">
								<a
									class="btn btn-default btn-xs dropdown-toggle"
									href="#"
									role="button"
									:id="item.name"
									data-toggle="dropdown"
									aria-haspopup="true"
									aria-expanded="false">
									<i class="fa fa-search"></i>
								</a>
								<div class="dropdown-menu" :aria-labelledby="item.name">
									<a
										v-for="attachment in item.attachments"
										class="dropdown-item"
										href="javascript:;"
										@click="showPreview(attachment.file_url)"
										data-pdf-preview="item"
										>{{ attachment.file_name }}</a
									>
								</div>
							</div>
							<button
								v-if="item.attachments && item.attachments.length == 1"
								style="float: right"
								type="button"
								class="btn btn-secondary btn-xs"
								@click="showPreview(item.attachments)"
								data-pdf-preview="item">
								<i @click="showPreview(item.attachments)" data-pdf-preview="item" class="fa fa-search"></i>
							</button>
						</td>
						<td>{{ datetime.str_to_user(item.posting_date) }}</td>
						<td class="mop-onclick">
							<select
								v-if="frm.doc.status == 'Draft'"
								class="form-control form-select form-select-lg mb-3"
								@change="onMOPChange(frm, $event, item.name)">
								<option v-for="mop in modes_of_payment" :selected="transactions[item.name].mode_of_payment == mop">
									{{ mop }}
								</option>
							</select>
							<span v-else>{{ transactions[item.name].mode_of_payment }}</span>
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
let location = ref(window.location)

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

onMounted(() => {
	window.check_run.get_entries(window.cur_frm)
})

function showPreview(attachment) {
	var file_url = typeof attachment == 'string' ? attachment : attachment[0].file_url
	frappe.ui.addFilePreviewWrapper()
	frappe.ui.pdfPreview(cur_frm, file_url)
}

watch(selectAll, (val, oldVal) => {
	Object.values(transactions).forEach(row => {
		row.pay = val
	})
	check_run.total(frm)
})

watch(location, (val, oldVal) => {
	window.check_run.get_entries(window.cur_frm)
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

function update_sort(key_name) {
	filters.key = key_name
	filters[key_name] *= -1
}

function onMOPChange(frm, event, rowName) {
	transactions[rowName].mode_of_payment = modes_of_payment.value[event.target.selectedIndex]
	frm.dirty()
	frm.page.set_indicator('Unsaved', 'orange')
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

function moveNext(event) {
	event.target.nextElementSibling.focus();
	selectedRow = event.target.nextElementSibling.id;
}

function movePrev(event) {
	event.target.previousElementSibling.focus();
}

function updateSelectedRow(event) {
	selectedRow = event.target.id;
	if (event.target.classList.contains("selectedRow")) {
		event.target.classList.remove("selectedRow");
	}
	else {
		event.target.className  = event.target.className  + " selectedRow";
		event.target.cells[3].firstChild.focus();
	}
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
	vertical-align: sub;
	/* weird but this gives the best alignment */
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
