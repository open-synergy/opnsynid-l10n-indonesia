# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Indonesia - Lap. Penyelesaian Scrap/Waste for DJBC Reporting",
    "version": "8.0.2.0.0",
    "category": "localization",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "stock",
        "l10n_id_djbc_app",
    ],
    "data": [
        "security/ir.model.access.csv",
        "reports/lap_penyelesaian_scrap_views.xml",
        "views/stock_picking_type_views.xml",
    ],
}
