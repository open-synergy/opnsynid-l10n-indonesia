# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    @api.depends("categ_ids")
    def _compute_djbc_ok(self):
        for template in self:
            djbc_ok = False
            for categ in template.categ_ids:
                if categ.djbc_kb_ok:
                    djbc_ok = True
            template.djbc_kb_ok = djbc_ok

    djbc_kb_ok = fields.Boolean(
        string="Can be Used for DJBC KB",
        compute="_compute_djbc_ok",
        store=True,
    )
