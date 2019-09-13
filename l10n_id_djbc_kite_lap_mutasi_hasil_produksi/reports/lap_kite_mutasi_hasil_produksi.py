# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models


class LapKiteMutasiHasilProduksi(models.Model):
    _name = "l10n_id.djbc_kite_lap_mutasi_hasil_produksi"
    _inherit = "l10n_id.djbc_kite_lap_mutasi_common"
    _description = "Laporan Mutasi Hasil Produksi Untuk KITE"
    _auto = False

    def _join(self):
        _super = super(LapKiteMutasiHasilProduksi, self)
        join_str = _super._join() + """
        JOIN product_categ_rel AS c ON
            b.id = c.product_id
        JOIN product_category AS d ON
            c.categ_id = d.id
        JOIN (
            SELECT res_id
            FROM ir_model_data AS e1
            WHERE
                e1.module = 'l10n_id_djbc_kite_common' AND
                (e1.name = 'product_categ_kite_hasil_produksi')
            ) as e ON
            d.id = e.res_id
        """
        return join_str
