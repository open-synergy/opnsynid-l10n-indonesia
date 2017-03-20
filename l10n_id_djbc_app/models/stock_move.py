# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api



class StockMove(models.Model):
    _inherit = "stock.move"

    @api.depends(
        "quant_ids",
        "quant_ids.djbc_custom",
        )
    @api.multi
    def _compute_djbc(self):
        for move in self:
            move.djbc_custom = False
            for quant in move.quant_ids:
                move.djbc_custom = True
                if not quant.djbc_custom:
                    move.djbc_custom = False

    djbc_custom_document_id = fields.Many2one(
        string="DJBC Custom Document",
        comodel_name="l10n_id.djbc_custom_document",
        ondelete="restrict",
        )
    djbc_custom = fields.Boolean(
        string="DJBC Marking",
        compute="_compute_djbc",
        store=True,
        readonly=True,
        )
