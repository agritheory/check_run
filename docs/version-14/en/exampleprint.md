# Example Print Formats: Voucher Check and Summary of References

## Example Voucher Print Format
To take advantage of Check Run's check printing functionality, you'll need to set up a print format in ERPNext. An Example Voucher check print format is provided with the application to serve as a starting point. Print formats are as unique as the organizations using ERPNext, so the example template should be customized to suit your needs. It's enabled by default and can be found in the Print Format list.

![Screen shot showing the print preview screen of a Check Run that applies the Example Voucher print format. The top half of the format includes the actual check data and the bottom half includes the references associated with the payment.](./assets/print_format_example_voucher.png)

**Note:** If you've set a background image in a Check Run Settings document, it can be accessed in the print format after fetching the document. To remove the background image from the actual print, make sure to set the background image to the preset `check-run-print` class in the print format HTML. This will ensure that the background image is not printed, but is still visible in the print preview. The Example Voucher provides an example of how to do this.

## Example Secondary Print Format
A second print format called Example Secondary Print Format is also provided under Print Formats. It's not meant to be used to print checks, but will display a summary of the references associated with each Check.

![Screen shot showing the print preview of a Check Run that applies the Example Secondary Print Format. It shows a table of references and amounts associated with the payment.](./assets/print_format_secondary.png)

## Considerations

Both example print formats are set to only display transactions where the Mode of Payment is included in the Printable Modes of Payment in Check Run multiselect field found in Check Run Settings.

One consideration to be aware of, if you include references in the print format (like the examples), is that if there are a lot of references associated with a payment, the list may exceed the length of the paper and not print correctly. The value for Number of Invoices per Voucher in Check Run Settings will limit the number of references associated with a payment and can be adjusted as-needed.

Additional resources:

- [ERPNext print format documentation](https://docs.erpnext.com/docs/v14/user/manual/en/customize-erpnext/print-format)
