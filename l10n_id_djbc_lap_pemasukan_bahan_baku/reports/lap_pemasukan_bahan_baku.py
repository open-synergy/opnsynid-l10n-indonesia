# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp import tools


class LapPemasukanBahanBaku(models.Model):
    _name = "l10n_id.djbc_lap_pemasukan_bahan_baku"
    _description = "DJBC Lap. Pemasukan Bahan Baku"
    _auto = False

    @api.multi
    def _compute_value(self):
        for move in self:
            move.inventory_value = 0.0
            if move.po_line_id:
                move.inventory_value = (
                    move.po_line_id.price_subtotal /
                    move.po_line_id.product_qty) * \
                    move.quantity

    document_type_id = fields.Many2one(
        string="Document Type",
        comodel_name="l10n_id.djbc_document_type",
        readonly=True,
    )
    custom_document_id = fields.Many2one(
        string="Custom Document",
        comodel_name="l10n_id.djbc_custom_document",
        readonly=True,
    )
    custom_document_date = fields.Date(
        string="Custom Document Date",
        readonly=True,
    )
    lot_id = fields.Many2one(
        string="Lot",
        comodel_name="stock.production.lot",
        readonly=True,
    )
    picking_id = fields.Many2one(
        string="Picking",
        comodel_name="stock.picking",
        readonly=True,
    )
    move_date = fields.Datetime(
        string="Move Date",
        readonly=True,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        readonly=True,
    )
    product_name = fields.Char(
        string="Product Name",
        readonly=True,
    )
    product_code = fields.Char(
        string="Product Code",
        readonly=True,
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
        readonly=True,
    )
    quantity = fields.Float(
        string="Qty.",
        readonly=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        readonly=True,
    )
    inventory_value = fields.Float(
        string="Inventory Value",
        readonly=True,
        compute="_compute_value",
    )
    warehouse_id = fields.Many2one(
        string="Warehouse",
        comodel_name="stock.warehouse",
        readonly=True,
    )
    subcontract_id = fields.Many2one(
        string="Subcontract",
        comodel_name="res.partner",
        readonly=True,
    )
    country_origin_id = fields.Many2one(
        string="Country Origin",
        comodel_name="res.country",
        readonly=True,
    )
    po_line_id = fields.Many2one(
        string="PO Line",
        comodel_name="purchase.order.line",
        readonly=True,
    )

    def _select(self):
        select_str = """
             SELECT a.id as id,
                    b.type_id AS document_type_id,
                    a.djbc_custom_document_id AS custom_document_id,
                    b.date AS custom_document_date,
                    a.restrict_lot_id as lot_id,
                    a.picking_id AS picking_id,
                    a.date AS move_date,
                    a.product_id AS product_id,
                    d.name AS product_name,
                    c.default_code AS product_code,
                    a.product_uom AS uom_id,
                    a.product_uom_qty AS quantity,
                    j.currency_id AS currency_id,
                    0.0 AS inventory_value,
                    e.warehouse_id AS warehouse_id,
                    NULL AS subcontract_id,
                    g.country_id AS country_origin_id,
                    a.purchase_line_id AS po_line_id
        """
        return select_str

    def _from(self):
        from_str = """
                stock_move AS a
                JOIN l10n_id_djbc_custom_document AS b ON
                    a.djbc_custom_document_id = b.id
                JOIN product_product AS c ON a.product_id = c.id
                JOIN product_template AS d ON c.product_tmpl_id = d.id
                JOIN stock_picking_type AS e ON a.picking_type_id = e.id
                JOIN stock_picking AS f ON a.picking_id = f.id
                LEFT JOIN res_partner AS g ON f.origin_address_id = g.id
                JOIN stock_location AS h ON a.location_id = h.id
                JOIN purchase_order_line AS i ON a.purchase_line_id = i.id
                JOIN purchase_order AS j ON i.order_id = j.id
        """
        return from_str

    def _where(self):
        where_str = """
                a.state = 'done' AND
                h.usage = 'supplier' AND
                d.djbc_rm = TRUE
        """
        return where_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM ( %s )
            WHERE
            %s
            )""" % (self._table, self._select(), self._from(), self._where()))
