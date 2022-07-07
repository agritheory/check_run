// Copyright (c) 2022, AgriTheory and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Positive Pay"] = {
	"filters": [
		{
			fieldname: "bank_account",
			label: __("Bank Account"),
			fieldtype: "Link",
			options: 'Bank Account',
			reqd: 1,
		},
		{
			fieldname: "start_date",
			label: __("Start Date"),
			fieldtype: "Date",
			default: moment().date(0).startOf('month').format(),
			reqd: 1,
		},
		{
			fieldname: "end_date",
			label: __("End Date"),
			fieldtype: "Date",
			default: moment().date(0).format(),
			reqd: 1,
		},
	]
}
