# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class DaftarBuktiPotongPPhType(models.Model):
    _name = "l10n_id.daftar_bukti_potong_pph_type"
    _description = "Type of Daftar Bukti Potong PPh"

    name = fields.Char(
        string="Type",
        required=True,
        translate=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    description = fields.Text(
        string="Description",
        translate=True,
    )
    sequence_id = fields.Many2one(
        string="Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
    allow_confirm_group_ids = fields.Many2many(
        string="Allow to Confirm",
        comodel_name="res.groups",
        relation="rel_daftar_bukpot_pph_type_confirm_group",
        column1="type_id",
        column2="group_id",
    )
    allow_approve_group_ids = fields.Many2many(
        string="Allow to Approve",
        comodel_name="res.groups",
        relation="rel_daftar_bukpot_pph_type_approve_group",
        column1="type_id",
        column2="group_id",
    )
    allow_cancel_group_ids = fields.Many2many(
        string="Allow to Cancel",
        comodel_name="res.groups",
        relation="rel_daftar_bukpot_pph_type_cancel_group",
        column1="type_id",
        column2="group_id",
    )
    allow_reset_group_ids = fields.Many2many(
        string="Allow to Set to Draft",
        comodel_name="res.groups",
        relation="rel_daftar_bukpot_pph_type_reset_group",
        column1="type_id",
        column2="group_id",
    )
