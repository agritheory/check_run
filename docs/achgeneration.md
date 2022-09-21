# ACH Generation

For electronic bank transfers, banking institutions require specifically-formatted plain-text files to encode all necessary information. This includes data about the type of payment, the parties, their bank accounts, and payment amounts. These files conform to Automated Clearing House (ACH) standards, which is an electronic-funds transfer system run by the National Automated Clearing House Association (NACHA). ACH files are intended to represent electronic inter-bank transactions.

After submission, a Check Run will automatically generate this file, but only if the run includes payments using an "Electronic" Mode of Payment. See the [configuration page](./configuration.md) for details on how to set the `Mode of Payment` `type` field to mark it as an electronic bank transfer.

The system defaults to using the "ach" file extension, but you can change this as needed in [Check Run Settings](./settings.md). The settings page also includes options to set two other mandatory fields in an ACH file:

1. **ACH Service Class Code** indicates the types of transactions in the batch. Code 200 is for both debit and credit transactions, code 220 is for only credit transactions, and code 225 is for only debit transactions
2. **ACH Standard Class Code** indicates how the transaction was authorized. Currently, the Check Run application only supports Prearranged Payment and Deposit Entries (code PPD)

![Example ACH file data with properly-formatted header and batch entries.](./assets/ACHFile.png)