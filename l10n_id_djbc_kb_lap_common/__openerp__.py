# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Indonesia - Common Feature for Kawasan Berikat Reporting",
    "version": "8.0.1.3.0",
    "category": "localization",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "l10n_id_djbc_app",
        "product_m2mcategories",
    ],
    "data": [
        "data/product_category_data.xml",
        "menu.xml",
        "reports/lap_kb_mutasi_common_views.xml",
        "views/stock_picking_type_views.xml",
        "views/stock_inventory_views.xml",
    ],
}
