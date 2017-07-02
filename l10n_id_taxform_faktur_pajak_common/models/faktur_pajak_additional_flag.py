# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class FakturPajakAditionalFlag(models.Model):
    _name = "l10n_id.faktur_pajak_additional_flag"
    _description = "Faktur Pajak Additional Flag"

    code = fields.Char(
        string="Code",
        required=True,
    )
    name = fields.Char(
        string="Transaction Type",
        required=True,
    )
    description = fields.Text(
        string="Description",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
