# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    djbc_adjustment_in_picking_type_id = fields.Many2one(
        string="DJBC Adjustment In Picking Type",
        comodel_name="stock.picking.type",
    )
    djbc_adjustment_out_picking_type_id = fields.Many2one(
        string="DJBC Adjustment Out Picking Type",
        comodel_name="stock.picking.type",
    )
