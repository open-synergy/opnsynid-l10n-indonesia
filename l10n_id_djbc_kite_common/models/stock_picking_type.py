# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    djbc_kite_movement_type_id = fields.Many2one(
        string="DJBC's Kite Movement Type",
        comodel_name="l10n_id.djbc_kite_movement_type",
    )
    djbc_kite_scrap = fields.Boolean(
        string="DJBC's KITE Scrap?",
        default=False,
    )
