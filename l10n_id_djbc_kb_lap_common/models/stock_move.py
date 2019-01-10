# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, _, api
from openerp.exceptions import Warning as UserError


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.constrains("state", "djbc_custom_document_id", "picking_type_id")
    def _check_djbc_document(self):
        for move in self:
            if move.state == "done" and \
                    move.picking_type_id.djbc_kb_required_doc and \
                    not move.djbc_custom_document_id:
                raise UserError(_("Need DJBC KB Doc"))
