suppliers = [
	(
		"Exceptional Grid",
		"Electricity",
		"ACH/EFT",
		150.00,
		"Net 14",
		{
			"address_line1": "2 Cosmo Point",
			"city": "Summerville",
			"state": "MA",
			"country": "United States",
			"pincode": "34791",
		},
	),
	(
		"Liu & Loewen Accountants LLP",
		"Accounting Services",
		None,
		500.00,
		"Net 30",
		{
			"address_line1": "138 Wanda Square",
			"city": "Chino",
			"state": "ME",
			"country": "United States",
			"pincode": "90953",
		},
	),
	(
		"Mare Digitalis",
		"Cloud Services",
		"Credit Card",
		200.00,
		"Due on Receipt",
		{
			"address_line1": "1000 Toll Plaza Tunnel Alley",
			"city": "Joplin",
			"state": "CT",
			"country": "United States",
			"pincode": "51485",
		},
	),
	(
		"AgriTheory",
		"ERPNext Consulting",
		None,
		1000.00,
		"Net 14",
		{
			"address_line1": "1293 Bannan Road",
			"city": "New Brighton",
			"state": "NH",
			"country": "United States",
			"pincode": "55932",
		},
	),
	(
		"HIJ Telecom, Inc",
		"Internet Services",
		"Check",
		150.00,
		"Net 30",
		{
			"address_line1": "955 Winding Highway",
			"city": "Glassboro",
			"state": "NY",
			"country": "United States",
			"pincode": "28026",
		},
	),
	(
		"Sphere Cellular",
		"Phone Services",
		"ACH/EFT",
		250.00,
		"Net 30",
		{
			"address_line1": "1198 Carpenter Road",
			"city": "Rolla",
			"state": "VT",
			"country": "United States",
			"pincode": "94286",
		},
	),
	(
		"Cooperative Ag Finance",
		"Financial Services",
		"Bank Draft",
		5000.00,
		"Net 30",
		{
			"address_line1": "629 Loyola Landing",
			"city": "Warner Robins",
			"state": "CT",
			"country": "United States",
			"pincode": "28989",
		},
	),
	(
		"Tireless Equipment Rental, Inc",
		"Equipment Rental",
		"Check",
		30000.00,
		"18 Month Rental Agreement",
		{
			"address_line1": "385 Crespi Road",
			"city": "Garfield",
			"state": "VT",
			"country": "United States",
			"pincode": "28327",
		},
	),
]

tax_authority = [
	(
		"Massachusetts Department of Revenue",
		"Payroll Taxes",
		"Check",
		0.00,
		"Net 30",
		{
			"address_line1": "18 Spooner Stravenue",
			"city": "Danbury",
			"state": "RI",
			"country": "United States",
			"pincode": "07165",
		},
	),
	(
		"Rhode Island Division of Taxation",
		"Payroll Taxes",
		"Check",
		0.00,
		"Net 30",
		{
			"address_line1": "18 Spooner Stravenue",
			"city": "Danbury",
			"state": "RI",
			"country": "United States",
			"pincode": "07165",
		},
	),
	(
		"Vermont Department of Taxes",
		"Payroll Taxes",
		"Check",
		0.00,
		"Net 30",
		{
			"address_line1": "18 Spooner Stravenue",
			"city": "Danbury",
			"state": "RI",
			"country": "United States",
			"pincode": "07165",
		},
	),
]

sales_tax_templates = [
	{
		"name": "MA Sales Tax - CFC",
		"doctype": "Sales Taxes and Charges Template",
		"title": "MA Sales Tax",
		"is_default": 1,
		"company": "Chelsea Fruit Co",
		"taxes": [
			{
				"charge_type": "On Net Total",
				"account_head": "2320 - Sales Tax Payable - CFC",
				"description": "Sales Tax 6% ",
				"cost_center": "Main - CFC",
				"rate": 6.25,
				"party_type": "Supplier",
				"party": "Massachusetts Department of Revenue",
			}
		],
	},
	{
		"name": "VT Sales Tax - CFC",
		"doctype": "Sales Taxes and Charges Template",
		"title": "VT Sales Tax",
		"is_default": 0,
		"company": "Chelsea Fruit Co",
		"taxes": [
			{
				"charge_type": "On Net Total",
				"account_head": "2320 - Sales Tax Payable - CFC",
				"description": "Sales Tax 6.25% ",
				"cost_center": "Main - CFC",
				"rate": 6,
				"party_type": "Supplier",
				"party": "Vermont Department of Taxes",
			}
		],
	},
	{
		"name": "RI Sales Tax - CFC",
		"doctype": "Sales Taxes and Charges Template",
		"title": "RI Sales Tax",
		"is_default": 0,
		"company": "Chelsea Fruit Co",
		"taxes": [
			{
				"charge_type": "On Net Total",
				"account_head": "2320 - Sales Tax Payable - CFC",
				"description": "Sales Tax 7% ",
				"cost_center": "Main - CFC",
				"rate": 7,
				"party_type": "Supplier",
				"party": "Rhode Island Division of Taxation",
			}
		],
	},
]


