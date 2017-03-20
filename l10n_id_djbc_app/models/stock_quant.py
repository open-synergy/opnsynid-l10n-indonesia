# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api



class StockQuant(models.Model):
    _inherit = "stock.quant"

    djbc_custom = fields.Boolean(
        string="DJBC Marking",
        )

    @api.model
    def _quant_create(self, qty, move, lot_id=False, owner_id=False,
                      src_package_id=False, dest_package_id=False,
                      force_location_from=False, force_location_to=False,
                      ):
        quant = super(StockQuant, self)._quant_create(
                qty, move, lot_id, owner_id, src_package_id, dest_package_id,
                force_location_from, force_location_to)
        if move.djbc_custom_document_id:
            quant.write({"djbc_custom": True})
