# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp import tools


class LapKbMutasiCommon(models.AbstractModel):
    _name = "l10n_id.djbc_kb_lap_mutasi_common"
    _description = "Common Model for Laporan Mutasi Kawasan Berikat"
    _auto = False

    @api.multi
    def _qty_from(self):
        self.ensure_one()
        str_select = """
        FROM stock_move AS a
        JOIN stock_picking_type AS b ON a.picking_type_id = b.id
        JOIN stock_location AS c ON a.location_id = c.id
        JOIN stock_location AS d ON a.location_dest_id =d.id
        """
        return str_select

    @api.multi
    def _qty_where(self, date_start, date_end, movement_type="in", scrap=False):
        self.ensure_one()
        str_where = """
        WHERE
            a.product_id = %s AND
            b.djbc_kb_movement_type = '%s' AND
            b.djbc_kb_scrap %s AND
            a.date >= '%s' AND
            a.date <= '%s'
        """ % (self.product_id.id, movement_type, scrap and 'IS NOT NULL'or 'IS NULL', date_start, date_end)
        return str_where

    @api.multi
    def _qty_join(self):
        self.ensure_one()
        pass

    @api.multi
    def _qty_select(self):
        self.ensure_one()
        str_select = """
        SELECT
            a.product_uom_qty AS qty
        """
        return str_select



    @api.multi
    def _compute_qty(self):
        date_start = self._context.get("date_start", False)
        date_end = self._context.get("date_end", False)

        for lap in self:
            lap.saldo_awal = lap.pemasukan = lap.pengeluaran = \
                lap.penyesuaian = lap.saldo_buku = lap.stock_opname = \
                lap.selisih = 0.0
            lap.pemasukan = lap._get_qty(
                date_start, date_end, "in", False)
            lap.keterangan = "sesuai"

    @api.multi
    def _get_qty(self, date_start, date_end, movement_type, scrap):
        self.ensure_one()
        result = 0.0
        str_sql = """
        %s
        %s
        %s
        """ % (self._qty_select(), self._qty_from(), self._qty_where(date_start, date_end, movement_type, scrap))
        self.env.cr.execute(str_sql)
        for row in self.env.cr.dictfetchall():
            result += row["qty"]
        return result








    kode_barang = fields.Char(
        string="Kode Barang",
        readonly=True,
        )
    product_id = fields.Many2one(
        string="Nama Barang",
        comodel_name="product.product",
        readonly=True,
        )
    uom_id = fields.Many2one(
        string="Satuan",
        comodel_name="product.uom",
        readonly=True,
        )
    saldo_awal = fields.Float(
        string="Saldo Awal",
        readonly=True,
        compute="_compute_qty",
        store=False,
        )
    pemasukan = fields.Float(
        string="Pemasukan",
        readonly=True,
        compute="_compute_qty",
        store=False,
        )
    pengeluaran = fields.Float(
        string="Pengeluaran",
        readonly=True,
        compute="_compute_qty",
        store=False,
        )
    penyesuaian = fields.Float(
        string="Penyesuaian",
        readonly=True,
        compute="_compute_qty",
        store=False,
        )
    stock_opname = fields.Float(
        string="Stock Opname",
        readonly=True,
        compute="_compute_qty",
        store=False,
        )
    saldo_akhir = fields.Float(
        string="Saldo Buku",
        readonly=True,
        compute="_compute_qty",
        store=False,
        )
    selisih = fields.Float(
        string="Selisih",
        readonly=True,
        compute="_compute_qty",
        store=False,
        )
    keterangan = fields.Selection(
        string="Ket",
        compute="_compute_qty",
        store=False,
        selection=[
            ("sesuai", "Sesuai"),
            ("kurang", "Selisih Kurang"),
            ("lebih", "Selisih Lebih"),
            ],
        )

    def _select(self):
        select_str = """
             SELECT a.id as id,
                    a.default_code AS kode_barang,
                    a.id AS product_id,
                    b.uom_id AS uom_id
        """
        return select_str

    def _from(self):
        from_str = """
                product_product AS a
        """
        return from_str

    def _where(self):
        where_str = """
        """
        return where_str

    def _join(self):
        join_str = """
        JOIN product_template AS b
            ON a.product_tmpl_id = b.id
        """
        return join_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            %s
            )""" % (self._table, self._select(), self._from(), self._join(), self._where()))
