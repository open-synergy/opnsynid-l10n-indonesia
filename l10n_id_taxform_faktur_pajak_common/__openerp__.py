# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Indonesia - Faktur Pajak Common Feature",
    "version": "8.0.6.0.1",
    "license": "AGPL-3",
    "author": "OpenSynergy Indonesia",
    "website": "https://opensynergy-indonesia.com",
    "category": "Localization",
    "depends": [
        "partner_street_number",
        "res_partner_affiliate",
        "base_location_lau_level3",
        "l10n_id_taxform_period",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/faktur_pajak_transaction_type_data.xml",
        "data/faktur_pajak_additional_flag_data.xml",
        "menu.xml",
        "views/faktur_pajak_type_views.xml",
        "views/faktur_pajak_transaction_type_views.xml",
        "views/faktur_pajak_additional_flag_views.xml",
        "views/faktur_pajak_common_views.xml",
    ],
    "installable": True,
}
