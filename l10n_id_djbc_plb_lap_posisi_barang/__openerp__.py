# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Indonesia - Lap. Posisi Barang for DJBC's "
            "Pusat Logistik Berikat",
    "version": "8.0.1.0.0",
    "category": "localization",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "l10n_id_djbc_plb_common",
        "l10n_id_djbc_lap_posisi_barang_common",
    ],
    "data": [
        "wizards/cetak_lap_posisi_barang_plb.xml",
    ],
}
