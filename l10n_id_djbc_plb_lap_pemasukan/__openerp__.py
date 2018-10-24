# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Indonesia - Lap. Pemasukan for DJBC's "
            "Pusat Logistik Berikat",
    "version": "8.0.1.2.1",
    "category": "localization",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "l10n_id_djbc_plb_common"
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizards/date_range_selector_views.xml",
        "reports/lap_plb_lap_pemasukan.xml"
    ],
}
