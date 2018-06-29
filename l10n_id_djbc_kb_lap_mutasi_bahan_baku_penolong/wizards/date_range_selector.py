# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class KBLapMutasiBahanBakuWizard(models.TransientModel):
    _name = "l10n_id.kb_lap_mutasi_bahan_baku_wizard"
    _inherit = ["l10n_id.date_range_selector"]

    @api.multi
    def action_print_sreen(self):
        waction = self.env.ref(
            "l10n_id_djbc_kb_lap_mutasi_bahan_baku_penolong."
            "djbc_kb_lap_mutasi_bahan_baku_penolong_action")
        return waction.read()[0]
