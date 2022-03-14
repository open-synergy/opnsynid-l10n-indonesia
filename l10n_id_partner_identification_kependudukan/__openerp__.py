# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author

{
    "name": "Partner Identification - Identitas Kependudukan",
    "version": "8.0.1.0.0",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "website": "https://simetri-sinergi.id",
    "license": "AGPL-3",
    "depends": [
        "partner_identification",
    ],
    "external_dependencies": {
        "python": [
            "openupgradelib",
        ],
    },
    "data": [
        "data/res_partner_id_category_data.xml",
    ],
    "installable": True,
    "pre_init_hook": "_load_partner_identification_data",
}
