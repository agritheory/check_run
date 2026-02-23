<!-- Copyright (c) 2026, AgriTheory and contributors
For license information, please see license.txt-->

# Example Print Format: Voucher Check

<div class="byline">
  AgriTheory and Tyler Matteson 2026-02-21
</div>


To take advantage of Check Run's check printing functionality, you'll need to set up a print format in ERPNext. Print formats are as unique as the organizations using ERPNext, so a voucher check print format serves as an example template. It can be a starting point from which to customize to suit your needs.

The example print format included with this application can be found in the Print Format List under Example Voucher. It is disabled by default.


## Using MICR Encoding Font

The Check Run app also includes an example print format for a check template that applies the [MICR Encoding font](https://www.1001fonts.com/micr-encoding-font.html) to the routing number, account number, and check number part of the layout. The format is called Example Voucher MICR and is disabled by default.

In order for the preview of any print format that's using the MICR Encoding font to render the font correctly, the font must be installed on the machine serving your site. This will be the server for a production environment or your local machine for a development environment. Below are the steps to make the MICR Encoding font available for Check Run print formats and during the conversion to print to a PDF:

- Download and install the [MICR Encoding font](https://www.1001fonts.com/micr-encoding-font.html) onto either your server (production environment) or your local machine (development environment). Refer to your Operating System's guide for how to install fonts, as the instructions vary depending on the OS
- Installing the font isn't enough to make it available during the PDF conversion process in the current software that Frappe uses to convert print format HTML into a PDF. For the font to render in the PDF, the [Base64](https://en.wikipedia.org/wiki/Base64) value of the font's `.ttf` (Truetype format) file needs to be embedded in the print format's Custom CSS as a `@font-face` declaration. There are a number of online or command line tools that can do the conversion from the `.ttf` file to a Base64 string. You then need to pasted the resulting Base64 string into the `url` attribute of the `@font-face` declaration, as indicated in the following example:

```css
/* At the top of the print format's Custom CSS section */
@font-face {
    font-family: 'MICR Encoding';
    font-style: normal;
    src: url(data:font/truetype;charset=utf-8;base64,<<copied Base64 string>>) format('truetype');
}
```
The Example Voucher MICR print format includes a Base64 string that was generated using the MacOS/Linux built-in `base64` command line tool. An important caveat is that Base64 fonts may not render exactly the same as the installed version.

- Finally, apply the font in the print format by setting the `font-family` attribute to `'MICR Encoding` on the element(s) containing the text that should render in the MICR Encoding font. This may be done either inline in the HTML via the `style` attribute, or in the custom CSS on the relevant selector. The Example Voucher MICR print format uses hard-coded, fictitious values for the routing number and account number.

```html
<!-- Option 1: In the print format's HTML (assumes a Jinga print format type)-->
<span id="micr_encoding_block" style="font-family: 'MICR Encoding';">
    a{{ routing_number }}a {{ account_number }}b{{ doc.reference_no }}
</span>
```

```css
/* Option 2: In the print format's Custom CSS section */
#micr_encoding_block {
    font-family: 'MICR Encoding';
    /* other attributes */
}
```

Additional resources:

- [ERPNext print format documentation](https://docs.erpnext.com/docs/v14/user/manual/en/customize-erpnext/print-format)
