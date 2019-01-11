# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ProductCategory(models.Model):
    _inherit = "product.category"

    djbc_plb_ok = fields.Boolean(
        string="Category for DJBC PLB",
    )
