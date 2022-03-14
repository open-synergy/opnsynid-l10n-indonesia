# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models, tools


class LapKitePemakaianBahanBakuUnion(models.Model):
    _name = "l10n_id.lap_kite_pemakaian_bahan_baku_union"
    _description = "Laporan Pemakaian Bahan Baku Union KITE"
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

    # Object: l10n_id.lap_kite_pemakaian_bahan_baku
    def _select_1(self):
        select_str = """
             SELECT id,
                    no_pengeluaran,
                    tgl_pengeluaran,
                    nama_barang,
                    kode_barang,
                    satuan,
                    jumlah_digunakan,
                    jumlah_disubkontrakkan,
                    penerima_subkontrak,
                    gudang
        """
        return select_str

    def _from_1(self):
        from_str = """
            FROM l10n_id_lap_kite_pemakaian_bahan_baku
        """
        return from_str

    # Object: l10n_id.lap_kite_pemakaian_bahan_baku_subkon
    def _select_2(self):
        select_str = """
             SELECT id,
                    no_pengeluaran,
                    tgl_pengeluaran,
                    nama_barang,
                    kode_barang,
                    satuan,
                    jumlah_digunakan,
                    jumlah_disubkontrakkan,
                    penerima_subkontrak,
                    gudang
        """
        return select_str

    def _from_2(self):
        from_str = """
            FROM l10n_id_lap_kite_pemakaian_bahan_baku_subkon
        """
        return from_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        cr.execute(
            """CREATE or REPLACE VIEW %s as (
            %s
            %s
            UNION
            %s
            %s
        )"""
            % (
                self._table,
                self._select_1(),
                self._from_1(),
                self._select_2(),
                self._from_2(),
            )
        )
