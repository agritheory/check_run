<!-- Copyright (c) 2026, AgriTheory and contributors
For license information, please see license.txt-->

# Default Permissions and Workflow

<div class="byline">
  AgriTheory, Heather Kusmierz, and Tyler Matteson 2026-02-21
</div>


It's strongly recommended that you set system permissions to limit which users can see and execute a Check Run. The only permission the application enforces is that a user must have a permission level in ERPNext to create payment entries in order to perform a Check Run. Additionally, only the first user to access a draft Check Run doctype can edit it. 

See the [ERPNext documentation page](https://docs.erpnext.com/docs/v13/user/manual/en/setting-up/users-and-permissions) for more information about user and role permissions.

## First User Only
The Check Run doctype only allows a single user to interact with it at a time. The first write-permissioned user on the specific Check Run is allowed to edit, subsequent viewers are not. 

## Only One Draft Check Run Allowed
Only one draft Check Run is allowed per payable/bank account combination. This is intended to minimize double paying bills.

## Role Permissions
Out of the box, Check Run is permissioned the same as Payment Entry. For most small organizations this may be fine, but larger organizations with document approval policies and a desire to limit persons with access to printed checks will likely want to implement additional policies. Check Run print and ACH generation policies are based on permissions for Payment Entry, not on Check Run itself.

## Voidable Payment Entry Workflow
Check Run ships with an optional Voidable Payment Entry Workflow that allows a user an additional option to void a Payment Entry, versus cancelling it. To activate this workflow, navigate to Workflow -> Voidable Payment Entry, and check the "Is Active" box.

While the "Void" and "Cancel" Payment Entry workflows have similar accounting effects in ERPNext, they differ in the date used to reverse the Payment Entry's General Ledger entries and how Payment Ledger entries are handled.

- a normal "Cancel" workflow reverses the GL entries as of the original Payment Entry's posting date as if the payment were never made. Note that if the company has the immutable ledger feature enabled in Accounts Settings, then reverse GL entries are made as of the cancellation date
- the "Void" workflow provides a dialog for the user to specify the void date (which defaults to the current date) and reverses the GL entries as of that date

This helps to indicate a difference in the two scenarios and to preserve an audit trail of when the company learned about an issue with a sent payment.

These distinctions can be important in scenarios when the company sent a valid payment on time, but the recipient didn't received it. Examples include:

- a physical check gets lost or destroyed in the mail
- a physical check arrives, but is then misplaced or damaged
- there's an error in the routing/account information given for an electronic transfer and the transfer goes to the wrong account

For the Payment Ledger, the "Void" workflow follows abehavior is a hybrid between how ERPNext handles cancelled payments when the immutable ledger feature is enabled or not.

- a "Cancel" workflow (without the immutable ledger feature enabled) will find the initial Payment Ledger Entry (PLE), use it to create an offsetting PLE with the same posting date, then "unlink" both. Unlinked PLEs don't show up in any ERPNext reports, so the Accounts Payable Report will show Invoice as outstanding for any report date between the original Invoice posting date and beyond, until another payment is recorded
- a "Cancel workflow" (with the immutable ledger feature enabled) will find the initial Payment Ledger Entry (PLE), use it to create an offsetting PLE with the the current date, then keep both PLEs linked. The Accounts Payable Report will show that the Invoice is paid using a report date up to the cancellation date (report dates after that show the Invoice as outstanding again with aging calculated against the Invoice's due date)
- a "Void" workflow follows the immutable ledger pattern where it doesn't unlink the entries, except that the offsetting PLE uses the user-provided void date for its posting date. This maintains the historical record in the Accounts Payable report that the Invoice were presumed paid from original payment date up to the void date, then report dates after than show the Invoice as outstanding

The following example demonstrates the differences in the accounting entries and the Accounts Payable report results between voiding a Payment Entry vs. cancelling it. It assumes the company doesn't have the immutable ledger feature enabled:

1. On Nov-01, the company creates a Purchase Invoice to Cooperative Ag Finance for $5,000 with Net 30 terms (posting date is Nov-01, due date is Dec-01)

| Date | Account | Party | Debit | Credit |
| :---- | :--------| :----: | -----: | ------: | 
| Nov-01 | Accounts Payable | Cooperative Ag Finance | | $5,000 |
| Nov-01 | Inventory Received But Not Billed |  | $5,000 |  |

2. The company postmarks and mails a physical check for the amount due on Dec-01, and creates a Payment Entry against the Purchase Invoice

| Date | Account | Party | Debit | Credit |
| :---- | :--------| :----: | -----: | ------: | 
| Dec-01 | Accounts Payable | Cooperative Ag Finance | $5,000 |  |
| Dec-01 | Primary Checking |  |  | $5,000 |

On the due date (before payment), the Accounts Payable Report would show the Purchase Invoice as still outstanding and an Age (in days) of zero.

| Posting Date | Party | Voucher Type | Due Date | O/S Amt | Age (Days) |
| :---- | :---- | :---- | :---- | :---- | ----: | :----: |
| Nov-01 | Cooperative Ag Finance | Purchase Invoice | Dec-01 | $5,000 | 0 |

Once the company creates the Payment Entry, the row no longer shows in the Accounts Payable Report when the report's date is set to on or after the payment's posting date.

3. On Dec-31, Cooperative Ag Finance notifies the company that they never received the check. The company's local bank is closed for a bank holiday, so they have to wait until Jan-02 to issue and confirm a stop payment on the check.

a. Below are the General Ledger entries if the company **CANCELS** the Payment Entry - the ledger entries are reversed as of the original posting date, as if the payment were never made:

**Payment Entry is Cancelled**

| Date | Account | Party | Debit | Credit |
| :---- | :--------| :----: | -----: | ------: | 
| Dec-01 | Accounts Payable | Cooperative Ag Finance |  | $5,000 |
| Dec-01 | Primary Checking |  | $5,000 |  |

The Accounts Payable report again shows the original Purchase Invoice as outstanding again, and will do so using any report date on or after the original Purchase Invoice's posting date of Nov-01. Using a report date of Jan-02:

| Report Date | Posting Date | Party | Voucher Type | Due Date | O/S Amt | Age (Days) |
| :----- | :---- | :---- | :---- | :---- | ----: | :----: |
| Jan-02 | Nov-01 | Cooperative Ag Finance | Purchase Invoice | Dec-01 | $5,000 | 32 |

b. Below are the General Ledger entries if the company **VOIDS** the Payment Entry on Jan-02, but uses a voided date of Dec-31 (the day they learned of the lost check) - the ledger entries are reversed as of the voided date:

**Payment Entry is Voided**

| Date | Account | Party | Debit | Credit |
| :---- | :--------| :----: | -----: | ------: | 
| Dec-31 | Accounts Payable | Cooperative Ag Finance |  | $5,000 |
| Dec-31 | Primary Checking |  | $5,000 |  |

The Accounts Payable Report again shows the original Purchase Invoice as outstanding and calculates the same age as the cancelled workflow when using a report date of Jan-02:

| Report Date | Posting Date | Party | Voucher Type | Due Date | O/S Amt | Age (Days) |
| :----- | :---- | :---- | :---- | :---- | ----: | :----: |
| Jan-02 | Nov-01 | Cooperative Ag Finance | Purchase Invoice | Dec-01 | $5,000 | 32 |

However, the Accounts Payable report won't include the Invoice in its results when the report date is between the original payment (Dec-01) and the day prior to voiding payment (Dec-30):

| Report Date | Posting Date | Party | Voucher Type | Due Date | O/S Amt | Age (Days) |
| :----- | :---- | :---- | :---- | :---- | ----: | :----: |
| Dec-30 |  |  |  |  |  |  |
