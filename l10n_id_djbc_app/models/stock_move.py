# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


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

    @api.depends("picking_type_id", "picking_type_id.allowed_document_type_ids")
    def _compute_all_allowed_document_type_ids(self):
        obj_document_type = self.env["l10n_id.djbc_document_type"]
        for move in self:
            if move.picking_type_id and move.picking_type_id.allowed_document_type_ids:
                move.all_allowed_document_type_ids = (
                    move.picking_type_id.allowed_document_type_ids
                )
            else:
                move.all_allowed_document_type_ids = obj_document_type.search([])

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
    all_allowed_document_type_ids = fields.Many2many(
        string="All Allowed Document Type",
        comodel_name="l10n_id.djbc_document_type",
        compute="_compute_all_allowed_document_type_ids",
        store=False,
    )
