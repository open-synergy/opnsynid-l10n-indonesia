# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models, _
from openerp.exceptions import except_orm


class KBLapPemasukanWizard(models.TransientModel):
    _name = "l10n_id.kb_lap_pemasukan_wizard"
    _inherit = "l10n_id.date_range_selector"

    @api.multi
    def action_print_sreen(self):
        waction = self.env.ref(
            "l10n_id_djbc_kb_lap_pemasukan.djbc_kb_lap_pemasukan_action")
        criteria = [
            ("tgl_penerimaan", ">=", self.date_start),
            ("tgl_penerimaan", "<=", self.date_end),
            ("warehouse_id", "in", self.warehouse_ids.ids)
        ]
        waction.domain = criteria
        waction.update({"target": "new"})
        return waction.read()[0]

    @api.multi
    def action_print(self):
        return super(KBLapPemasukanWizard, self).action_print()
