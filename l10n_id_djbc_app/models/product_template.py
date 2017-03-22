# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    djbc_rm = fields.Boolean(
        string="DJBC Raw Material"
    )
    djbc_fg = fields.Boolean(
        string="DJBC Finished Good"
    )
    djbc_wip = fields.Boolean(
        string="DJBC WIP"
    )