employees = [
	("Wilmer Larson", "Male", "1977-03-06", "2019-04-12", "20 Gaven Path", "Spokane", "NV", "66308"),
	(
		"Shanel Finley",
		"Female",
		"1984-04-23",
		"2019-07-04",
		"1070 Ulloa Green",
		"DeKalb",
		"PA",
		"30474",
	),
	(
		"Camellia Phelps",
		"Female",
		"1980-07-06",
		"2019-07-28",
		"787 Sotelo Arcade",
		"Stockton",
		"CO",
		"14860",
	),
	(
		"Michale Mitchell",
		"Male",
		"1984-06-29",
		"2020-01-12",
		"773 Icehouse Road",
		"West Sacramento",
		"VT",
		"24355",
	),
	(
		"Sharilyn Romero",
		"Female",
		"1998-04-22",
		"2020-03-20",
		"432 Dudley Ranch",
		"Clovis",
		"WA",
		"97159",
	),
	(
		"Doug Buckley",
		"Male",
		"1979-06-18",
		"2020-09-08",
		"771 Battery Caulfield Motorway",
		"Yonkers",
		"VT",
		"38125",
	),
	(
		"Margarito Wallace",
		"Male",
		"1991-08-17",
		"2020-11-01",
		"639 Brook Park",
		"Terre Haute",
		"OR",
		"41704",
	),
	(
		"Mckenzie Ashley",
		"Female",
		"1997-09-13",
		"2021-02-22",
		"1119 Hunter Glen",
		"Ormond Beach",
		"MD",
		"30864",
	),
	(
		"Merrie Oliver",
		"Other",
		"1979-11-08",
		"2021-03-11",
		"267 Vega Freeway",
		"West Palm Beach",
		"FL",
		"24411",
	),
	(
		"Naoma Blake",
		"Female",
		"1987-07-10",
		"2021-06-21",
		"649 Conrad Road",
		"Thousand Oaks",
		"CT",
		"97929",
	),
	(
		"Donnell Fry",
		"Male",
		"1994-07-27",
		"2021-06-24",
		"504 Starr King Canyon",
		"Norwalk",
		"OR",
		"46845",
	),
	(
		"Shalanda Peterson",
		"Female",
		"1999-10-04",
		"2021-08-01",
		"109 Seventh Parkway",
		"Urbana",
		"DE",
		"55975",
	),
]

customers = [
	(
		"Almacs Food Group",
		{
			"address_line1": "1103 Storey Road",
			"city": "Edina",
			"state": "AZ",
			"country": "United States",
			"pincode": "24632",
		},
	),
	(
		"Beans and Dreams Roasters",
		{
			"address_line1": "743 Dorcas Road",
			"city": "Salina",
			"state": "CT",
			"country": "United States",
			"pincode": "25901",
		},
	),
	(
		"Cafe 27 Cafeteria",
		{
			"address_line1": "1340 Cook Street",
			"city": "Salina",
			"state": "OK",
			"country": "United States",
			"pincode": "93312",
		},
	),
	(
		"Capital Grille Restaurant Group",
		{
			"address_line1": "4 South Gate",
			"city": "Salina",
			"state": "MA",
			"country": "United States",
			"pincode": "08385",
		},
	),
	(
		"Downtown Deli",
		{
			"address_line1": "1302 Sibley Road",
			"city": "Salina",
			"state": "MT",
			"country": "United States",
			"pincode": "24654",
		},
	),
]
