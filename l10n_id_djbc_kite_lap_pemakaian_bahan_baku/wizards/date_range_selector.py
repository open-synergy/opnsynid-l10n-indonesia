# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models, fields


class KitePemakaianBahanBakuWizard(models.TransientModel):
    _name = "l10n_id.kite_pemakaian_bahan_baku_wizard"
    _inherit = [
        "l10n_id.date_range_selector"
    ]

    warehouse_ids = fields.Many2many(
        string="Warehouse",
        comodel_name="stock.warehouse",
        relation="rel_kite_pemakaian_baku_2_warehouse",
        column1="wizard_id",
        column2="warehouse_id"
    )

    @api.multi
    def action_print_sreen(self):
        waction = self.env.ref(
            "l10n_id_djbc_kite_lap_pemakaian_bahan_baku."
            "lap_kite_pemakaian_bahan_baku_action")
        criteria = [
            ("tgl_pengeluaran", ">=", self.date_start),
            ("tgl_pengeluaran", "<=", self.date_end),
            ("gudang", "in", self.warehouse_ids.ids)
        ]
        waction.domain = criteria
        return waction.read()[0]
