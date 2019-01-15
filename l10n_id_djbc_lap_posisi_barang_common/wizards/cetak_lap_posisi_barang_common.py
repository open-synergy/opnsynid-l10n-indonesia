# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models, fields
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError


class CetakLapPosisiBarangCommon(models.AbstractModel):
    _name = "l10n_id.cetak_lap_posisi_barang_common"
    _description = "Abstract Model for Cetak Lap. Posisi Barang"

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.user.company_id.id,
    )
    date_start = fields.Datetime(
        string="Date Start",
        required=True,
    )
    date_end = fields.Datetime(
        string="Date End",
        required=True,
    )
    output_format = fields.Selection(
        string="Output Format",
        required=True,
        selection=[
            ("ods", "ODS"),
            ("xls", "XLS")
        ],
        default="ods",
    )

    @api.multi
    def action_print_ods(self):
        raise UserError(
            _("This feature hasn't been implemented yet"))

    @api.multi
    def action_print_xls(self):
        raise UserError(
            _("This feature hasn't been implemented yet"))

    @api.multi
    def action_print(self):
        self.ensure_one()

        if self.output_format == "ods":
            result = self.action_print_ods()
        elif self.output_format == "xls":
            result = self.action_print_xls()
        else:
            raise UserError(_("No Output Format Selected"))

        return result
