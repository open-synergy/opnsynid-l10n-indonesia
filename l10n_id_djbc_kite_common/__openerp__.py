# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Indonesia - Common Feature for KITE",
    "version": "8.0.1.1.0",
    "category": "localization",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "l10n_id_djbc_app",
        "product_m2mcategories",
        "stock_adjustment_operation",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/product_category_data.xml",
        "menu.xml",
        "reports/lap_kite_mutasi_common_views.xml",
        "views/djbc_kite_movement_type_views.xml",
        "views/stock_picking_type_views.xml",
        "views/product_category_views.xml",
        "views/product_template_views.xml",
    ],
}
