# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Indonesia - Bukti Potong PPh Pasal 26 (F.1.1.33.08)",
    "version": "8.0.1.1.0",
    "category": "localization",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "l10n_id_taxform_bukti_potong_pph_common",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/l10n_id_bukti_potong_type.xml",
        "views/bukti_potong_pph_f113308_in_views.xml",
        "views/bukti_potong_pph_f113308_out_views.xml",
    ],
}
