# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Indonesia - Common Feature for Daftar Bukti Potong PPh",
    "version": "8.0.1.0.0",
    "category": "localization",
    "website": "https://opensynergy-indonesia.com/",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "mail",
        "l10n_id_taxform_bukti_potong_pph_common",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/daftar_bukti_potong_pph_type_views.xml",
        "views/daftar_bukti_potong_pph_views.xml",
    ],
}
