# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models, tools


class LapKitePemakaianBahanBakuSubkon(models.Model):
    _name = "l10n_id.lap_kite_pemakaian_bahan_baku_subkon"
    _description = "Laporan Pemakaian Bahan Baku Subkontrak KITE"
    _auto = False

    no_pengeluaran = fields.Many2one(
        string="Nomor Pengeluaran",
        comodel_name="stock.picking",
    )
    tgl_pengeluaran = fields.Datetime(
        string="Tanggal Pengeluaran",
    )
    kode_barang = fields.Char(
        string="Kode Barang",
    )
    nama_barang = fields.Char(
        string="Nama Barang",
    )
    satuan = fields.Many2one(
        string="Satuan",
        comodel_name="product.uom",
    )
    jumlah_digunakan = fields.Float(
        string="Jumlah Digunakan",
    )
    jumlah_disubkontrakkan = fields.Float(
        string="Jumlah Disubkontrakan",
    )
    penerima_subkontrak = fields.Many2one(
        string="Penerima Subkontrak",
        comodel_name="res.partner",
    )
    gudang = fields.Many2one(string="Gudang", comodel_name="stock.warehouse")

    def _get_movement_type(self, cr):
        query = """
            SELECT  res_id
            FROM  ir_model_data
            WHERE
            module = 'l10n_id_djbc_kite_lap_pemakaian_bahan_baku' AND
            name = 'djbc_kite_movement_type_pemakaian_bahan_baku_subkontrak'
        """
        cr.execute(query)
        movement_type = cr.fetchone()
        if movement_type:
            return movement_type
        else:
            return 0

    def _select(self):
        select_str = """
             SELECT a.id as id,
                    a.picking_id AS no_pengeluaran,
                    a.date AS tgl_pengeluaran,
                    c.name AS nama_barang,
                    b.default_code AS kode_barang,
                    a.product_uom AS satuan,
                    0.0 AS jumlah_digunakan,
                    a.product_uom_qty AS jumlah_disubkontrakkan,
                    e.partner_id AS penerima_subkontrak,
                    d.warehouse_id AS gudang
        """
        return select_str

    def _from(self):
        from_str = """
            FROM stock_move AS a
        """
        return from_str

    def _join(self):
        join_str = """
            JOIN product_product AS b ON a.product_id = b.id
            JOIN product_template AS c ON b.product_tmpl_id = c.id
            JOIN stock_picking_type AS d ON a.picking_type_id = d.id
            LEFT JOIN stock_picking AS e ON a.picking_id = e.id
            JOIN product_categ_rel AS f ON
                c.id = f.product_id
            JOIN product_category AS g ON
                f.categ_id = g.id
            JOIN (
                SELECT res_id
                FROM ir_model_data AS e1
                WHERE
                    e1.module = 'l10n_id_djbc_kite_common' AND
                    (e1.name = 'product_categ_kite_bahan_baku')
                ) as h ON
                g.id = h.res_id
        """
        return join_str

    def _where(self, movement_type_id):
        where_str = """
            WHERE
                a.state = 'done' AND
                a.djbc_custom IS TRUE AND
                d.djbc_kite_scrap IS FALSE AND
                d.djbc_kite_movement_type_id=%s
        """ % (
            movement_type_id
        )
        return where_str

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
