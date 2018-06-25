# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class KBLapPengeluaranWizard(models.TransientModel):
    _name = "l10n_id.kb_lap_pengeluaran_wizard"
    _inherit = ["l10n_id.date_range_selector"]

    @api.multi
    def action_print_sreen(self):
        waction = self.env.ref(
            "l10n_id_djbc_kb_lap_pengeluaran.djbc_kb_lap_pengeluaran_action")
        criteria = [
            ("tgl_penerimaan", ">=", self.date_start),
            ("tgl_penerimaan", "<=", self.date_end),
            ("warehouse_id", "in", self.warehouse_ids.ids)
        ]
        waction.domain = criteria
        return waction.read()[0]
