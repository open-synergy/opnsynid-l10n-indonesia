# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Indonesia - Laporan Pemakaian Bahan Baku for KITE",
    "version": "8.0.1.2.0",
    "category": "localization",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "stock",
        "l10n_id_djbc_kite_common",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/djbc_kite_movement_type_data.xml",
        "reports/djbc_kite_lap_pemakaian_bahan_baku.xml",
        "wizards/date_range_selector_views.xml"
    ],
}
