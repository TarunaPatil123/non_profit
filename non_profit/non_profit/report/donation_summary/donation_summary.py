# Copyright (c) 2026, Quantbit Technologies and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):

    filters = filters or {}

    fiscal_years = frappe.get_all(
        "Fiscal Year",
        fields=["name"],
        order_by="year_start_date"
    )

    columns = [
        {
            "label": f"<div style='text-align:center'>Donor</div>",
            "fieldname": "donor",
            "fieldtype": "Link",
            "options": "Donor",
            "width": 200
        },
    ]

    for fy in fiscal_years:
        columns.append({
            "label": f"<div style='text-align:center'>{fy.name}</div>",
            "fieldname": fy.name,
            "fieldtype": "Currency",
            "width": 120
        })

    columns.append({
        "label": "<div style='text-align:center'>Total</div>",
        "fieldname": "total",
        "fieldtype": "Currency",
        "width": 120
    })

    conditions = "d.docstatus = 1"

    if filters.get("donor"):
        conditions += " AND d.donor = %(donor)s"

    if filters.get("donor_name"):
        conditions += " AND dn.donor_name LIKE %(donor_name)s"
        filters["donor_name"] = "%" + filters["donor_name"] + "%"

    donations = frappe.db.sql(f"""
        SELECT
            d.donor,
            d.amount,
            d.custom_fiscal_year
        FROM
            `tabDonation` d
        LEFT JOIN
            `tabDonor` dn ON d.donor = dn.name
        WHERE
            {conditions}
    """, filters, as_dict=True)

    data_map = {}

    for d in donations:

        donor = d.donor
        amount = d.amount or 0
        fy_name = d.custom_fiscal_year

        if not fy_name:
            continue

        if donor not in data_map:
            data_map[donor] = {
                "donor": donor,
                "total": 0
            }
        data_map[donor][fy_name] = data_map[donor].get(fy_name, 0) + amount
        data_map[donor]["total"] = data_map[donor].get("total", 0) + amount

    data = list(data_map.values())

    return columns, data