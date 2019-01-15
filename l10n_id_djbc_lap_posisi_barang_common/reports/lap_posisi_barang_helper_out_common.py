# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
from openerp import tools


class LapPosisiBarangHelperOutCommon(models.AbstractModel):
    _name = "l10n_id.djbc_lap_posisi_barang_helper_out_common"
    _auto = False

    document_type_id = fields.Many2one(
        string="Jenis",
        comodel_name="l10n_id.djbc_document_type",
    )
    document_id = fields.Many2one(
        string="# Document",
        comodel_name="l10n_id.djbc_custom_document",
    )
    document_date = fields.Date(
        string="Document Date",
    )
    picking_date = fields.Datetime(
        string="Picking Date",
    )
    product_code = fields.Char(
        string="Product Code",
    )
    lot_id = fields.Many2one(
        string="Lot",
        comodel_name="stock.production.lot",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
    )
    quantity = fields.Float(
        string="Quantity",
    )
    cost = fields.Float(
        string="Cost",
    )

    def _select(self):
        select_str = """
             SELECT row_number() OVER() as id,
                    a.move_id AS move_id,
                    c.type_id AS document_type_id,
                    c.id AS document_id,
                    c.date AS document_date,
                    d.date_done AS picking_date,
                    e.default_code AS product_code,
                    a.lot_id AS lot_id,
                    a.product_id AS product_id,
                    a.product_uom_id AS uom_id,
                    a.product_qty AS quantity,
                    a.cost AS cost

        """
        return select_str

    def _from(self):
        from_str = """
                stock_stock_move_lot_out AS a
        """
        return from_str

    def _where(self):
        where_str = """
        """
        return where_str

    def _join(self):
        join_str = """
        JOIN stock_move AS b
            ON a.move_id = b.id
        JOIN l10n_id_djbc_custom_document AS c
            ON b.djbc_custom_document_id = c.id
        JOIN stock_picking AS d
            ON a.picking_id = d.id
        JOIN product_product AS e
            ON a.product_id = e.id
        JOIN product_template AS f
            ON e.product_tmpl_id = f.id

        """
        return join_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            %s
        )""" % (
            self._table,
            self._select(),
            self._from(),
            self._join(),
            self._where()
        ))
