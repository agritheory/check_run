<!-- Copyright (c) 2026, AgriTheory and contributors
For license information, please see license.txt-->

# Sales Tax Remittance Report

<div class="byline">
  Tyler Matteson 2026-04-01
</div>


The Sales Tax Remittance Report provides a running view of collected sales tax obligations and their remittance status. It is designed for businesses that track sales tax payable to government authorities via the Sales Taxes and Charges table on their Sales Invoices (see [Sales Tax Payable](./sales_tax_payable.md)).

To access the report, type "Sales Tax Remittance" into the AwesomeBar. Required filters are Company and Up To Date. Unlike most date-range reports, no start date is required — sales tax is managed on a rolling basis and older liabilities remain visible until remitted. Optional filters include Tax Authority, Tax Account, Remittance Status (`Outstanding`, `Remitted`, or `All`), and Show Detail.

## Summary View (default)

Aggregates tax by authority, account, and calendar month. Each row shows the gross tax collected from customers (`total_collected`), how much of that has been received from customers (`customer_paid_amount`), how much has been remitted to the authority (`total_remitted`), and the net amount still owed (`total_outstanding`). Return invoice credits appear as negative values and reduce `total_outstanding` accordingly.

## Detail View

Shows one row per Sales Taxes and Charges entry. In addition to the amounts above, each row links to the originating Sales Invoice, shows whether the customer has paid (`customer_paid`), and — once remitted — shows the remittance amount, the Payment Entry voucher, and the remittance date.

## Returns and Credits

When a Sales Invoice return is submitted, the original invoice's tax row outstanding is reduced to `0` and the return invoice carries a negative outstanding representing a credit owed back from the authority. Both rows appear in the report. See [Sales Tax Payable](./sales_tax_payable.md) for configuration recommendations around returns.
