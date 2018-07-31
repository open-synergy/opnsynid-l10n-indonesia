# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class BuktiPotongPPhF113312In(models.Model):
    _name = "l10n_id.bukti_potong_pph_f113312_in"
    _inherit = "l10n_id.bukti_potong_pph"
    _table = "l10n_id_bukti_potong_pph"
    _description = "Bukti Potong PPh f.1.1.33.12 In"

    @api.model
    def _default_type_id(self):
        return self.env.ref(
            "l10n_id_taxform_bukti_potong_pph_f113312."
            "bukti_potong_pph_type_f113312_in").id

    type_id = fields.Many2one(
        default=lambda self: self._default_type_id(),
    )

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        type_id = self.env.ref(
            "l10n_id_taxform_bukti_potong_pph_f113312."
            "bukti_potong_pph_type_f113312_in")
        args.append(("type_id", "=", type_id.id))
        return super(BuktiPotongPPhF113312In, self).search(
            args=args, offset=offset, limit=limit,
            order=order, count=count)
