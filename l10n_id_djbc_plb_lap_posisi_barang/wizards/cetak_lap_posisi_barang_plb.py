# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models


class CetakLapPosisiBarangPlb(models.TransientModel):
    _name = "l10n_id.cetak_lap_posisi_barang_plb"
    _inherit = ["l10n_id.cetak_lap_posisi_barang_common"]
