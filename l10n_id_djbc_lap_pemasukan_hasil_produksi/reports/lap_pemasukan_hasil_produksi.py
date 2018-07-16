# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
from openerp import tools


class LapPemasukanHasilProduksi(models.Model):
    _name = "l10n_id.djbc_lap_pemasukan_hasil_produksi"
    _description = "DJBC Lap. Pemasukan Hasil Produksi"
    _auto = False

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
    quantity_used = fields.Float(
        string="Qty. Used",
        readonly=True,
    )
    quantity_subcontracted = fields.Float(
        string="Qty. Subcontracted",
        readonly=True,
    )
    subcontract_id = fields.Many2one(
        string="Subcontract",
        comodel_name="res.partner",
        readonly=True,
    )

    def _select(self):
        select_str = """
             SELECT a.id as id,
                    a.picking_id AS picking_id,
                    a.date AS move_date,
                    a.product_id AS product_id,
                    c.name AS product_name,
                    b.default_code AS product_code,
                    a.product_uom AS uom_id,
                    CASE
                    WHEN e.partner_id IS NULL
                    THEN a.product_uom_qty
                    ELSE 0.0
                    END AS quantity_used,
                    CASE
                    WHEN e.partner_id IS NOT NULL
                    THEN a.product_uom_qty
                    ELSE 0.0
                    END AS quantity_subcontracted,
                    e.partner_id AS subcontract_id
        """
        return select_str

    def _from(self):
        from_str = """
                stock_move AS a
                JOIN product_product AS b ON a.product_id = b.id
                JOIN product_template AS c ON b.product_tmpl_id = c.id
                JOIN stock_picking_type AS d ON a.picking_type_id = d.id
                LEFT JOIN stock_picking AS e ON a.picking_id = e.id
        """
        return from_str

    def _where(self):
        where_str = """
                a.state = 'done' AND
                a.djbc_custom = TRUE AND
                d.djbc_lap_pemasukan_hasil_produksi = TRUE
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
