# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from openerp import api, models, fields
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError


class DateRangeSelector(models.TransientModel):
    _name = "l10n_id.date_range_selector"
    _description = "Date Range Selector"

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.user.company_id.id,
    )
    date_start = fields.Datetime(
        string="Date Start",
        required=True,
        default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    date_end = fields.Datetime(
        string="Date End",
        required=True,
        default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    warehouse_ids = fields.Many2many(
        string="Warehouse",
        comodel_name="stock.warehouse",
        relation="rel_djbc_date_range_2_warehouse",
        column1="wizard_id",
        column2="warehouse_id",
        required=True,
    )
    output_format = fields.Selection(
        string='Output Format',
        required=True,
        selection=[
            ('screen', 'On-Screen'),
            ('xls', 'XLS'),
            ('ods', 'ODS')
        ],
        default='ods',
    )

    @api.constrains(
        "date_start", "date_end")
    def _check_date(self):
        strWarning = _(
            "Date start must be greater than date end")
        if self.date_start and self.date_end:
            if self.date_start > self.date_end:
                raise UserError(strWarning)

    @api.multi
    def action_print(self):
        self.ensure_one()

        datas = {}
        output_format = ''

        datas['form'] = self.read()[0]

        if self.output_format == 'xls':
            output_format = 'stock_card_xls'
        elif self.output_format == 'ods':
            output_format = 'stock_card_ods'

        return {
            'type': 'ir.actions.report.xml',
            'report_name': output_format,
            'datas': datas,
        }
