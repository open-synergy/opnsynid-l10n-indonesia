# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class DocumentType(models.Model):
    _name = "l10n_id.djbc_document_type"
    _description = "Document Type"

    name = fields.Char(
        string="Document Type",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
    )
    description = fields.Text(
        string="Description",
    )
