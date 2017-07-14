# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Indonesia - Retur Pajak Keluaran",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "OpenSynergy Indonesia",
    "website": "https://opensynergy-indonesia.com",
    "category": "Localization",
    "depends": [
        "l10n_id_taxform_faktur_pajak_common",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/faktur_pajak_type_data.xml",
        "views/retur_pajak_keluaran_views.xml",
    ],
    "installable": True,
}
