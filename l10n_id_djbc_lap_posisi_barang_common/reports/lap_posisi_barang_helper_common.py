# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models, tools


class LapPosisiBarangHelperCommon(models.AbstractModel):
    _name = "l10n_id.djbc_lap_posisi_barang_helper_common"
    _auto = False

    in_document_type_id = fields.Many2one(
        string="Jenis",
        comodel_name="l10n_id.djbc_document_type",
    )
    in_document_id = fields.Many2one(
        string="# Document",
        comodel_name="l10n_id.djbc_custom_document",
    )
    in_document_date = fields.Date(
        string="Document Date",
    )
    in_picking_date = fields.Datetime(
        string="Picking Date",
    )
    in_product_code = fields.Char(
        string="Product Code",
    )
    in_lot_id = fields.Many2one(
        string="Lot",
        comodel_name="stock.production.lot",
    )
    in_product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    in_uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
    )
    in_quantity = fields.Float(
        string="Quantity",
    )
    in_cost = fields.Float(
        string="Cost",
    )

    out_document_type_id = fields.Many2one(
        string="Jenis",
        comodel_name="l10n_id.djbc_document_type",
    )
    out_document_id = fields.Many2one(
        string="# Document",
        comodel_name="l10n_id.djbc_custom_document",
    )
    out_document_date = fields.Date(
        string="Document Date",
    )
    out_picking_date = fields.Datetime(
        string="Picking Date",
    )
    out_product_code = fields.Char(
        string="Product Code",
    )
    out_lot_id = fields.Many2one(
        string="Lot",
        comodel_name="stock.production.lot",
    )
    out_product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    out_uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
    )
    out_quantity = fields.Float(
        string="Quantity",
    )
    out_cost = fields.Float(
        string="Cost",
    )
    total_quantity = fields.Float(
        string="Total Quantity",
    )
    total_cost = fields.Float(
        string="Total Cost",
    )

    def _select(self):
        select_str = """
             SELECT row_number() OVER() as id,
                    a.document_type_id AS in_document_type_id,
                    a.document_id AS in_document_id,
                    a.document_date AS in_document_date,
                    a.picking_date AS in_picking_date,
                    a.product_code AS in_product_code,
                    a.lot_id AS in_lot_id,
                    a.product_id AS in_product_id,
                    a.uom_id AS in_uom_id,
                    a.quantity AS in_quantity,
                    a.cost AS in_cost,
                    b.document_type_id AS out_document_type_id,
                    b.document_id AS out_document_id,
                    b.document_date AS out_document_date,
                    b.picking_date AS out_picking_date,
                    b.product_code AS out_product_code,
                    b.lot_id AS out_lot_id,
                    b.product_id AS out_product_id,
                    b.uom_id AS out_uom_id,
                    b.quantity AS out_quantity,
                    b.cost AS out_cost,
                    (a.quantity -
                        (CASE
                            WHEN c.total_qty IS NOT NULL
                            THEN -1.0 * c.total_qty
                            ELSE 0.0
                        END)) as total_quantity,
                    (a.cost -
                        (CASE
                            WHEN c.total_cost IS NOT NULL THEN c.total_cost
                            ELSE 0.0
                        END)) as total_cost
        """
        return select_str

    def _from(self):
        from_str = """
                l10n_id_djbc_lap_posisi_barang_helper_in_common AS a
        """
        return from_str

    def _where(self):
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join(self):
        join_str = """
        LEFT JOIN l10n_id_djbc_lap_posisi_barang_helper_out_common AS b
            ON a.lot_id = b.lot_id
        LEFT JOIN (
            SELECT c1.lot_id,
                    SUM(c1.cost) AS total_cost,
                    SUM(c1.quantity) AS total_qty
            FROM l10n_id_djbc_lap_posisi_barang_helper_out_common AS c1
            GROUP BY c1.lot_id
        ) AS c
            ON a.lot_id = c.lot_id

        """
        return join_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        cr.execute(
            """CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            %s
        )"""
            % (self._table, self._select(), self._from(), self._join(), self._where())
        )
