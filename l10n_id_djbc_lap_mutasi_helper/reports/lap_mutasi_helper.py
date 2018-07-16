# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp import tools
from lxml import etree


class LapMutasiHelper(models.Model):
    _name = "l10n_id.djbc_lap_mutasi_helper"
    _description = "DJBC Lap. Mutasi Helper"
    _auto = False
    _order = "date_start asc"

    @api.depends(
        "report_period_id",
        "date_start", "date_end",
        "product_id", "warehouse_id",
    )
    @api.multi
    def _compute_all(self):
        obj_move = self.env["stock.move"]
        for helper in self:
            helper.beginning_balance_qty = 0.0
            helper.stock_in_qty = 0.0
            helper.stock_out_qty = 0.0
            helper.ending_balance_qty = 0.0
            date_start = helper.report_period_id.date_start + " 00:00:00"
            date_end = helper.report_period_id.date_end + " 23:59:00"
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
                ("location_id.usage", "!=", "internal"),
            ]
            for move in obj_move.search(criteria1):
                helper.beginning_balance_qty += move.product_qty
            criteria2 = criteria + [
                ("location_id.id", "child_of",
                 helper.warehouse_id.view_location_id.id),
                ("location_id.usage", "=", "internal"),
                ("date", "<", date_start),
                ("location_dest_id.usage", "!=", "internal"),
            ]
            for move in obj_move.search(criteria2):
                helper.beginning_balance_qty -= move.product_qty
            criteria3 = criteria + [
                ("location_dest_id.id", "child_of",
                 helper.warehouse_id.view_location_id.id),
                ("location_dest_id.usage", "=", "internal"),
                ("date", ">", date_start),
                ("date", "<", date_end),
                ("location_id.usage", "!=", "internal"),
            ]
            for move in obj_move.search(criteria3):
                helper.stock_in_qty += move.product_qty
            criteria4 = criteria + [
                ("location_id.id", "child_of",
                 helper.warehouse_id.view_location_id.id),
                ("location_id.usage", "=", "internal"),
                ("date", ">", date_start),
                ("date", "<", date_end),
                ("location_dest_id.usage", "!=", "internal"),
            ]
            for move in obj_move.search(criteria4):
                helper.stock_out_qty += move.product_qty
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
        compute="_compute_all",
    )
    stock_out_qty = fields.Float(
        string="Stock Out Qty.",
        readonly=True,
        compute="_compute_all",
    )
    ending_balance_qty = fields.Float(
        string="Ending Balance Qty.",
        readonly=True,
        compute="_compute_all",
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
        # pylint: disable=locally-disabled, sql-injection
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM ( %s )
            WHERE
            %s
            ORDER BY b.date_start DESC
            )""" % (self._table, self._select(), self._from(), self._where()))

    @api.model
    def fields_view_get(self, view_id=None,
                        view_type=False, toolbar=False,
                        submenu=False):
        res = super(LapMutasiHelper, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)

        doc = etree.XML(res["arch"])
        obj_product = self.env["product.product"]
        obj_period = self.env["l10n_id.djbc_report_period"]
        obj_warehouse = self.env["stock.warehouse"]
        rm_filter = doc.xpath("//group[@name='filter_rm']")
        wip_filter = doc.xpath("//group[@name='filter_wip']")
        fg_filter = doc.xpath("//group[@name='filter_fg']")
        wh_filter = doc.xpath("//group[@name='filter_warehouse']")
        period_filter = doc.xpath("//group[@name='filter_period']")

        if view_type == "search" and wh_filter:
            for warehouse in obj_warehouse.search([]):
                filter_name = "filter_wh_%s" % (str(warehouse.id))
                filter_string = "%s" % (str(warehouse.name))
                fdomain = "[('warehouse_id.id', '=', %s)]" \
                    % (str(warehouse.id))
                xelement = etree.Element(
                    "filter", {"name": filter_name,
                               "string": filter_string,
                               "domain": fdomain,
                               })
                wh_filter[0].insert(0, xelement)
        if view_type == "search" and period_filter:
            for period in obj_period.search([]):
                filter_name = "filter_period_%s" % (str(period.id))
                filter_string = "%s" % (str(period.name))
                fdomain = "[('report_period_id.id', '=', %s)]" \
                    % (str(period.id))
                xelement = etree.Element(
                    "filter", {"name": filter_name,
                               "string": filter_string,
                               "domain": fdomain,
                               })
                period_filter[0].insert(0, xelement)
        if view_type == "search" and rm_filter:
            criteria = [
                ("djbc_rm", "=", True),
            ]
            for product in obj_product.search(criteria):
                filter_name = "filter_rm_%s" % (str(product.id))
                filter_string = "%s" % (str(product.name))
                fdomain = "[('product_id.id', '=', %s)]" \
                    % (str(product.id))
                xelement = etree.Element(
                    "filter", {"name": filter_name,
                               "string": filter_string,
                               "domain": fdomain,
                               })
                rm_filter[0].insert(0, xelement)
        if view_type == "search" and wip_filter:
            criteria = [
                ("djbc_wip", "=", True),
            ]
            for product in obj_product.search(criteria):
                filter_name = "filter_wip_%s" % (str(product.id))
                filter_string = "%s" % (str(product.name))
                fdomain = "[('product_id.id', '=', %s)]" \
                    % (str(product.id))
                xelement = etree.Element(
                    "filter", {"name": filter_name,
                               "string": filter_string,
                               "domain": fdomain,
                               })
                wip_filter[0].insert(0, xelement)
        if view_type == "search" and fg_filter:
            criteria = [
                ("djbc_fg", "=", True),
            ]
            for product in obj_product.search(criteria):
                filter_name = "filter_fg_%s" % (str(product.id))
                filter_string = "%s" % (str(product.name))
                fdomain = "[('product_id.id', '=', %s)]" \
                    % (str(product.id))
                xelement = etree.Element(
                    "filter", {"name": filter_name,
                               "string": filter_string,
                               "domain": fdomain,
                               })
                fg_filter[0].insert(0, xelement)

        res["arch"] = etree.tostring(doc)

        return res
