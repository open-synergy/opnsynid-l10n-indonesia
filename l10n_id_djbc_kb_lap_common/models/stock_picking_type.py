# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    djbc_kb_movement_type = fields.Selection(
        string="DJBC's KB Movement Type",
        selection=[
            ("in", "In"),
            ("out", "Out"),
            ],
        )
    djbc_kb_scrap = fields.Boolean(
        string="DJBC's KB Scrap?",
        default=False,
        )
    djbc_kb_adjustment = fields.Boolean(
        string="DJBC's KB Adjustment?",
        default=False,
        )

