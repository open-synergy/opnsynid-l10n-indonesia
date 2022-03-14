# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    djbc_lap_penyelesaian_scrap = fields.Boolean(
        string="DJBC Lap. Penyelesaian Scrap/Waste",
    )
