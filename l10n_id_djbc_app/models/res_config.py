# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ResConfig(models.TransientModel):
    _name = "l10n_id.djbc_config_setting"
    _inherit = "res.config.settings"

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
    )
    module_l10n_id_djbc_bc20 = fields.Boolean(
        string="Manage BC 2.0",
    )
    module_l10n_id_djbc_bc24 = fields.Boolean(
        string="Manage BC 2.4",
    )
    module_l10n_id_djbc_bc24 = fields.Boolean(
        string="Manage BC 3.0",
    )
    # KITE
    module_l10n_id_djbc_lap_mutasi_bahan_baku = fields.Boolean(
        string="Lap. Mutasi Bahan Baku",
    )
    module_l10n_id_djbc_lap_mutasi_hasil_produksi = fields.Boolean(
        string="Lap. Mutasi Hasil Produksi",
    )
    module_l10n_id_djbc_lap_pemakaian_bahan_baku = fields.Boolean(
        string="Lap. Pemakaian Bahan Baku",
    )
    module_l10n_id_djbc_lap_pemasukan_bahan_baku = fields.Boolean(
        string="Lap. Pemasukan Bahan Baku",
    )
    module_l10n_id_djbc_lap_pemasukan_hasil_produksi = fields.Boolean(
        string="Lap. Pemasukan Hasil Produksi",
    )
    module_l10n_id_djbc_lap_pengeluaran_hasil_produksi = fields.Boolean(
        string="Lap. Pengeluaran Hasil Produksi",
    )
    module_l10n_id_djbc_lap_penyelesaian_scrap = fields.Boolean(
        string="Lap. Penyelesaian Scrap",
    )
