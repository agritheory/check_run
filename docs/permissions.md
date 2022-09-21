# Default Permissions and Workflow

It's strongly recommended that you set system permissions to limit which users can see and execute a Check Run. The only permission the application enforces is that a user must have a permission level in ERPNext to create payment entries in order to perform a Check Run. Additionally, only the first user to access a draft Check Run doctype can edit it. 

See the [ERPNext documentation page](https://docs.erpnext.com/docs/v13/user/manual/en/setting-up/users-and-permissions) for more information about user and role permissions.

## First User Only
The Check Run doctype only allows a single user to interact with it at a time. The first write-permissioned user on the specific Check Run is allowed to edit, subsequent viewers are not. 

## Only One Draft Check Run Allowed
Only one draft Check Run is allowed per payable/bank account combination. This is intended to minimize double paying bills.

## Role Permissions
Out of the box, Check Run is permissioned the same as Payment Entry. For most small organizations this may be fine, but larger organizations with document approval policies and a desire to limit persons with access to printed checks will likely want to implement additional policies. Check Run print and ACH generation policies are based on permissions for Payment Entry, not on Check Run itself.
