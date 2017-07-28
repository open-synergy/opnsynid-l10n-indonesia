# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Indonesia - Daftar Bukti Potong PPh 23/26 (D.1.1.32.05)",
    "version": "8.0.1.0.0",
    "category": "localization",
    "website": "https://opensynergy-indonesia.com/",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "l10n_id_taxform_daftar_bukti_potong_pph_common",
        "l10n_id_taxform_bukti_potong_pph_23",
        "l10n_id_taxform_bukti_potong_pph_f113308",
    ],
    "data": [
        "data/daftar_bukti_potong_pph_type_datas.xml",
        "security/ir.model.access.csv",
        "views/daftar_bukti_potong_pph_d113205_views.xml",
    ],
}
