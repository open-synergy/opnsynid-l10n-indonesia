# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp import models, fields, api


class FakturPajakMasukan(models.Model):
    _name = "l10n_id.faktur_pajak_masukan"
    _description = "Faktur Pajak Masukan"
    _inherit = ["l10n_id.faktur_pajak_common"]

    @api.model
    def _get_faktur_pajak_type(self):
        return self.env.ref(
            "l10n_id_taxform_faktur_pajak_masukan.fp_type_fp_masukan")

    reference_id = fields.Many2one(
        string="Doc. Reference",
        comodel_name="account.invoice",
        )
    reference_ids = fields.Many2many(
        string="Doc. References",
        comodel_name="account.invoice",
        relation="rel_fp_masukan_2_invoice",
        column1="fp_masukan_id",
        column2="invoice_id",
        )
    reverse_id = fields.Many2one(
        string="Reverse From",
        comodel_name="l10n_id.faktur_pajak_masukan",
        )
    substitute_id = fields.Many2one(
        string="Substitute For",
        comodel_name="l10n_id.faktur_pajak_masukan",
        )
