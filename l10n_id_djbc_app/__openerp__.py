# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Indonesia - IT Inventory for DJBC Reporting",
    "version": "8.0.1.6.1",
    "category": "localization",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "stock_account",
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
        "views/stock_picking_views.xml",
        "views/stock_picking_type_views.xml",
        "views/stock_production_lot_views.xml",
    ],
}
