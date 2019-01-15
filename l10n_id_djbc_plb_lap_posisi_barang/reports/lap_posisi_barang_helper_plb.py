# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models


class LapPosisiBarangHelperPlb(models.AbstractModel):
    _name = "l10n_id.djbc_lap_posisi_barang_helper_plb"
    _inherit = "l10n_id.djbc_lap_posisi_barang_helper_common"
    _auto = False

    def _where(self):
        _super = super(LapPosisiBarangHelperPlb, self)
        where_str = _super._where()
        where_str += """
        AND e.djbc_plb_ok = TRUE
        """
        return where_str

    def _join(self):
        _super = super(LapPosisiBarangHelperPlb, self)
        join_str = _super._join()
        join_str += """
        JOIN product_product AS d
            ON a.product_id = d.id
        JOIN product_template AS e
            ON d.product_tmpl_id = e.id

        """
        return join_str
