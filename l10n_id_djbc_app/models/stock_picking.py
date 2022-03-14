# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.depends("picking_type_id", "picking_type_id.allowed_document_type_ids")
    def _compute_all_allowed_document_type_ids(self):
        obj_document_type = self.env["l10n_id.djbc_document_type"]
        for picking in self:
            if picking.picking_type_id.allowed_document_type_ids:
                picking.all_allowed_document_type_ids = (
                    picking.picking_type_id.allowed_document_type_ids
                )
            else:
                picking.all_allowed_document_type_ids = obj_document_type.search([])

    all_allowed_document_type_ids = fields.Many2many(
        string="All Allowed Document Type",
        comodel_name="l10n_id.djbc_document_type",
        compute="_compute_all_allowed_document_type_ids",
        store=False,
    )
