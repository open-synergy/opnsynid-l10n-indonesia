# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields



class CustomDocument(models.Model):
    _name = "l10n_id.djbc_custom_document"
    _description = "Custom Document"

    name = fields.Char(
        string="# Document",
        required=True,
    )
    date = fields.Date(
        string="Date",
        required=True,
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="l10n_id.djbc_document_type",
        required=True,
        ondelete="restrict",
        )
