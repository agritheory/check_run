# Configuring Mode of Payment for Employees and Suppliers

The Check Run application includes six `Mode of Payment` documents: 

- ACH/EFT
- Bank Draft
- Cash
- Check
- Credit Card
- Wire Transfer

[TODO: configuration needed to use any of these?]

## Supplier Configuration

The `Supplier` doctype has three new fields under the "Credit Limit" section for default mode of payment, bank, and bank account. These fields should be filled in for any supplier that will be paid via a check run.

[TODO: screen shots for supplier]

![]()

## Employee Configuration

Similarly, the `Employee` doctype includes new mode of payment, bank, and bank account fields in the "Salary Details" section. These fields should be filled in for any employee that will be paid via a check run.

![Employee doctype detail showing the Salary Details section expanded with new fields for Mode of Payment, Bank, and Bank Account](../assets/ConfigEmployee.png)
