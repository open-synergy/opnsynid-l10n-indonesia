# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    sim_a_umum_number = fields.Char(
        string="# SIM A Umum",
        compute=lambda s: s._compute_identification(
            "sim_a_umum_number", "sim_A_umum"),
        search=lambda s, *a: s._search_identification(
            "sim_A_umum", *a),
    )
    sim_a_number = fields.Char(
        string="# SIM A",
        compute=lambda s: s._compute_identification(
            "sim_a_number", "sim_A"),
        search=lambda s, *a: s._search_identification(
            "sim_A", *a),
    )
    sim_b1_umum_number = fields.Char(
        string="# SIM B1 Umum",
        compute=lambda s: s._compute_identification(
            "sim_b1_umum_number", "sim_B1_umum"),
        search=lambda s, *a: s._search_identification(
            "sim_B1_umum", *a),
    )
    sim_b1_number = fields.Char(
        string="# SIM B1",
        compute=lambda s: s._compute_identification(
            "sim_b1_number", "sim_B1"),
        search=lambda s, *a: s._search_identification(
            "sim_B1", *a),
    )
    sim_b2_umum_number = fields.Char(
        string="# SIM B2 Umum",
        compute=lambda s: s._compute_identification(
            "sim_b2_umum_number", "sim_B2_umum"),
        search=lambda s, *a: s._search_identification(
            "sim_B2_umum", *a),
    )
    sim_b2_number = fields.Char(
        string="# SIM B2",
        compute=lambda s: s._compute_identification(
            "sim_b2_number", "sim_B2"),
        search=lambda s, *a: s._search_identification(
            "sim_B2", *a),
    )
    sim_c_number = fields.Char(
        string="# SIM C",
        compute=lambda s: s._compute_identification(
            "sim_c_number", "sim_C"),
        search=lambda s, *a: s._search_identification(
            "sim_C", *a),
    )
    sim_d_number = fields.Char(
        string="# SIM D",
        compute=lambda s: s._compute_identification(
            "sim_d_number", "sim_D"),
        search=lambda s, *a: s._search_identification(
            "sim_D", *a),
    )
