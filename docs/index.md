# Check Run Documentation

The Check Run application extends ERPNext[^1] with several payables-related utilities. These include check run (a single-page payment mechanism), check printing, and a bank-friendly report.

The check run feature collects all outstanding payables for a given company and account head. It defaults to returning payables up to the current date, but this can be adjusted as needed. The user then selects the invoices to pay and the payment method. On submission, the form creates payment entries that post against a specified bank account, and gives the user the option to print checks.

## Installation, Settings, and Configuration

See the following pages for details on installation, settings, and configuration for the Check Run application:

- [Installation Guide](./installationguide.md)
- [Configuring Mode of Payment for Employees and Suppliers](./configuration.md)
- [Check Run Settings](./settings.md)

## Check Run Quick Start

To initiate a check run, search for "Check Run List" in the AwesomeBar, and click the `Add Check Run` button. This opens a dialogue box where the user must select the company, the bank account from which to make the payments, and the payables account head.

Note that a user must have a permission level in ERPNext to create payment entries in order to perform a check run.

![New Check Run dialogue box showing the mandatory fields the user must fill in for Company, Paid From (Bank Account), and Accounts Payable.](./assets/InitiatingCheckRunDialogue.png)

The check run then returns a list of all outstanding payables for the given account. The report shows the party, the invoice document name, the outstanding amount, and the due date. This screen also allows the user to edit the parameters of the run as needed, including the end date, the posting date, and the initial check number.

![Check run parameters and results. The user can edit the Check Run End Date, Posting Date, Initial Check Number, Company, Paid From (Bank Account), and Accounts Payable fields. The Beginning Bank Account Balance, Final Check Number, and Amount in Check Run are calculated. The table shows a list of outstanding payables, with columns for Party, Document, Document Date, Mode of Payment, Outstanding Amount, Due Date, and a check box to Pay.](./assets/CheckRunScreen.png)

The user checks which payables to pay and the mode of payment for each one. The mode of payment dropdown options will correspond to the `Mode of Payment` documents you have set up in your system. You can configure a default mode of payment for each supplier and employee that will then automatically show as the selection in a check run.

![Detail view of the dropdown menu for the mode of payment. Options include ACH/EFT, Bank Draft, Cash, Check, Credit Card, and Wire Transfer.](./assets/ModeOfPayment.png)

When the user submits the check run, payment entries are automatically generated for each party. The user is also given the choice to print checks [(a print format must be in the system)] and save a PDF. [Files are automatically deleted after they have been downloaded.]

## Additional Check Run Features

Follow the links below for more information about Check Run's features:

- [ACH Generation](./achgeneration.md)
- [Render PDF Sequence](./renderpdfsequence.md)
- [Positive Pay Report](./postivepay.md)
- [Example Print Format: Voucher Check](./exampleprint.md)
- [Example Data: Experimenting with Check Run Using Demo Data](./exampledata.md)

[^1]: [ERPNext](https://erpnext.com/) is an open-sourced Enterprise Resource Planning (ERP) software that provides a wide range of business management functionality. Its core features include support for accounting, inventory, manufacturing, customer relationship management (CRM), distribution, and retail.

