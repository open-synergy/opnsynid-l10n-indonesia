# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    djbc_kb_ok = fields.Boolean(
        string="Category for DJBC KB",
    )
