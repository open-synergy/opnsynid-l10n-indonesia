# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, _


class ResPartnerIdNumber(models.Model):
    _inherit = 'res.partner.id_number'

    _sql_constraints = [
        ("name_unique",
         "unique(category_id,name)",
         _("No duplicate ID Number"),
         ),
    ]
