# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
from openerp import tools


class LapKbLapPemasukan(models.Model):
    _name = "l10n_id.djbc_kb_lap_pemasukan"
    _description = "Laporan Pemasukan Barang Untuk Kawasan Berikat"
    _auto = False

    jenis_dokumen = fields.Many2one(
        string="Jenis Dokumen",
        comodel_name="l10n_id.djbc_document_type"
    )

    no_dokumen = fields.Char(
        string="No. Dokumen"
    )

    tgl_dokumen = fields.Date(
        string="Tanggal Dokumen"
    )

    no_penerimaan = fields.Char(
        string="Nomor Penerimaan"
    )

    tgl_penerimaan = fields.Char(
        string="Tanggal Penerimaan"
    )

    pengirim = fields.Many2one(
        string="Pengirim Barang",
        comodel_name="res.partner"
    )

    kode_barang = fields.Char(
        string="Kode Barang"
    )

    nama_barang = fields.Many2one(
        string="Nama Barang",
        comodel_name="product.product"
    )

    jumlah = fields.Float(
        string="Jumlah"
    )

    satuan = fields.Many2one(
        string="Satuan",
        comodel_name="product.uom"
    )

    nilai = fields.Float(
        string="Nilai"
    )

    warehouse_id = fields.Many2one(
        string="Warehouse",
        comodel_name="stock.warehouse"
    )

    def _select(self):
        select_str = """
            SELECT  a.id as id,
                C.type_id as jenis_dokumen,
                C.name as no_dokumen,
                C.date as tgl_dokumen,
                B.name as no_penerimaan,
                A.date as tgl_penerimaan,
                B.partner_id as pengirim,
                D.default_code as kode_barang,
                A.product_id as nama_barang,
                A.product_qty as jumlah,
                A.product_uom as satuan,
                F.nilai as nilai,
                E.warehouse_id AS warehouse_id
        """
        return select_str

    def _from(self):
        from_str = """
            FROM stock_move AS A
        """
        return from_str

    def _where(self):
        where_str = """
            WHERE E.djbc_kb_movement_type='in' AND
                  E.djbc_kb_scrap IS FALSE AND
                  E.djbc_kb_adjustment IS FALSE
        """
        return where_str

    def _join(self):
        join_str = """
            LEFT JOIN stock_picking AS B ON A.picking_id=B.id
            JOIN l10n_id_djbc_custom_document AS C
                ON A.djbc_custom_document_id=C.id
            JOIN product_product AS D ON A.product_id=D.id
            JOIN stock_picking_type AS E ON A.picking_type_id=E.id
            JOIN
            (
                SELECT F1.move_id,
                SUM(G1.qty*G1.cost) AS nilai
                FROM stock_quant_move_rel AS F1
                JOIN stock_quant AS G1 ON F1.quant_id=G1.id
                GROUP BY F1.move_id
            ) AS F ON F.move_id=A.id
        """
        return join_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            %s
            %s
            %s
        )""" % (
            self._table,
            self._select(),
            self._from(),
            self._join(),
            self._where()
        ))
