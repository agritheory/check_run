import time

import frappe
from frappe.utils import get_link_to_form, get_url, getdate


@frappe.whitelist()
def gen_sepa_xml_file(doc):
	doc = frappe.parse_json(doc)
	payments = frappe.parse_json(doc.transactions)
	posting_date = getdate()
	content = genrate_file_for_sepa(payments, doc, posting_date)
	return content


def genrate_file_for_sepa(payments, doc, posting_date):
	# Message Root
	content = make_line("<?xml version='1.0' encoding='UTF-8'?>")
	content += make_line(
		"<Document xmlns='urn:iso:std:iso:20022:tech:xsd:pain.001.001.03' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'>"
	)
	content += make_line("  <CstmrCdtTrfInitn>")

	# Group Header
	content += make_line("      <GrpHdr>")
	content += make_line("          <MsgId>{}</MsgId>".format(time.strftime("%Y%m%d%H%M%S")))
	content += make_line("          <CreDtTm>{}</CreDtTm>".format(time.strftime("%Y-%m-%dT%H:%M:%S")))
	transaction_count = 0
	transaction_count_identifier = "<!-- $COUNT -->"
	content += make_line(f"          <NbOfTxs>{transaction_count_identifier}</NbOfTxs>")
	control_sum = 0.0
	control_sum_identifier = "<!-- $CONTROL_SUM -->"
	content += make_line(f"          <CtrlSum>{control_sum_identifier}</CtrlSum>")
	content += make_line("          <InitgPty>")
	content += make_line(f"              <Nm>{doc.company}</Nm>")
	content += make_line("              <Id>")

	orgid = get_party_orgid(doc.company, doc.bank_account, doc.pay_to_account)

	initiating_party_org_id = orgid.get("initiating_party_org_id", None)
	if not initiating_party_org_id:
		frappe.throw(
			frappe._(
				"Please specify <b>'Initiating Party OrgID'</b> in {}".format(
					f"<a href='{get_check_run_settings_link(doc)}'>Check Run Settings</a>"
				)
			)
		)
	content += make_line("                  <OrgId>")
	content += make_line("                      <Othr>")
	content += make_line(f"                          <Id>{initiating_party_org_id}</Id>")
	content += make_line("                          <SchmeNm>")
	content += make_line("                              <Cd>BANK</Cd>")
	content += make_line("                          </SchmeNm>")
	content += make_line("                      </Othr>")
	content += make_line("                  </OrgId>")
	content += make_line("              </Id>")
	content += make_line("          </InitgPty>")
	content += make_line("      </GrpHdr>")

	# Payment Information Elements
	content += make_line("      <PmtInf>")
	content += make_line(f"          <PmtInfId>{doc.name}</PmtInfId>")
	content += make_line("          <PmtMtd>TRF</PmtMtd>")
	content += make_line("          <BtchBookg>false</BtchBookg>")
	content += make_line(f"          <NbOfTxs>{transaction_count_identifier}</NbOfTxs>")

	content += make_line(f"          <CtrlSum>{control_sum_identifier}</CtrlSum>")
	content += make_line("          <PmtTpInf>")
	content += make_line("              <SvcLvl>")
	content += make_line("                  <Cd>SEPA</Cd>")
	content += make_line("              </SvcLvl>")
	content += make_line("          </PmtTpInf>")
	required_execution_date = posting_date
	content += make_line(f"          <ReqdExctnDt>{required_execution_date}</ReqdExctnDt>")
	content += make_line("          <Dbtr>")
	content += make_line(f"              <Nm>{doc.company}</Nm>")
	# Address
	addr = debtors_address(doc.company, doc.bank_account, doc.pay_to_account)
	if addr:
		content += make_line("              <PstlAdr>")
		content += make_line(
			"              	<PstCd>{}</PstCd>".format(addr.pincode if addr.pincode else "")
		)
		content += make_line(
			"              	<TwnNm>{}</TwnNm>".format(addr.address_line1 if addr.address_line1 else "")
		)
		content += make_line("              	<Ctry>{}</Ctry>".format(addr.city if addr.city else ""))
		content += make_line(
			"              	<AdrLine>{}</AdrLine>".format(addr.address_line2 if addr.address_line2 else "")
		)
		content += make_line("              </PstlAdr>")
	content += make_line("               <Id>")
	content += make_line("                  <OrgId>")
	content += make_line("                      <Othr>")
	debtor_org_id = orgid.get("debtor_org_id", None)
	if not debtor_org_id:
		frappe.throw(
			frappe._(
				"Please specify <b>'Debtor Org Id'</b> in {}".format(
					f"<a href='{get_check_run_settings_link(doc)}'>Check Run Settings</a>"
				)
			)
		)
	content += make_line(f"                          <Id>{debtor_org_id}</Id>")
	content += make_line("                          <SchmeNm>")
	content += make_line("                              <Cd>BANK</Cd>")
	content += make_line("                          </SchmeNm>")
	content += make_line("                      </Othr>")
	content += make_line("                  </OrgId>")
	content += make_line("              </Id>")
	content += make_line("              <CtryOfRes>SE</CtryOfRes>")
	content += make_line("          </Dbtr>")
	content += make_line("          <DbtrAcct>")
	content += make_line("              <Id>")
	iban = get_iban_number(doc.company, doc.bank_account, doc.pay_to_account)
	content += make_line(f"                  <IBAN>{iban}</IBAN>")
	content += make_line("              </Id>")
	content += make_line("              <Ccy>EUR</Ccy>")
	content += make_line("          </DbtrAcct>")
	content += make_line("          <DbtrAgt>")
	content += make_line(
		"          <!-- Note: For IBAN only on Debtor side use Othr/Id: NOTPROVIDED - see below -->"
	)
	content += make_line("              <FinInstnId>")
	bank_bic = frappe.db.get_value("Bank Account", doc.bank_account, "branch_code")  # optional
	if bank_bic:
		content += make_line(f"                  	<BIC>{bank_bic}</BIC>")
	else:
		content += make_line("                  <Othr>")
		content += make_line("                      <Id>NOTPROVIDED</Id>")
		content += make_line("                  </Othr>")
	content += make_line("              </FinInstnId>")
	content += make_line("          </DbtrAgt>")
	content += make_line("          <ChrgBr>SLEV</ChrgBr>")
	for payment in payments:
		payment_record = frappe.get_doc("Payment Entry", payment.get("payment_entry"))
		content += make_line("          <CdtTrfTxInf>")
		content += make_line("              <PmtId>")
		content += make_line(
			"                  <InstrId>{}</InstrId>".format(payment.get("payment_entry"))
		)
		content += make_line(
			"                  <EndToEndId>{}</EndToEndId>".format(
				payment.get("payment_entry").replace("-", "")
			)
		)
		content += make_line("              </PmtId>")
		content += make_line("              <Amt>")
		content += make_line(
			'                  <InstdAmt Ccy="{}">{:.2f}</InstdAmt>'.format(
				payment_record.paid_from_account_currency, payment_record.paid_amount
			)
		)
		content += make_line("              </Amt>")
		content += make_line(
			"              <!-- Note: Creditor Agent should not be used at all for IBAN only on Creditor side -->"
		)
		content += make_line("              <Cdtr>")
		if payment_record.party_type == "Supplier":
			name = frappe.db.get_value("Supplier", payment_record.party, "supplier_name")
			if "&" in name:
				new_name = name.replace("& ", "")
				if new_name == name:
					new_name = name.replace("&", " ")
				name = new_name
		content += make_line(f"                  <Nm>{name}</Nm>")
		content += make_line("              </Cdtr>")
		content += make_line("              <CdtrAcct>")
		content += make_line("                  <Id>")

		iban_code = get_party_iban_code(payment_record.party_type, payment_record.party)

		content += make_line(
			"                      <IBAN>{}</IBAN>".format(iban_code.strip() if iban_code else "")
		)
		content += make_line("                  </Id>")
		content += make_line("              </CdtrAcct>")
		content += make_line("              <RmtInf>")
		sup_invoice_no = [
			frappe.db.get_value("Purchase Invoice", row.reference_name, "bill_no")
			for row in payment_record.references
		]

		content += make_line(
			"                  <Ustrd>{}</Ustrd>".format(
				", ".join(sup_invoice_no) if sup_invoice_no[0] else ""
			)
		)
		content += make_line("              </RmtInf>")
		content += make_line("          </CdtTrfTxInf>")
		transaction_count += 1
		control_sum += payment_record.paid_amount
	content += make_line("      </PmtInf>")

	# Finished tags
	content += make_line("  </CstmrCdtTrfInitn>")
	content += make_line("</Document>")
	content = content.replace(transaction_count_identifier, f"{transaction_count}")
	content = content.replace(control_sum_identifier, f"{control_sum:.2f}")
	return content


