# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp.tools.translate import _
from datetime import datetime


class ReportPeriod(models.Model):
    _name = "l10n_id.djbc_report_period"
    _description = "DJBC Report Period"
    _order = "date_start asc, id"

    name = fields.Char(
        string="Period",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    date_start = fields.Date(
        string="Date Start",
        required=True,
    )
    date_end = fields.Date(
        string="Date End",
        required=True,
    )

    @api.constrains("date_start", "date_end")
    def _check_range(self):
        if self.date_end <= self.date_start:
            strWarning = _("The start date must precede it's end date")
            raise models.ValidationError(strWarning)

    @api.multi
    def _next_period(self, step):
        self.ensure_one()
        criteria = [
            ("date_start", ">", self.date_start)
        ]
        results = self.search(criteria)
        if results:
            return results[step - 1]
        return False

    @api.multi
    def _previous_period(self, step):
        self.ensure_one()
        criteria = [
            ("date_start", "<", self.date_start)
        ]
        results = self.search(criteria, order="date_start desc")
        if results:
            return results[step - 1]
        return False

    @api.model
    def _find_period(self, dt=None):
        if not dt:
            dt = datetime.now().strftime("%Y-%m-%d")
        criteria = [
            ("date_start", "<=", dt),
            ("date_end", ">=", dt),
        ]
        results = self.search(criteria)
        if not results:
            strWarning = _("No DJBC report period configured for %s" % dt)
            raise models.ValidationError(strWarning)
        result = results[0]
        return result
