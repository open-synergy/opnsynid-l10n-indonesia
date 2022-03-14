# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Indonesia - Common Feature for Pusat Logistik Berikat",
    "version": "8.0.2.0.0",
    "category": "localization",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "l10n_id_djbc_app",
        "product_m2mcategories",
    ],
    "data": [
        "menu.xml",
        "views/stock_picking_type_views.xml",
        "views/product_template_views.xml",
        "views/product_category_views.xml",
    ],
}
