# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class DjbcKiteMovementType(models.Model):
    _name = "l10n_id.djbc_kite_movement_type"
    _description = "DJBC KITE Movement Type"

    name = fields.Char(
        string="Name",
        required=True,
    )
    code = fields.Char(
        string="Code",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
