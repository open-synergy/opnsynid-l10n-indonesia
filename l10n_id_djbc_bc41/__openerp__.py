# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Indonesia - Form BC 4.1 for DJBC Reporting",
    "version": "8.0.1.0.0",
    "category": "localization",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "l10n_id_djbc_app",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/djbc_document_type.xml",
        "views/djbc_bc41_views.xml",
    ],
}
