# Default Permissions and Workflow

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

While the "Void" and "Cancel" Payment Entry workflows have similar accounting effects in ERPNext, they differ in the date used to reverse the Payment Entry's General Ledger entries. A normal "Cancel" workflow reverses the GL entries as of the original Payment Entry's posting date as if the payment were never made. The "Void" workflow uses the current date (by default), or the user can change to a specific date in the provided dialog. This helps to indicate a difference in the two scenarios and to preserve an audit trail of when the company learned about an issue with a sent payment.

The distinction can be important in scenarios when the company sent a valid payment on time, but the recipient never received it. Examples include when a physical check gets lost or destroyed in the mail, or there's an error in the account number used for an electronic transfer.

The following tables demonstrate the differences in the accounting entries between voiding a Payment Entry vs. cancelling it. The example assumes the Purchase Invoice posting date was November 1 with Net 30 terms (due on December 1):

1. The company creates a Purchase Invoice to Cooperative Ag Finance for $5,000 on Nov-01 with Net 30 terms (posting date is Nov-01, due date is Dec-01)

| Date | Account | Party | Debit | Credit |
| :---- | :--------| :----: | -----: | ------: | 
| Nov-01 | Accounts Payable | Cooperative Ag Finance | | $5,000 |
| Nov-01 | Inventory Received But Not Billed |  | $5,000 |  |

2. The company postmarks and mails a physical check for the amount due on Dec-01, and creates a Payment Entry against the Purchase Invoice

| Date | Account | Party | Debit | Credit |
| :---- | :--------| :----: | -----: | ------: | 
| Dec-01 | Accounts Payable | Cooperative Ag Finance | $5,000 |  |
| Dec-01 | Primary Checking |  |  | $5,000 |

3. On Dec-31, Cooperative Ag Finance notifies the company that they never received the check. The company's local bank is closed for a bank holiday, so they have to wait until Jan-02 to issue and confirm a stop payment on the check.

Below are the General Ledger entries if the company **CANCELS** the Payment Entry - the ledger entries are reversed as of the original posting date, as if they payment were never made:

**Payment Entry is Cancelled**

| Date | Account | Party | Debit | Credit |
| :---- | :--------| :----: | -----: | ------: | 
| Dec-01 | Accounts Payable | Cooperative Ag Finance |  | $5,000 |
| Dec-01 | Primary Checking |  | $5,000 |  |


Below are the General Ledger entries if the company **VOIDS** the Payment Entry on Jan-02, but uses a voided date of Dec-31 (the day they learned of the lost check) - the ledger entries are reversed as of the voided date:

**Payment Entry is Voided**

| Date | Account | Party | Debit | Credit |
| :---- | :--------| :----: | -----: | ------: | 
| Dec-31 | Accounts Payable | Cooperative Ag Finance |  | $5,000 |
| Dec-31 | Primary Checking |  | $5,000 |  |
