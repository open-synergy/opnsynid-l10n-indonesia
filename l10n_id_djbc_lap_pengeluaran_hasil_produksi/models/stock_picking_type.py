# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    djbc_lap_pengeluaran_hasil_produksi = fields.Boolean(
        string="DJBC Lap. Pengeluaran Hasil Produksi",
    )
