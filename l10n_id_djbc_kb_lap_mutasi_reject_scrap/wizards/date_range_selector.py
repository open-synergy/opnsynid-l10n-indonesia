# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class DateRangeSelector(models.TransientModel):
    _inherit = "l10n_id.date_range_selector"

    @api.multi
    def action_mutasi_reject_scrap(self):
        self.ensure_one()
        waction = self.env.ref(
            "l10n_id_djbc_kb_lap_mutasi_reject_scrap."
            "djbc_kb_lap_mutasi_reject_scrap_action")
        return waction.read()[0]
