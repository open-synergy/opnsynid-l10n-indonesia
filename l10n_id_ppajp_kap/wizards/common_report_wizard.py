# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class PpajpCommonReportWizard(models.AbstractModel):
    _name = "l10n_id.ppajp_common_report_wizard"
    _description = "PPAJP Common Report Wizard"

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.user.company_id.id,
    )
    year_id = fields.Many2one(
        string="Year",
        comodel_name="date.range",
        required=True,
    )
    output_format = fields.Selection(
        string="Output Format",
        required=True,
        selection=[("screen", "On-Screen"), ("ods", "ODS"), ("xls", "XLS")],
        default="screen",
    )

    @api.multi
    def action_print_sreen(self):
        raise UserError(_("This feature hasn't been implemented yet"))

    @api.multi
    def action_print_ods(self):
        raise UserError(_("This feature hasn't been implemented yet"))

    @api.multi
    def action_print_xls(self):
        raise UserError(_("This feature hasn't been implemented yet"))

    @api.multi
    def action_print(self):
        self.ensure_one()

        if self.output_format == "screen":
            result = self.action_print_sreen()
        elif self.output_format == "ods":
            result = self.action_print_ods()
        elif self.output_format == "xls":
            result = self.action_print_xls()
        else:
            raise UserError(_("No Output Format Selected"))

        return result
