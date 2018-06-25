# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Indonesia - IT Inventory for DJBC Reporting",
    "version": "8.0.1.3.2",
    "category": "localization",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "stock",
    ],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "menu.xml",
        "wizards/date_range_selector_views.xml",
        "views/djbc_report_period_views.xml",
        "views/djbc_document_type_views.xml",
        "views/djbc_custom_document_views.xml",
        "views/stock_move_views.xml",
        "views/stock_quant_views.xml",
        "views/product_template_views.xml",
    ],
}
