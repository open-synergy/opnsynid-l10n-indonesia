# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class FakturPajakType(models.Model):
    _name = "l10n_id.faktur_pajak_type"
    _description = "Faktur Pajak Type"

    name = fields.Char(
        string="Transaction Type",
        required=True,
    )

    description = fields.Text(
        string="Description",
    )
    fp_direction = fields.Selection(
        string="Jenis Faktur Pajak",
        selection=[
            ("masukan", "Masukan"),
            ("keluaran", "Keluaran"),
        ],
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    allowed_invoice_journal_ids = fields.Many2many(
        string="Allowed Invoice Journals",
        domain=[
            (
                "type",
                "in",
                ["sale", "sale_refund", "purchase", "purchase_refund"],
            ),
        ],
        comodel_name="account.journal",
        relation="rel_fp_type_2_journal",
        column1="fp_type_id",
        column2="journal_id",
    )
    allowed_ppn_tax_ids = fields.Many2many(
        string="Allowed PPn Taxes",
        comodel_name="account.tax",
        relation="rel_fp_type_2_ppn_tax",
        column1="fp_type_id",
        column2="tax_id",
    )
    allowed_ppnbm_tax_ids = fields.Many2many(
        string="Allowed PPnBM Taxes",
        comodel_name="account.tax",
        relation="rel_fp_type_2_ppnbm_tax",
        column1="fp_type_id",
        column2="tax_id",
    )
    allowed_transaction_type_ids = fields.Many2many(
        string="Allowed Transaction Types",
        comodel_name="l10n_id.faktur_pajak_transaction_type",
        relation="rel_fp_type_2_trans_type",
        column1="fp_type_id",
        column2="transaction_type_id",
    )
    allowed_additional_flag_ids = fields.Many2many(
        string="Allowed Additional Tags",
        comodel_name="l10n_id.faktur_pajak_additional_flag",
        relation="rel_fp_type_2_additional_flag",
        column1="fp_type_id",
        column2="additional_flag_id",
    )
    allow_reverse = fields.Boolean(
        string="Allow to Reverse Document",
    )
    allow_substitute = fields.Boolean(
        string="Allow to Substitute Document",
    )
    allow_creditable = fields.Boolean(
        string="Allow to Creditable",
    )
    allow_multiple_reference = fields.Boolean(
        string="Allow Multiple Doc. References",
    )
