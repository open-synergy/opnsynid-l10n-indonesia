# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp import tools


class LapKbMutasiBahanBakuPenolong(models.Model):
    _name = "l10n_id.djbc_kb_lap_mutasi_bahan_baku_penolong"
    _inherit = "l10n_id.djbc_kb_lap_mutasi_common"
    _description = "Laporan Mutasi Bahan Baku/Penolong Untuk Kawasan Berikat"
    _auto = False

    def _join(self):
        _super = super(LapKbMutasiBahanBakuPenolong, self)
        join_str = _super._join() + """
        JOIN product_categ_rel AS c ON
            b.id = c.product_id
        JOIN product_category AS d ON
            c.categ_id = d.id
        JOIN (
            SELECT res_id
            FROM ir_model_data AS e1
            WHERE 
                e1.module = 'l10n_id_djbc_kb_lap_common' AND
                (e1.name = 'product_categ_kb_bahan_baku' OR
                e1.name = 'product_categ_kb_bahan_penolong')
            ) as e ON
            d.id = e.res_id
        """
        return join_str
