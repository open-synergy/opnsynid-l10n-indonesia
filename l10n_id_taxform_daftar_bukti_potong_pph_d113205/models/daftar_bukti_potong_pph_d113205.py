# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class DaftarBuktiPotongPPhD113205(models.Model):
    _name = "l10n_id.daftar_bukti_potong_pph_d113205"
    _inherit = "l10n_id.daftar_bukti_potong_pph"
    _description = "Daftar Bukti Potong PPh 23/26"

    @api.model
    def _default_type_id(self):
        return self.env.ref(
            "l10n_id_taxform_daftar_bukti_potong_pph_d113205."
            "daftar_bukti_potong_pph_type_d113205").id

    type_id = fields.Many2one(
        default=lambda self: self._default_type_id(),
    )
    pemotong_pajak_id = fields.Many2one(
        related="company_id.partner_id",
        store=True,
    )
    bukpot_23_ids = fields.Many2many(
        string="Bukti Potong PPh 23",
        comodel_name="l10n_id.bukti_potong_pph_23_out",
        relation="rel_daftar_bukpot_23_2_bukpot",
        column1="daftar_bukpot_id",
        column2="bukpot_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        }
    )
    bukpot_26_ids = fields.Many2many(
        string="Bukti Potong PPh 26",
        comodel_name="l10n_id.bukti_potong_pph_f113308_out",
        relation="rel_daftar_bukpot_26_2_bukpot",
        column1="daftar_bukpot_id",
        column2="bukpot_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        }
    )
