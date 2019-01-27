# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
from openerp import tools


class LapPlbLapPemasukan(models.Model):
    _name = "l10n_id.djbc_plb_lap_pemasukan"
    _description = "Laporan Pemasukan Barang Untuk Pusat Logistik Berikat"
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

    tgl_penerimaan = fields.Datetime(
        string="Tanggal Penerimaan"
    )

    pengirim = fields.Many2one(
        string="Pembeli/Penerima",
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

    pemilik_barang = fields.Many2one(
        string="Pemilik Barang",
        comodel_name="res.partner"
    )

    def _select(self):
        select_str = """
            SELECT  a.id as id,
                c.type_id as jenis_dokumen,
                c.name as no_dokumen,
                c.date as tgl_dokumen,
                b.name as no_penerimaan,
                a.date as tgl_penerimaan,
                b.partner_id as pengirim,
                d.default_code as kode_barang,
                a.product_id as nama_barang,
                a.product_qty as jumlah,
                a.product_uom as satuan,
                (CASE
                    WHEN g.price_subtotal IS NOT NULL
                        THEN g.price_subtotal
                    ELSE 0.0
                END) AS nilai,
                e.warehouse_id AS warehouse_id,
                b.owner_id AS pemilik_barang
        """
        return select_str

    def _from(self):
        from_str = """
            FROM stock_move AS a
        """
        return from_str

    def _where(self):
        where_str = """
            WHERE e.djbc_plb_movement_type='in'AND
                  e.djbc_plb_scrap IS FALSE AND
                  e.djbc_plb_adjustment IS FALSE
        """
        return where_str

    def _join(self):
        join_str = """
            LEFT JOIN stock_picking AS b ON
                a.picking_id = b.id
            JOIN l10n_id_djbc_custom_document AS c ON
                a.djbc_custom_document_id = c.id
            JOIN product_product AS d ON
                a.product_id = d.id
            JOIN stock_picking_type AS e ON
                a.picking_type_id = e.id
            LEFT JOIN account_invoice_line_stock_move_rel AS f ON
                a.id = f.stock_move_id
            LEFT JOIN account_invoice_line AS g ON
                f.account_invoice_line_id = g.id
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
