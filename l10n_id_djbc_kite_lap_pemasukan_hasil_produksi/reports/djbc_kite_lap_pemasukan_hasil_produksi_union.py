# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
from openerp import tools


class LapKitePemasukanHasilProduksiUnion(models.Model):
    _name = "l10n_id.lap_kite_pemasukan_hasil_produksi_union"
    _description = "Laporan Pemasukan Hasil Produksi Union KITE"
    _auto = False

    no_penerimaan = fields.Many2one(
        string="Nomor Penerimaan",
        comodel_name="stock.picking",
    )
    tgl_penerimaan = fields.Datetime(
        string="Tanggal Penerimaan",
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
    jumlah_produksi = fields.Float(
        string="Jumlah Dari Produksi",
    )
    jumlah_disubkontrakkan = fields.Float(
        string="Jumlah Disubkontrakan",
    )
    gudang = fields.Many2one(
        string="Gudang",
        comodel_name="stock.warehouse"
    )

    # Object: l10n_id.lap_kite_pemasukan_hasil_produksi
    def _select_1(self):
        select_str = """
             SELECT id,
                    no_penerimaan,
                    tgl_penerimaan,
                    nama_barang,
                    kode_barang,
                    satuan,
                    jumlah_produksi,
                    jumlah_disubkontrakkan,
                    gudang
        """
        return select_str

    def _from_1(self):
        from_str = """
            FROM l10n_id_lap_kite_pemasukan_hasil_produksi
        """
        return from_str

    # Object: l10n_id.lap_kite_pemasukan_hasil_produksi_subkon
    def _select_2(self):
        select_str = """
             SELECT id,
                    no_penerimaan,
                    tgl_penerimaan,
                    nama_barang,
                    kode_barang,
                    satuan,
                    jumlah_produksi,
                    jumlah_disubkontrakkan,
                    gudang
        """
        return select_str

    def _from_2(self):
        from_str = """
            FROM l10n_id_lap_kite_pemasukan_hasil_produksi_subkon
        """
        return from_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            %s
            UNION
            %s
            %s
        )""" % (
            self._table,
            self._select_1(),
            self._from_1(),
            self._select_2(),
            self._from_2(),
        ))
