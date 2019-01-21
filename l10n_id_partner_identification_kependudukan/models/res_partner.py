# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    ektp_number = fields.Char(
        string="# e-KTP",
        compute=lambda s: s._compute_identification(
            "ektp_number", "ektp"),
        search=lambda s, *a: s._search_identification(
            "ektp", *a),
    )
    kartu_keluarga_number = fields.Char(
        string="# Kartu Keluarga",
        compute=lambda s: s._compute_identification(
            "kartu_keluarga_number", "kk"),
        search=lambda s, *a: s._search_identification(
            "kk", *a),
    )
