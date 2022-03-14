# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp import api, fields, models


class ReturPajakMasukan(models.Model):
    _name = "l10n_id.retur_pajak_masukan"
    _description = "Retur Pajak Masukan"
    _inherit = ["l10n_id.faktur_pajak_common"]

    @api.model
    def _get_faktur_pajak_type(self):
        return self.env.ref("l10n_id_taxform_retur_pajak_masukan.fp_type_rp_masukan")

    name = fields.Char(
        string="# Retur Pajak Masukan",
    )
    enofa_nomor_dokumen = fields.Char(
        string="NOMOR_DOKUMEN_RETUR",
    )
    enofa_tanggal_dokumen = fields.Char(
        string="TANGGAL_RETUR",
    )
    enofa_masa_pajak = fields.Char(
        string="MASA_PAJAK_RETUR",
    )
    enofa_tahun_pajak = fields.Char(
        string="TAHUN_PAJAK_RETUR",
    )
    enofa_jumlah_dpp = fields.Char(
        string="NILAI_RETUR_DPP",
    )
    enofa_jumlah_ppn = fields.Char(
        string="NILAI_RETUR_PPN",
    )
    enofa_jumlah_ppnbm = fields.Char(
        string="NILAI_RETUR_PPNBM",
    )
    enofa_nomor_dokumen_balik = fields.Char(
        string="NOMOR_FAKTUR",
    )
    enofa_tanggal_dokumen_balik = fields.Char(
        string="TANGGAL_FAKTUR",
    )
    reference_id = fields.Many2one(
        string="Doc. Reference",
        comodel_name="account.move",
    )
    reference_ids = fields.Many2many(
        string="Doc. References",
        comodel_name="account.move",
        relation="rel_rp_masukan_2_move",
        column1="rp_masukan_id",
        column2="move_id",
    )
    all_reference_ids = fields.Many2many(
        string="Doc. References",
        comodel_name="account.move",
        relation="rel_rp_masukan_2_all_move",
        compute="_compute_all_reference",
        column1="rp_masukan_id",
        column2="move_id",
        store=True,
    )
    reverse_id = fields.Many2one(
        string="Reverse From",
        comodel_name="l10n_id.faktur_pajak_masukan",
    )
    substitute_id = fields.Many2one(
        string="Substitute For",
        comodel_name="l10n_id.retur_pajak_masukan",
    )

    @api.onchange("reference_id")
    def onchange_reference_id(self):
        if self.reference_id:
            self.name = self.reference_id.name
