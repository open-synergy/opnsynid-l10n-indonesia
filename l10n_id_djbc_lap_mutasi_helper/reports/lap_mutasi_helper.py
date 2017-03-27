# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp import tools


class LapMutasiHelper(models.Model):
    _name = "l10n_id.djbc_lap_mutasi_helper"
    _description = "DJBC Lap. Mutasi Helper"
    _auto = False

    @api.multi
    def _compute_all(self):
        obj_move = self.env["stock.move"]
        for helper in self:
            helper.beginning_balance_qty = 0.0
            helper.stock_in_qty = 0.0
            date_start = helper.date_start + " 00:00:00"
            date_end = helper.date_end + " 23:59:00"
            criteria = [
                ("djbc_custom", "=", True),
                ("product_id.id", "=", helper.product_id.id),
                ("state", "=", "done"),
            ]
            criteria1 = criteria + [
                ("location_dest_id.id", "child_of",
                 helper.warehouse_id.view_location_id.id),
                ("location_dest_id.usage", "=", "internal"),
                ("date", "<", date_start),
            ]
            for move in obj_move.search(criteria1):
                helper.beginning_balance_qty += move.product_qty
            criteria2 = criteria + [
                ("location_id.id", "child_of",
                 helper.warehouse_id.view_location_id.id),
                ("location_id.usage", "=", "internal"),
                ("date", "<", date_start),
            ]
            for move in obj_move.search(criteria2):
                helper.beginning_balance_qty -= move.product_qty
            criteria3 = criteria + [
                ("location_dest_id.id", "child_of",
                 helper.warehouse_id.view_location_id.id),
                ("location_dest_id.usage", "=", "internal"),
                ("date", ">", date_start),
                ("date", "<", date_end),
            ]
            for move in obj_move.search(criteria3):
                helper.stock_in_qty += move.product_qty
            criteria4 = criteria + [
                ("location_id.id", "child_of",
                 helper.warehouse_id.view_location_id.id),
                ("location_id.usage", "=", "internal"),
                ("date", ">", date_start),
                ("date", "<", date_end),
            ]
            for move in obj_move.search(criteria4):
                helper.stock_out_qty -= move.product_qty
            helper.ending_balance_qty = helper.beginning_balance_qty + \
                helper.stock_in_qty - \
                helper.stock_out_qty

    report_period_id = fields.Many2one(
        string="Reporting Period",
        comodel_name="l10n_id.djbc_report_period",
        readonly=True,
    )
    date_start = fields.Date(
        string="Date Start",
        readonly=True,
    )
    date_end = fields.Date(
        string="Date End",
        readonly=True,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        readonly=True,
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
        readonly=True,
    )
    djbc_rm = fields.Boolean(
        string="DJBC RM",
    )
    djbc_fg = fields.Boolean(
        string="DJBC FG",
    )
    djbc_wip = fields.Boolean(
        string="DJBC WIP",
    )
    beginning_balance_qty = fields.Float(
        string="Beginning Balance Qty.",
        readonly=True,
        compute="_compute_all",
    )
    stock_in_qty = fields.Float(
        string="Stock In Qty.",
        readonly=True,
    )
    stock_out_qty = fields.Float(
        string="Stock Out Qty.",
        readonly=True,
    )
    ending_balance_qty = fields.Float(
        string="Ending Balance Qty.",
        readonly=True,
    )
    warehouse_id = fields.Many2one(
        string="Warehouse",
        comodel_name="stock.warehouse",
        readonly=True,
    )

    def _select(self):
        select_str = """
             SELECT row_number() OVER() AS id,
                    a.report_period_id AS report_period_id,
                    b.date_start AS date_start,
                    b.date_end AS date_end,
                    a.product_id AS product_id,
                    e.uom_id AS uom_id,
                    e.djbc_rm AS djbc_rm,
                    e.djbc_fg AS djbc_fg,
                    e.djbc_wip AS djbc_wip,
                    0.0 AS beginning_balance_qty,
                    0.0 AS stock_in_qty,
                    0.0 AS stock_out_qty,
                    0.0 AS ending_balance_qty,
                    a.warehouse_id AS warehouse_id
        """
        return select_str

    def _from(self):
        from_str = """
                (
                SELECT  a1.id AS report_period_id,
                        a2.id AS warehouse_id,
                        a3.id AS product_id
                FROM
                l10n_id_djbc_report_period AS a1
                CROSS JOIN stock_warehouse AS a2
                CROSS JOIN product_product AS a3
                ) AS a
                JOIN l10n_id_djbc_report_period AS b
                    ON a.report_period_id = b.id
                JOIN stock_warehouse AS c
                    ON a.warehouse_id = c.id
                JOIN product_product AS d
                    ON a.product_id = d.id
                JOIN product_template AS e
                    ON d.product_tmpl_id = e.id
        """
        return from_str

    def _where(self):
        where_str = """
                (
                e.djbc_rm = TRUE OR
                e.djbc_fg = TRUE OR
                e.djbc_wip = TRUE
                )
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
