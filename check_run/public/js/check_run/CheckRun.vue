<template>
	<div>
		<ModeOfPaymentSummary :transactions="orderedTransactions" />
		<table class="table table-compact table-hover check-run-table" style="text-align: center; margin: 0">
			<thead>
				<tr>
					<th style="text-align: left" class="col col-sm-2" id="check-run-party-filter">
						<div class="d-flex align-items-center justify-between gap-2">
							<span class="party-onclick party-display"> Party </span>
							<span class="filter-icon" style="cursor: pointer" @click="show_party_filter = !show_party_filter">
								<svg class="icon icon-sm">
									<use class="" href="#icon-filter"></use>
								</svg>
							</span>
						</div>
						<div class="mt-2">
							<input v-if="show_party_filter" type="text" class="form-control" v-model="filters.party" />
						</div>
					</th>
					<th class="col col-sm-2">Document</th>
					<th class="col col-sm-2" style="white-space: nowrap; width: 12.49%">
						<span @click="update_sort('posting_date')" class="check-run-sort-indicator" id="check-run-doc-date-sort">
							Document Date &#11021;</span
						>
					</th>
					<th class="col col-sm-2" style="white-space: nowrap; width: 12.49%">
						<div class="d-flex align-items-center justify-between gap-2">
							<span
								@click="update_sort('mode_of_payment')"
								class="flex-grow-1 check-run-sort-indicator"
								id="check-run-mop-sort">
								Mode of Payment &#11021;
							</span>
							<span class="filter-icon" style="cursor: pointer" @click="show_mop_filter = !show_mop_filter">
								<svg class="icon icon-sm">
									<use href="#icon-filter"></use>
								</svg>
							</span>
						</div>

						<div v-if="show_mop_filter" class="mt-2">
							<select class="form-control form-select form-select-sm" v-model="filters.mode_of_payment_filter">
								<option value="All">All</option>
								<option v-for="mop in modes_of_payment" :key="mop" :value="mop">
									{{ mop === '' ? 'Not Set' : mop }}
								</option>
							</select>
						</div>
					</th>
					<th class="col col-sm-2">
						<span @click="update_sort('amount')" class="check-run-sort-indicator" id="check-run-outstanding-sort">
							Outstanding Amount &#11021;</span
						>
					</th>
					<th class="col col-sm-1">
						<span
							v-if="frm.settings.show_due_date == 'Show Days Past Due'"
							@click="update_sort('due_date')"
							class="check-run-sort-indicator"
							id="check-run-due-date-sort"
							>Days Past Due &#11021;</span
						>
						<span v-else @click="update_sort('due_date')" class="check-run-sort-indicator" id="check-run-due-date-sort"
							>Due Date &#11021;</span
						>
					</th>
					<th
						v-if="['Draft', 'Pending Approval', 'Approved'].includes(frm.doc.status)"
						class="col col-sm-1"
						style="text-align: left">
						<div class="d-flex align-items-center justify-between gap-2">
							<input
								type="checkbox"
								autocomplete="off"
								class="input-with-feedback reconciliation"
								data-fieldtype="Check"
								v-model="selectAll" /><span>Select All</span>
							<span class="filter-icon" style="cursor: pointer" @click="show_paid_filter = !show_paid_filter">
								<svg class="icon icon-sm">
									<use href="#icon-filter"></use>
								</svg>
							</span>
						</div>
						<div v-if="show_paid_filter" class="mt-2">
							<select class="form-control form-select form-select-sm" v-model="filters.paid_filter">
								<option value="All">All</option>
								<option value="Paid">Paid</option>
								<option value="Unpaid">Unpaid</option>
								<option value="On Hold">On Hold</option>
							</select>
						</div>
					</th>
					<th v-else class="col col-sm-1">Check Number | Reference</th>
				</tr>
			</thead>
			<tbody id="tableTransactions">
				<template v-for="(item, i) in orderedTransactions">
					<tr
						:id="i"
						class="checkrun-row-container"
						:class="{ selectedRow: selectedRow == i }"
						tabindex="1"
						@keydown.prevent.esc="handleEsc(item)"
						@keydown.prevent.space="handleSelectRow(i, item)"
						@keydown="handleKeyPress(i, item.name)">
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
								@change="onMOPChange(frm, $event, item.name)"
								:ref="el => (paymentSelects[item.name] = el)"
								:data-select="item.name">
								<option v-for="mop in modes_of_payment" :selected="transactions[item.name].mode_of_payment == mop">
									{{ mop }}
								</option>
							</select>
							<span v-else>{{ transactions[item.name].mode_of_payment }}</span>
						</td>
						<td v-if="item.has_discount">
							{{ format_currency(item.discount_amount, frm.pay_to_account_currency, 2) }}
						</td>
						<td v-else>{{ format_currency(item.amount, frm.pay_to_account_currency, 2) }}</td>
						<td>{{ datetime.str_to_user(item.due_date) }}</td>
						<td v-if="item.on_hold && frm.settings.automatically_release_on_hold_invoices == 0">
							<span style="font-weight: bold">On Hold</span>
						</td>
						<td v-else-if="['Draft', 'Pending Approval', 'Approved'].includes(frm.doc.status)" style="text-align: left">
							<input
								type="checkbox"
								class="input-with-feedback checkrun-check-box"
								data-fieldtype="Check"
								@change="onPayChange($event, item.name)"
								:checked="transactions[item.name].pay"
								:disabled="['Pending Approval', 'Approved'].includes(frm.doc.status)" />Pay
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
import { computed, onMounted, ref, reactive, watch, unref, nextTick } from 'vue'
import ModeOfPaymentSummary from './ModeOfPaymentSummary.vue'

