# -*- coding: utf-8 -*-
# Copyright 2017 Andhitia Rama
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.depends(
        "street",
        "state_id",
        "lau1_id",
        "lau2_id",
        "lau3_id",
        "zip",
        "street_number",
    )
    @api.multi
    def _compute_enofa_address(self):
        addrs = "%s Blok %s No. %s RT:%s RW:%s Kel.%s Kec.%s Kota/Kab.%s %s %s"
        for partner in self:
            partner.enofa_address = addrs % (
                partner.street,
                "-",
                partner.street_number or "-",
                "000",
                "000",
                partner.lau3_id and partner.lau3_id.name or "-",
                partner.lau2_id and partner.lau2_id.name or "-",
                partner.lau1_id and partner.lau1_id.name or "-",
                partner.state_id and partner.state_id.name or "-",
                partner.zip or "-",
            )

    enofa_address = fields.Char(
        string="Address for E-Nofa",
        compute="_compute_enofa_address",
        store=False,
    )
