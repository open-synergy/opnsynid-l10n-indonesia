# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp import tools


class LapPengeluaranHasilProduksi(models.Model):
    _name = "l10n_id.djbc_lap_pengeluaran_hasil_produksi"
    _description = "DJBC Lap. Pengeluaran Hasil Produksi"
    _auto = False

    @api.multi
    def _compute_value(self):
        for move in self:
            move.inventory_value = 0.0
            if move.so_line_id:
                move.inventory_value = (
                    move.so_line_id.price_subtotal /
                    move.so_line_id.product_uom_qty) * \
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
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        readonly=True,
    )
    country_id = fields.Many2one(
        string="Destination Country",
        comodel_name="res.country",
        readonly=True,
    )
    so_line_id = fields.Many2one(
        string="SO Line",
        comodel_name="sale.order.line",
        readonly=True,
    )

    def _select(self):
        select_str = """
             SELECT a.id as id,
                    b.type_id AS document_type_id,
                    a.djbc_custom_document_id AS custom_document_id,
                    b.date AS custom_document_date,
                    a.picking_id AS picking_id,
                    a.date AS move_date,
                    a.product_id AS product_id,
                    d.name AS product_name,
                    c.default_code AS product_code,
                    a.product_uom AS uom_id,
                    a.product_uom_qty AS quantity,
                    l.currency_id AS currency_id,
                    f.partner_id AS partner_id,
                    g.country_id AS country_id,
                    i.sale_line_id AS so_line_id
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
                LEFT JOIN res_partner AS g ON f.delivery_address_id = g.id
                JOIN stock_location AS h ON a.location_id = h.id
                JOIN procurement_order AS i ON a.procurement_id = i.id
                JOIN sale_order_line AS j ON i.sale_line_id = j.id
                JOIN sale_order AS k ON j.order_id = k.id
                JOIN product_pricelist AS l ON k.pricelist_id = l.id
        """
        return from_str

    def _where(self):
        where_str = """
                a.state = 'done' AND
                e.djbc_lap_pengeluaran_hasil_produksi = TRUE
        """
        return where_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM ( %s )
            WHERE
            %s
            )""" % (self._table, self._select(), self._from(), self._where()))
