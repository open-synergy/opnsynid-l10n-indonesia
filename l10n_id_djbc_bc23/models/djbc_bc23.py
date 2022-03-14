# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class DjbcForm23(models.Model):
    _name = "l10n_id.djbc_bc23"
    _description = "Form 2.3 DJBC"
    _inherits = {
        "l10n_id.djbc_custom_document": "custom_document_id",
    }

    custom_document_id = fields.Many2one(
        string="Custom Document",
        comodel_name="l10n_id.djbc_custom_document",
        required=True,
        ondelete="restrict",
    )
