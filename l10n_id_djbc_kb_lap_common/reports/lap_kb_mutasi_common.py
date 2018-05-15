# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp import tools
from lxml import etree


class LapKbMutasiCommon(models.AbstractModel):
    _name = "l10n_id.djbc_kb_lap_mutasi_common"
    _description = "Common Model for Laporan Mutasi Kawasan Berikat"
    _auto = False

    @api.multi
    def _compute_qty(self):
        for lap in self:
            lap.saldo_awal = lap.pemasukan = lap.pengeluaran = \
                lap.penyesuaian = lap.saldo_buku = lap.stock_opname = \
                lap.selisih = 0.0
            lap.keterangan = "sesuai"

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
                JOIN product_template AS b
                    ON a.product_tmpl_id = b.id
        """
        return from_str

    def _where(self):
        where_str = """
        """
        return where_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            )""" % (self._table, self._select(), self._from(), self._where()))
