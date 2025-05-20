<!-- Copyright (c) 2025, AgriTheory and contributors
For license information, please see license.txt-->

# ACH Generation and Prenote

For electronic bank transfers, banking institutions require specifically-formatted plain-text files to encode all necessary information. This includes data about the type of payment, the parties, their bank accounts, and payment amounts. These files conform to Automated Clearing House (ACH) standards, which is an electronic-funds transfer system run by the National Automated Clearing House Association (NACHA). ACH files are intended to represent electronic inter-bank transactions.

## Standard ACH Files

A Check Run will automatically generate this on demand, but only if the run includes payments using an "Electronic" Mode of Payment. See the [configuration page](./configuration.md) for details on how to set the `Mode of Payment` `type` field to mark it as an electronic bank transfer.

The system defaults to using the "ach" file extension, but you can change this as needed in [Check Run Settings](./settings.md). The settings page also includes options to set two other mandatory fields in an ACH file:

1. **ACH Service Class Code** indicates the types of transactions in the batch. Code 200 is for both debit and credit transactions, code 220 is for only credit transactions, and code 225 is for only debit transactions
2. **ACH Standard Class Code** indicates how the transaction was authorized. Currently, the Check Run application only supports Prearranged Payment and Deposit Entries (code PPD)

Other fields available to help configure your ACH generation include:
- ACH Description, which goes into the Batch header
- Company Discretionary Data, also in the Batch header
- Immediate Origin, which can override the ABA number that the bank is expecting
- Custom Post Processing Hook, which allows you to provide a custom function to further manipulate the ACH file. For example, Royal Bank of Canada requires a non-standard first line.

The 'Custom Post Processing Hook' is a read-only field and not intended to be set by non-technical users. The RBC example noted above can be set by entering the following into the browser console: `cur_frm.set_value('custom_post_processing_hook','check_run.test_setup.example_post_processing_hook')`. Provide the dotted path to your function with a signature matching that of the example.

![Example ACH file data with properly-formatted header and batch entries.](./assets/ACHFile.png)

## ACH Prenote

Before processing actual payments, banks often require ACH prenote files to validate the recipient bank account information. The ACH Prenote report allows you to generate these validation files with minimal transaction amounts (typically $0.00 to $0.50) to test the payment pathways before actual transfers occur.

### Transaction Codes for Prenotes

ACH prenotes use specific transaction codes to indicate they are test transactions for account verification:

| Account Type | Prenote Credit Code | Regular Credit Code | Prenote Debit Code | Regular Debit Code |
|-------------|---------------------|---------------------|---------------------|---------------------|
| Checking    | 23                  | 22                  | 28                  | 27                  |
| Savings     | 33                  | 32                  | 38                  | 37                  |

For suppliers receiving payments (credits), you would typically use code **23** for checking accounts or **33** for savings accounts during the prenote process.

### Using the ACH Prenote Report

1. Navigate to the ACH Prenote report in the Reports menu
2. The report displays eligible recipients for ACH prenote testing
3. Use the report filters to narrow down recipients by supplier group, payment terms, or other criteria
4. Click the "Generate ACH Prenote" button to create the prenote file

### Generating the Prenote File

When generating an ACH prenote file, you'll be prompted for the following information:

- **Check Run Settings**: Select the appropriate settings profile for your bank
- **ACH Amount**: Enter the test amount, your bank should give you advice on the correct amount
- **Date**: The effective date for the prenote transactions

After submitting this information, the system will generate and download an ACH prenote file that you can submit to your bank.

### Editing Bank Information from the Prenote Report

After submitting the prenote NACHA file to your bank, you may receive feedback requiring corrections. The ACH Prenote report allows you to:

1. Update recipient bank account information directly in the report view
2. Edit effective dates or prenote amounts as needed
3. Re-generate the prenote file with the corrected information
