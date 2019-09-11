# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Indonesia - Laporan Pengeluaran Hasil Produksi for KITE",
    "version": "8.0.1.0.0",
    "category": "localization",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "l10n_id_djbc_kite_common"
    ],
    "data": [
        "data/djbc_kite_movement_type_data.xml",
        "security/ir.model.access.csv",
        "wizards/date_range_selector_views.xml",
        "reports/djbc_kite_lap_pengeluaran_hasil_produksi.xml",
    ],
}
