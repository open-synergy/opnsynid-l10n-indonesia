# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models, fields


class KBLapMutasiMesinPeralatanWizard(models.TransientModel):
    _name = "l10n_id.kb_lap_mutasi_mesin_peralatan_wizard"
    _inherit = ["l10n_id.date_range_selector"]

    warehouse_ids = fields.Many2many(
        string="Warehouse",
        comodel_name="stock.warehouse",
        relation="rel_djbc_mesin_peralatan_2_warehouse",
        column1="wizard_id",
        column2="warehouse_id"
    )

    @api.multi
    def action_print_sreen(self):
        waction = self.env.ref(
            "l10n_id_djbc_kb_lap_mutasi_mesin_peralatan."
            "djbc_kb_lap_mutasi_mesin_peralatan_action")
        context = {
            "date_start": self.date_start,
            "date_end": self.date_end,
        }
        domain = [("warehouse_id", "in", self.warehouse_ids.ids)]
        result = waction.read()[0]
        result.update({"context": context, "domain": domain})
        return result
