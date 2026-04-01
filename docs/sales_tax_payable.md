<!-- Copyright (c) 2026, AgriTheory and contributors
For license information, please see license.txt-->

# Sales Tax Payable

<div class="byline">
  Tyler Matteson 2024-04-01
</div>


By noting the Party Type and Party in the Sales Taxes and Charges table of a Sales Invoice, the user can opt to record the Sales Tax as payable and note the party. An Outstanding Amount will be created on submit to track which rows have been satisfied.

In Check Run Settings, set the "Include Tax Payable from Sales Invoices" to create a Check Run with these options. Given the large number of rows that may be included in a given period, enabling the secondary print format feature is recommended.

## Recommended Settings for the Sales Tax Payable Check Run

When creating Check Run Settings for the bank account / Sales Tax Payable account combination, set **Allow stand-alone debit notes?** to **Yes**.

Sales invoice returns create a negative outstanding amount on the corresponding Sales Taxes and Charges row. With this setting enabled, those credit rows appear in the Check Run so the credit can be remitted or netted against future tax payments to the same authority. With the default value of **No**, only positive outstanding amounts are shown and credits from returns will not surface for reconciliation.

## Returns After Tax Has Been Remitted

When a sales invoice is returned after the tax liability has already been paid via a Check Run:

- The original invoice's tax row outstanding amount remains `0` (it was already remitted).
- The return invoice's tax row carries a **negative** outstanding amount equal to the original tax, representing the credit owed back from the tax authority.

This credit row will appear in the next Check Run (with **Allow stand-alone debit notes?** set to **Yes**), where it can be selected to net against other tax remittances or processed as a standalone refund.