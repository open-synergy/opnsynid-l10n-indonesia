# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    @api.depends(
        "categ_ids",
        "categ_ids.djbc_plb_ok",
    )
    def _compute_djbc_plb_ok(self):
        for template in self:
            djbc_ok = False
            for categ in template.categ_ids:
                if categ.djbc_plb_ok:
                    djbc_ok = True
            template.djbc_plb_ok = djbc_ok

    djbc_plb_ok = fields.Boolean(
        string="Can be Used for DJBC PLB",
        compute="_compute_djbc_plb_ok",
        store=True,
    )
