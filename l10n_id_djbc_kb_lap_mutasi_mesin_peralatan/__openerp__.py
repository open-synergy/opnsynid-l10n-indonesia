# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Indonesia - Lap.  Mutasi Mesin Peralatan "
    "for DJBC's Kawasan Berikat Reporting",
    "version": "8.0.1.1.0",
    "category": "localization",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "l10n_id_djbc_kb_lap_common",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizards/date_range_selector_views.xml",
        "reports/lap_kb_mutasi_mesin_peralatan_views.xml",
    ],
}