def get_company_name(payment_entry):
	return frappe.get_value("Payment Entry", payment_entry, "company")


def make_line(line):
	return line + "\r\n"


def get_iban_number(company, bank_account, pay_to_account):
	bank_iban = frappe.db.get_value("Bank Account", bank_account, "iban")

	if bank_iban:
		return bank_iban
	else:
		frappe.throw(
			frappe._(f"Iban no is missing in bank account {get_link_to_form('Bank Account', bank_account)}")
		)


def get_party_iban_code(party_type, party):
	party_iban = frappe.db.sql(
		f"""
                        Select iban
                        From `tabBank Account`
                        Where party_type = '{party_type}' and party = '{party}'
     """,
		as_dict=1,
	)

	if party_iban:
		return party_iban[0].iban
	else:
		frappe.throw(
			frappe._(f"Iban Code is not available for {party_type} {get_link_to_form(party_type, party)}")
		)


def get_party_orgid(company, bank_account, pay_to_account):
	orgid = frappe.db.sql(
		f"""
				Select initiating_party_org_id, debtor_org_id
				From `tabCheck Run Settings`
				Where company = '{company}' and pay_to_account = '{pay_to_account}' and bank_account = '{bank_account}'
			""",
		as_dict=1,
	)
	return orgid[0]


def debtors_address(company, bank_account, pay_to_account):
	if crs_name := frappe.db.exists(
		"Check Run Settings", {"bank_account": bank_account, "pay_to_account": pay_to_account}
	):
		address = frappe.db.get_value("Check Run Settings", crs_name, "debtors_address")
		if not address:
			return None
		address_doc = frappe.get_doc("Address", address)
		return address_doc


def get_check_run_settings_link(doc):
	url = get_url()
	check_run_settings_path = "/app/check-run-settings/"
	check_run_settings = frappe.db.exists(
		"Check Run Settings", {"bank_account": doc.bank_account, "pay_to_account": doc.pay_to_account}
	)
	check_run_settings_url = url + check_run_settings_path + check_run_settings
	return str(check_run_settings_url)
