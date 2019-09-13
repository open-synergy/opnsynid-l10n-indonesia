# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
from openerp import tools


class LapKitePengeluaranHasilProduksi(models.Model):
    _name = "l10n_id.lap_kite_pengeluaran_hasil_produksi"
    _description = "Laporan Pengeluaran Hasil Produksi KITE"
    _auto = False

    no_peb = fields.Many2one(
        string="No. PEB",
        comodel_name="l10n_id.djbc_custom_document",
    )
    tgl_peb = fields.Date(
        string="Tgl. PEB",
        readonly=True,
    )
    no_pengeluaran = fields.Many2one(
        string="No. Pengeluaran",
        comodel_name="stock.picking",
    )
    tgl_pengeluaran = fields.Datetime(
        string="Tgl. Pengeluaran",
    )
    penerima = fields.Many2one(
        string="Pembeli/Penerima",
        comodel_name="res.partner",
    )
    negara_tujuan = fields.Many2one(
        string="Negara Tujuan",
        comodel_name="res.country",
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
    jumlah = fields.Float(
        string="Jumlah",
    )
    mata_uang = fields.Many2one(
        string="Mata Uang",
        comodel_name="res.currency",
    )
    nilai = fields.Float(
        string="Nilai"
    )
    gudang = fields.Many2one(
        string="Gudang",
        comodel_name="stock.warehouse"
    )

    def _get_movement_type(self, cr):
        query = """
            SELECT  res_id
            FROM  ir_model_data
            WHERE
            module = 'l10n_id_djbc_kite_lap_pengeluaran_hasil_produksi' AND
            name = 'djbc_kite_movement_type_pengeluaran_hasil_produksi'
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
                a.djbc_custom_document_id AS no_peb,
                b.date AS tgl_peb,
                a.picking_id AS no_pengeluaran,
                a.date AS tgl_pengeluaran,
                f.partner_id AS penerima,
                g.country_id AS negara_tujuan,
                c.default_code AS kode_barang,
                d.name AS nama_barang,
                a.product_uom AS satuan,
                a.product_uom_qty AS jumlah,
                l.currency_id AS mata_uang,
                e1.nilai as nilai,
                e.warehouse_id AS gudang
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
        """ % (movement_type_id)
        return where_str

    def _join(self):
        join_str = """
            JOIN  l10n_id_djbc_custom_document AS b ON
                  a.djbc_custom_document_id = b.id
            JOIN  product_product AS c ON a.product_id = c.id
            JOIN  product_template AS d ON c.product_tmpl_id = d.id
            JOIN  stock_picking_type AS e ON a.picking_type_id = e.id
            JOIN
            (
                SELECT sqmr.move_id,
                SUM(sq.qty*sq.cost) AS nilai
                FROM stock_quant_move_rel AS sqmr
                JOIN stock_quant AS sq ON sqmr.quant_id=sq.id
                GROUP BY sqmr.move_id
            ) AS e1 ON e1.move_id=a.id
            JOIN  stock_picking AS f ON a.picking_id = f.id
            LEFT JOIN res_partner AS g ON f.delivery_address_id = g.id
            JOIN  stock_location AS h ON a.location_id = h.id
            JOIN  procurement_order AS i ON a.procurement_id = i.id
            JOIN  sale_order_line AS j ON i.sale_line_id = j.id
            JOIN  sale_order AS k ON j.order_id = k.id
            JOIN  product_pricelist AS l ON k.pricelist_id = l.id
            JOIN  product_categ_rel AS m ON d.id = m.product_id
            JOIN  product_category AS n ON m.categ_id = n.id
            JOIN (
                SELECT res_id
                FROM ir_model_data AS e1
                WHERE
                    e1.module = 'l10n_id_djbc_kite_common' AND
                    (e1.name = 'product_categ_kite_hasil_produksi')
            ) as o ON
            n.id = o.res_id
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
        movement_type_id =\
            self._get_movement_type(cr)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            %s
            %s
            %s
            %s
        )""" % (
            self._table,
            self._select(),
            self._from(),
            self._join(),
            self._where(movement_type_id),
            self._order_by(),
        ))
