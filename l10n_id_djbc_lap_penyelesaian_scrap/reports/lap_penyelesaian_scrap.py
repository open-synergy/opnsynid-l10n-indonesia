# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models, tools


class LapPenyelesaianScrap(models.Model):
    _name = "l10n_id.djbc_lap_penyelesaian_scrap"
    _description = "DJBC Lap. Penyelesaian"
    _auto = False

    custom_document_id = fields.Many2one(
        string="Custom Document",
        comodel_name="l10n_id.djbc_custom_document",
        readonly=True,
    )
    custom_document_date = fields.Date(
        string="Custom Document Date",
        readonly=True,
    )
    move_id = fields.Many2one(
        string="Product",
        comodel_name="stock.move",
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
        string="Qty. Used",
        readonly=True,
    )

    def _select(self):
        select_str = """
             SELECT a.id as id,
                    a.id AS move_id,
                    a.djbc_custom_document_id AS custom_document_id,
                    e.date AS custom_document_date,
                    a.date AS move_date,
                    a.product_id AS product_id,
                    c.name AS product_name,
                    b.default_code AS product_code,
                    a.product_uom AS uom_id,
                    a.product_uom_qty AS quantity
        """
        return select_str

    def _from(self):
        from_str = """
                stock_move AS a
                JOIN product_product AS b ON a.product_id = b.id
                JOIN product_template AS c ON b.product_tmpl_id = c.id
                JOIN stock_picking_type AS d ON a.picking_type_id = d.id
                JOIN l10n_id_djbc_custom_document AS e
                    ON a.djbc_custom_document_id = e.id
        """
        return from_str

    def _where(self):
        where_str = """
                a.state = 'done' AND
                a.djbc_custom = TRUE AND
                d.djbc_lap_penyelesaian_scrap = TRUE
        """
        return where_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        cr.execute(
            """CREATE or REPLACE VIEW %s as (
            %s
            FROM ( %s )
            WHERE
            %s
            )"""
            % (self._table, self._select(), self._from(), self._where())
        )
