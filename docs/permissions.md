# Default Permissions and Workflow

It's strongly recommended that you set system permissions to limit which users can see and execute a check run. The only permission the application enforces is that a user must have a permission level in ERPNext to create payment entries in order to perform a check run. Additionally, only the first user to access a draft check run doctype can edit it. 

See the [ERPNext documentation page](https://docs.erpnext.com/docs/v13/user/manual/en/setting-up/users-and-permissions) for more information about user and role permissions.

## First User Only
The Check Run doctype only allows a single user to interact with it at a time. The first write-permissioned user on the specific Check Run is allowed to edit, subsequent viewers are not. 


