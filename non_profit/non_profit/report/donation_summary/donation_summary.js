// Copyright (c) 2026, Quantbit Technologies and contributors
// For license information, please see license.txt
frappe.query_reports["Donation Summary"] = {
	filters: [
		{
			"fieldname": "donor",
			"label": __("Donor"),
			"fieldtype": "Link",
			"options": "Donor",
		}
	]

};