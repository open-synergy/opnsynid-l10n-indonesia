# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class FakturPajakTransactionType(models.Model):
    _name = "l10n_id.faktur_pajak_transaction_type"
    _description = "Faktur Pajak Transaction Type"

    code = fields.Char(
        string="Code",
        required=True,
    )
    name = fields.Char(
        string="Transaction Type",
        required=True,
    )
    allowed_base_tax_code_ids = fields.One2many(
        string="Allowed Base Tax Code",
        comodel_name="l10n_id.faktur_pajak_allowed_dpp_tax_code",
        inverse_name="transaction_type_id",
    )
    allowed_ppn_tax_code_ids = fields.One2many(
        string="Allowed PPn Tax Code",
        comodel_name="l10n_id.faktur_pajak_allowed_ppn_tax_code",
        inverse_name="transaction_type_id",
    )
    allowed_ppnbm_tax_code_ids = fields.One2many(
        string="Allowed PPnBm Tax Code",
        comodel_name="l10n_id.faktur_pajak_allowed_ppnbm_tax_code",
        inverse_name="transaction_type_id",
    )
    description = fields.Text(
        string="Description",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )


class FakturPajakAllowedDppTaxCode(models.Model):
    _name = "l10n_id.faktur_pajak_allowed_dpp_tax_code"
    _description = "Faktur Pajak Allowed DPP Tax Code"

    type_id = fields.Many2one(
        string="Faktur Pajak Type",
        comodel_name="l10n_id.faktur_pajak_type",
        required=True,
        ondelete="restrict",
    )

    transaction_type_id = fields.Many2one(
        string="Faktur Pajak Transaction Type",
        comodel_name="l10n_id.faktur_pajak_transaction_type",
        required=True,
        ondelete="restrict",
    )

    tax_code_ids = fields.Many2many(
        string="DPP Tax Codes",
        comodel_name="account.tax.code",
        relation="rel_fp_allowed_dpp_tax_code",
        column1="allow_id",
        column2="tax_code_id",
    )


class FakturPajakAllowedPpnTaxCode(models.Model):
    _name = "l10n_id.faktur_pajak_allowed_ppn_tax_code"
    _description = "Faktur Pajak Allowed PPn Tax Code"

    type_id = fields.Many2one(
        string="Faktur Pajak Type",
        comodel_name="l10n_id.faktur_pajak_type",
        required=True,
        ondelete="restrict",
    )

    transaction_type_id = fields.Many2one(
        string="Faktur Pajak Transaction Type",
        comodel_name="l10n_id.faktur_pajak_transaction_type",
        required=True,
        ondelete="restrict",
    )

    tax_code_ids = fields.Many2many(
        string="PPn Tax Codes",
        comodel_name="account.tax.code",
        relation="rel_fp_allowed_ppn_tax_code",
        column1="allow_id",
        column2="tax_code_id",
    )


class FakturPajakAllowedPpnbmTaxCode(models.Model):
    _name = "l10n_id.faktur_pajak_allowed_ppnbm_tax_code"
    _description = "Faktur Pajak Allowed PPnBm Tax Code"

    type_id = fields.Many2one(
        string="Faktur Pajak Type",
        comodel_name="l10n_id.faktur_pajak_type",
        required=True,
        ondelete="restrict",
    )

    transaction_type_id = fields.Many2one(
        string="Faktur Pajak Transaction Type",
        comodel_name="l10n_id.faktur_pajak_transaction_type",
        required=True,
        ondelete="restrict",
    )

    tax_code_ids = fields.Many2many(
        string="PPnBm Tax Codes",
        comodel_name="account.tax.code",
        relation="rel_fp_allowed_ppnbm_tax_code",
        column1="allow_id",
        column2="tax_code_id",
    )
