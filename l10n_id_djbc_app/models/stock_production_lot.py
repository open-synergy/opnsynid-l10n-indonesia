# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class StockQuant(models.Model):
    _inherit = "stock.production.lot"

    djbc_sequence = fields.Integer(
        string="DJBC Sequnce",
    )
