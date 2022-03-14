# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Indonesia - Faktur Pajak Keluaran",
    "version": "8.0.4.0.0",
    "license": "AGPL-3",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "website": "https://simetri-sinergi.id",
    "category": "Localization",
    "depends": [
        "l10n_id_taxform_faktur_pajak_common",
        "account_invoice_line_price_subtotal_gross",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/faktur_pajak_type_data.xml",
        "wizards/generate_nomor_seri_faktur_pajak_views.xml",
        "views/nomor_seri_faktur_pajak_views.xml",
        "views/faktur_pajak_keluaran_views.xml",
    ],
    "installable": True,
}
