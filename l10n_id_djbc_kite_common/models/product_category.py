# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ProductCategory(models.Model):
    _inherit = "product.category"

    djbc_kite_ok = fields.Boolean(
        string="Category for DJBC KITE",
    )
