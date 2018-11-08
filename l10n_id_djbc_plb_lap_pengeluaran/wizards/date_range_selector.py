# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models, fields


class PLBLapPemasukanWizard(models.TransientModel):
    _name = "l10n_id.plb_lap_pengeluaran_wizard"
    _inherit = ["l10n_id.date_range_selector"]

    warehouse_ids = fields.Many2many(
        string="Warehouse",
        comodel_name="stock.warehouse",
        relation="rel_plb_lap_pengeluaran_2_warehouse",
        column1="wizard_id",
        column2="warehouse_id"
    )

    @api.multi
    def action_print_sreen(self):
        waction = self.env.ref(
            "l10n_id_djbc_plb_lap_pengeluaran.djbc_plb_lap_pengeluaran_action")
        criteria = [
            ("tgl_pengiriman", ">=", self.date_start),
            ("tgl_pengiriman", "<=", self.date_end),
            ("warehouse_id", "in", self.warehouse_ids.ids)
        ]
        waction.domain = criteria
        return waction.read()[0]
