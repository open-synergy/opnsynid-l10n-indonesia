# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models, fields


class KBLapMutasiBarangJadiWizard(models.TransientModel):
    _name = "l10n_id.kb_lap_mutasi_barang_jadi_wizard"
    _inherit = ["l10n_id.date_range_selector"]

    warehouse_ids = fields.Many2many(
        string="Warehouse",
        comodel_name="stock.warehouse",
        relation="rel_djbc_barang_jadi_2_warehouse",
        column1="wizard_id",
        column2="warehouse_id"
    )

    @api.multi
    def action_print_sreen(self):
        waction = self.env.ref(
            "l10n_id_djbc_kb_lap_mutasi_barang_jadi."
            "djbc_kb_lap_mutasi_barang_jadi_action")
        return waction.read()[0]
