# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    djbc = fields.Boolean(
        string="DJBC",
    )
