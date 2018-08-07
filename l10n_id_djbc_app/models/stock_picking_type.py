# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    allowed_document_type_ids = fields.Many2many(
        string="Allowed Document Type",
        comodel_name="l10n_id.djbc_document_type",
        relation="djbc_document_type_stock_picking_type_rel",
        column1="stock_picking_type_id",
        column2="document_type_id",
    )
