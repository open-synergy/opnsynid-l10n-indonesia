# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Indonesia - Lap. Pemasukan Bahan Baku for DJBC Reporting",
    "version": "8.0.1.1.0",
    "category": "localization",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "l10n_id_djbc_bc20",
        "stock_transport_multi_address",
        "purchase",
    ],
    "data": [
        "security/ir.model.access.csv",
        "reports/lap_pemasukan_bahan_baku_views.xml",
    ],
}
