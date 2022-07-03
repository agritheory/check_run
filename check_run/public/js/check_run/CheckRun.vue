<template>
  <div>

    <table class="table table-compact table-hover check-run-table" style="text-align: center; margin: 0;">
    	<thead>
    		<tr>
    			<th
    				style="text-align: left"
    				class="col col-sm-2"
    				id="check-run-party-filter"
    			>
    				<span class="party-onclick party-display">Party</span> <span class="filter-icon"><svg class="icon  icon-sm" style="" @click="toggleShowPartyFilter()">
			<use class="" href="#icon-filter"></use>
		</svg></span>
            <div class="party-filter" v-if="state.show_party_filter">
              <input type="text" class="form-control" v-model="state.party_filter" />
            </div>
    			</th>
    			<th class="col col-sm-2">Document</th>
    			<th class="col col-sm-2" style="white-space: nowrap; width: 12.49%">
    				Document Date
    				<span @click="sortTransactions('posting_date')" class="check-run-sort-indicator" id="check-run-doc-date-sort">&#11021;</span>
    			</th>
    			<th class="col col-sm-2" tyle="white-space: nowrap; width: 12.49%">Mode of Payment
    				<span @click="sortTransactions('mode_of_payment')" class="check-run-sort-indicator" id="check-run-mop-sort">&#11021;</span>
    			</th>
    			<th class="col col-sm-2">
    				Outstanding Amount
    				<span @click="sortTransactions('amount')" class="check-run-sort-indicator" id="check-run-outstanding-sort">&#11021;</span>
    			</th>
    			<th class="col col-sm-1">
    				Due Date
    				<span @click="sortTransactions('due_date')" class="check-run-sort-indicator" id="check-run-due-date-sort">&#11021;</span>
    			</th>
  				<th v-if="state.docstatus < 1" style="min-width:200px; text-align: left">
  					<input type="checkbox" autocomplete="off" class="input-with-feedback reconciliation" data-fieldtype="Check"
  						id="select-all" v-model="selectAll"> Select All</input>
  				</th>
  				<th v-else class="col col-sm-2"> Check Number | Reference </th>
    		</tr>
    	</thead>
    	<tbody>

        <template v-for="(item, i) in transactions">
    		<tr
          v-if="partyIsInFilter(transactions[i].party)"
    			class="checkrun-row-container"
    			tabindex="1"
    		>
    			<td style="text-align: left">{{ transactions[i].party }}</td>
    			<td>
    				<a
    					:href="transactionUrl(i)"
    					target="_blank"
    				>
    					{{ transactions[i].ref_number || transactions[i].name}}
    				</a>
    			</td>
    			<td> {{ transactions[i].posting_date }}	</td>


    			<td
    				class="mop-onclick"
    				:data-mop-index="i"
    			>
    					<select
                v-if="state.docstatus < 1"
    						class="mop-input form-control"
    						:data-mop="transactions[i].mode_of_payment"
                v-model="transactions[i].mode_of_payment"
                @change="markDirty()"
    					>
    					<option></option>
              <template v-for="(mop, j) in modes_of_payment">
                <option :value="modes_of_payment[j].name">{{modes_of_payment[j].name}}</option>
              </template>
    					</select>
    					<span v-else>{{ transactions[i].mode_of_payment }}</span>
    				</td>


    			<td>{{ format_currency(transactions[i].amount, "USD", 2) }}</td>
    			<td>{{ moment(transactions[i].due_date).format("MM/DD/YY") }}</td>
    				<td v-if="state.docstatus < 1" style="text-align: left">
    					<input
    						type="checkbox"
    						class="input-with-feedback checkrun-check-box"
    						data-fieldtype="Check"
                @change="markDirty()"
    						:data-checkbox-index="i"
    						v-model="transactions[i].pay"
    						:id="transactions[i].id" />Pay
    				</td>
    				<td v-else>
    					<a :href="paymentEntryUrl(i)" target="_blank">
    					{{ transactions[i].check_number }}</a></td>
    		</tr>
        </template>

      </tbody>
    </table>


  </div>
</template>
<script>

export default {
	name: 'CheckRun',
	props: ['transactions', 'modes_of_payment', 'docstatus', 'state'],
	data(){
		return {
      selectAll: false,
      sort_order: {
        posting_date: 1,
        mode_of_payment: 1,
        amount: 1,
        due_date: 1
      }
		}
	},
  watch: {
      selectAll: (val, oldVal) => {
          for(let idx = 0;idx < cur_frm.check_run_state.transactions.length; idx++){
            cur_frm.check_run_state.transactions[idx].pay = val;
          }
          cur_frm.dirty();
      }
  },
  methods: {
    transactionUrl: transactionId => {
      if(!this.transactions) {
        return "";
      }
      return encodeURI(frappe.urllib.get_base_url() + "/app/" + this.transactions[transactionId].doctype.toLowerCase().replace(" ", "-") + "/" + thiis.transactions[transactionId].name );
    },
    paymentEntryUrl: transactionId => {
      if(!this.transactions) {
        return "";
      }
      return encodeURI(frappe.urllib.get_base_url() + "/app/payment-entry/" + this.transactions[i].payment_entry );
    },
    sortTransactions(key) {
      this.transactions.sort((a, b) => (a[key] > b[key] ? this.sort_order[key] : this.sort_order[key] * -1));
      this.sort_order[key] *= -1;
    },
    partyIsInFilter(party) {
      return cur_frm.check_run_state.party_filter.length < 1 || party.toLowerCase().includes(cur_frm.check_run_state.party_filter.toLowerCase());
    },
    toggleShowPartyFilter() {
      cur_frm.check_run_state.party_filter = "";
      cur_frm.check_run_state.show_party_filter = !cur_frm.check_run_state.show_party_filter;
    },
    markDirty() {
      cur_frm.dirty();
    }
  },
  beforeMount() {
    this.moment = moment;
    this.format_currency = format_currency;
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
</style>
