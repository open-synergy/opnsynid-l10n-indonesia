# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    jasa_audit_umum_ids = fields.Many2many(
        string="Jasa Audit Umum",
        comodel_name="accountant.service",
        relation="rel_company_2_jasa_audit_umum",
        column1="company_id",
        column2="service_id",
    )

    jasa_non_audit_umum_ids = fields.Many2many(
        string="Jasa Non-Audit Umum",
        comodel_name="accountant.service",
        relation="rel_company_2_jasa_non_audit_umum",
        column1="company_id",
        column2="service_id",
    )
