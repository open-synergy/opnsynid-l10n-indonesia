# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models, tools


class LapKitePemasukanBahanBaku(models.Model):
    _name = "l10n_id.lap_kite_pemasukan_bahan_baku"
    _description = "Laporan Pemasukan Bahan Baku Untuk KITE"
    _auto = False

    jenis_dokumen = fields.Many2one(
        string="Jenis Dokumen",
        comodel_name="l10n_id.djbc_document_type",
    )
    no_dokumen = fields.Char(
        string="No. Dokumen",
    )
    tgl_dokumen = fields.Date(
        string="Tanggal Dokumen",
    )
    no_seri_barang = fields.Many2one(
        string="Nomor Seri Barang",
        comodel_name="stock.production.lot",
    )
    no_penerimaan = fields.Char(
        string="Nomor Penerimaan",
    )
    tgl_penerimaan = fields.Char(
        string="Tanggal Penerimaan",
    )
    kode_barang = fields.Char(
        string="Kode Barang",
    )
    nama_barang = fields.Many2one(
        string="Nama Barang",
        comodel_name="product.product",
    )
    satuan = fields.Many2one(
        string="Satuan",
        comodel_name="product.uom",
    )
    jumlah = fields.Float(
        string="Jumlah",
    )
    mata_uang = fields.Many2one(
        string="Mata Uang",
        comodel_name="res.currency",
    )
    nilai = fields.Float(
        string="Nilai",
    )
    gudang = fields.Many2one(
        string="Gudang",
        comodel_name="stock.warehouse",
    )
    penerima_subkontrak = fields.Many2one(
        string="Penerima Subkontrak",
        comodel_name="res.partner",
    )
    negara_asal_barang = fields.Many2one(
        string="Negara Asal Barang",
        comodel_name="res.country",
    )

    def _get_movement_type(self, cr):
        query = """
            SELECT  res_id
            FROM  ir_model_data
            WHERE
            module = 'l10n_id_djbc_kite_lap_pemasukan_bahan_baku' AND
            name = 'djbc_kite_movement_type_pemasukan_bahan_baku'
        """
        cr.execute(query)
        movement_type = cr.fetchone()
        if movement_type:
            return movement_type
        else:
            return 0

    def _select(self):
        select_str = """
            SELECT
                a.id as id,
                c.type_id as jenis_dokumen,
                c.name as no_dokumen,
                c.date as tgl_dokumen,
                a.restrict_lot_id as no_seri_barang,
                b.name as no_penerimaan,
                a.date as tgl_penerimaan,
                d.default_code as kode_barang,
                a.product_id as nama_barang,
                a.product_uom as satuan,
                a.product_qty as jumlah,
                h.currency_id AS mata_uang,
                f.nilai as nilai,
                e.warehouse_id AS gudang,
                b.partner_id as penerima_subkontrak,
                m.country_id AS negara_asal_barang
        """
        return select_str

    def _from(self):
        from_str = """
            FROM stock_move AS a
        """
        return from_str

    def _where(self, movement_type_id):
        where_str = """
            WHERE
                a.state = 'done' AND
                a.djbc_custom IS TRUE AND
                e.djbc_kite_scrap IS FALSE AND
                e.djbc_kite_movement_type_id=%s
        """ % (
            movement_type_id
        )
        return where_str

    def _join(self):
        join_str = """
            JOIN stock_picking AS b ON a.picking_id=b.id
            JOIN l10n_id_djbc_custom_document AS c
                ON a.djbc_custom_document_id=c.id
            JOIN product_product AS d ON a.product_id=d.id
            JOIN stock_picking_type AS e ON a.picking_type_id=e.id
            JOIN
            (
                SELECT sqmr.move_id,
                SUM(sq.qty*sq.cost) AS nilai
                FROM stock_quant_move_rel AS sqmr
                JOIN stock_quant AS sq ON sqmr.quant_id=sq.id
                GROUP BY sqmr.move_id
            ) AS f ON f.move_id=a.id
            JOIN purchase_order_line AS g ON a.purchase_line_id = g.id
            JOIN purchase_order AS h ON g.order_id = h.id
            JOIN product_template AS i
                ON d.product_tmpl_id = i.id
            JOIN product_categ_rel AS j ON
                i.id = j.product_id
            JOIN product_category AS k ON
                j.categ_id = k.id
            JOIN (
                SELECT res_id
                FROM ir_model_data AS e1
                WHERE
                    e1.module = 'l10n_id_djbc_kite_common' AND
                    (e1.name = 'product_categ_kite_bahan_baku')
                ) as l ON
                k.id = l.res_id
            LEFT JOIN res_partner AS m ON b.origin_address_id = m.id
        """
        return join_str

    def _order_by(self):
        join_str = """
            ORDER BY a.date, a.id
        """
        return join_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        movement_type_id = self._get_movement_type(cr)
        cr.execute(
            """CREATE or REPLACE VIEW %s as (
            %s
            %s
            %s
            %s
            %s
        )"""
            % (
                self._table,
                self._select(),
                self._from(),
                self._join(),
                self._where(movement_type_id),
                self._order_by(),
            )
        )