frappe.provide('check_run')

let transactions = reactive(window.check_run.transactions)
let filters = reactive(window.check_run.filters)
let show_party_filter = ref(false)
let show_mop_filter = ref(false)
let show_paid_filter = ref(false)
let selectAll = ref(false)
let selectedRow = computed(() => unref(window.check_run.selectedRow))
let location = ref(window.location)
let paymentSelects = ref({})

let orderedTransactions = computed(() => {
	let arr = Object.values(transactions)

	arr = arr.filter(item => {
		if (!partyIsInFilter(item.party)) return false

		if (filters.mode_of_payment_filter === '') {
			if (item.mode_of_payment) return false
		} else if (
			filters.mode_of_payment_filter &&
			filters.mode_of_payment_filter !== 'All' &&
			item.mode_of_payment !== filters.mode_of_payment_filter
		) {
			return false
		}

		if (filters.paid_filter && filters.paid_filter !== 'All') {
			if (filters.paid_filter === 'Paid' && !item.pay) return false
			if (filters.paid_filter === 'Unpaid' && item.pay) return false
			if (filters.paid_filter === 'On Hold' && !item.on_hold) return false
		}

		return true
	})

	return arr.sort((a, b) => {
		if (a[filters.key] > b[filters.key]) return filters[filters.key]
		if (a[filters.key] < b[filters.key]) return -filters[filters.key]
		return 0
	})
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
	window.check_run.selectedRow.value = -1
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

function handleEsc(item) {
	window.check_run.selectedRow.value = -1
	togglePayUnselect(item)
}

function handleSelectRow(row, item) {
	if (window.check_run.selectedRow.value === -1 || row !== window.check_run.selectedRow.value) {
		togglePaySelect(item, row)
	} else {
		window.check_run.selectedRow.value = -1
		togglePayUnselect(item)
	}
	check_run.total(frm)
}

function handleKeyPress(row, itemName, event) {
	if (selectedRow.value === row) {
		nextTick(() => {
			const select = paymentSelects.value[itemName]
			if (select) {
				select.focus()
				if (['ArrowUp', 'ArrowDown'].includes(event?.key)) {
					const event = new Event('mousedown', { bubbles: true })
					select.dispatchEvent(event)
				}
			}
		})
	}
}

function togglePaySelect(item, row) {
	const rowName = item.name
	if (transactions[rowName].pay) {
		transactions[rowName].pay = false
		return
	}

	transactions[rowName].pay = true
	if (!transactions[rowName].mode_of_payment || transactions[rowName].mode_of_payment === 'None') {
		window.check_run.selectedRow.value = row
		frappe.show_alert(__('Please add a Mode of Payment for this row'))
	}
}

function togglePayUnselect(item) {
	const rowName = item.name
	if (!transactions[rowName].mode_of_payment) transactions[rowName].pay = false
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

.table tr:focus-visible {
	color: var(--text-color);
	border-color: var(--gray-500);
	outline: 0;
	box-shadow: 0 0 0 2px rgba(104, 113, 120, 0.25);
}
</style>
