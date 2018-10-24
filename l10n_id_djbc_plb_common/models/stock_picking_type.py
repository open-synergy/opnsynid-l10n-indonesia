# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    djbc_plb_movement_type = fields.Selection(
        string="DJBC's PLB Movement Type",
        selection=[
            ("in", "In"),
            ("out", "Out"),
        ],
    )
    djbc_plb_scrap = fields.Boolean(
        string="DJBC's PLB Scrap?",
        default=False,
    )
    djbc_plb_adjustment = fields.Boolean(
        string="DJBC's PLB Adjustment?",
        default=False,
    )
