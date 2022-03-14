# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    @api.depends("categ_ids")
    def _compute_djbc_kite_ok(self):
        for template in self:
            djbc_ok = False
            for categ in template.categ_ids:
                if categ.djbc_kite_ok:
                    djbc_ok = True
            template.djbc_kite_ok = djbc_ok

    djbc_kite_ok = fields.Boolean(
        string="Can be Used for DJBC KITE",
        compute="_compute_djbc_kite_ok",
        store=True,
    )
