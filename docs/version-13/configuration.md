# Configuring Mode of Payment for Employees and Suppliers

The options that show in the dropdown for `Mode of Payment` in a check run are determined by the `Mode of Payment` documents you have created in your ERPNext site. The Check Run application includes new fields in the `Supplier` and `Employee` doctypes to specify a default `Mode of Payment`. If populated, this option will show automatically in a check run for any payables owed to that party.



[TODO: are these added via demo data or included in Check Run? If included, any additional configuration needed for these to work (like credit card)?]


If you need to add a new `Mode of Payment`, Check Run includes a new field for the `type` of the payment. You can specify this from the following options:

- Cash
- Bank
- General
- Phone
- Electronic

## Supplier Configuration

The `Supplier` doctype has three new fields under the "Credit Limit" section to specify the default mode of payment, bank, and bank account. These fields should be filled in for any supplier that will be paid via a check run.

![Supplier doctype detail showing the Credit Limit section expanded with new fields for Supplier Default Mode of Payment, Bank, and Bank Account](../assets/ConfigSupplier.png)

## Employee Configuration

Similarly, the `Employee` doctype includes new mode of payment, bank, and bank account fields in the "Salary Details" section. These fields should be filled in for any employee that will be paid via a check run.

![Employee doctype detail showing the Salary Details section expanded with new fields for Mode of Payment, Bank, and Bank Account](../assets/ConfigEmployee.png)

## Mode of Payments

The Check Run application adds a new `type` field into this doctype. For any existing or new `Mode of Payment` document, you can specify one of the following options:

- Cash
- Bank
- General
- Phone
- Electronic

Using the `type` field helps
