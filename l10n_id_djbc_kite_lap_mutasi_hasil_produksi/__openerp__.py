# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Indonesia - Lap.  Mutasi Hasil Produksi for KITE",
    "version": "8.0.1.0.0",
    "category": "localization",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "l10n_id_djbc_kite_common",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizards/date_range_selector_views.xml",
        "reports/lap_kite_mutasi_hasil_produksi_views.xml",
    ],
}
