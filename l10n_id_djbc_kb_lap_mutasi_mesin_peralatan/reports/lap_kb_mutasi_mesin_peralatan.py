# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp import tools


class LapKbMutasiMesinPeralatan(models.Model):
    _name = "l10n_id.djbc_kb_lap_mutasi_mesin_peralatan"
    _inherit = "l10n_id.djbc_kb_lap_mutasi_common"
    _description = "Laporan Mutasi Mesin?perlatan Untuk Kawasan Berikat"
    _auto = False

    def _where(self):
        _super = super(LapKbMutasiMesinPeralatan, self)
        where_str = _super._where()
        return where_str
