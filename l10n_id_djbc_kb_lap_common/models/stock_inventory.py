# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    djbc = fields.Boolean(
        string="DJBC",
    )


class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    @api.model
    def _resolve_inventory_line(self, inventory_line):
        _super = super(StockInventoryLine, self)
        obj_location = self.env["stock.location"]
        obj_wh = self.env["stock.warehouse"]
        company = inventory_line.inventory_id.company_id
        location = inventory_line.inventory_id.location_id
        wh = False
        wh_id = obj_location.get_warehouse(location)
        if wh_id:
            wh = obj_wh.browse([wh_id])[0]

        adj_in_type = (
            wh
            and wh.adjustment_in_type_id
            or company.djbc_adjustment_in_picking_type_id
        )
        if not adj_in_type:
            raise UserError(_("No DJBC adjustment in picking type configured"))

        adj_out_type = (
            wh
            and wh.adjustment_out_type_id
            or company.djbc_adjustment_in_picking_type_id
        )
        if not adj_out_type:
            raise UserError(_("No DJBC adjustment out picking type configured"))

        move_id = _super._resolve_inventory_line(inventory_line)
        if not move_id:
            return
        obj_move = self.env["stock.move"]
        move = obj_move.browse([move_id])[0]
        if move.location_id.id == move.product_id.property_stock_inventory.id:
            move.write({"picking_type_id": adj_in_type.id})
        else:
            move.write({"picking_type_id": adj_out_type.id})
        return move_id
