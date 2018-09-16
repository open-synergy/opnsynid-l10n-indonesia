# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ResConfig(models.TransientModel):
    _inherit = "accountant.config_setting"

    jasa_audit_umum_ids = fields.Many2many(
        string="Jasa Audit Umum",
        comodel_name="accountant.service",
        related="company_id.jasa_audit_umum_ids",
        store=True,
    )

    jasa_non_audit_umum_ids = fields.Many2many(
        string="Jasa Non-Audit Umum",
        comodel_name="accountant.service",
        related="company_id.jasa_non_audit_umum_ids",
        store=True,
    )
