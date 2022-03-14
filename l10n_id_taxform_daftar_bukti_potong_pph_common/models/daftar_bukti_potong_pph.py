# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime

from openerp import SUPERUSER_ID, api, fields, models
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class DaftarBuktiPotongPPh(models.AbstractModel):
    _name = "l10n_id.daftar_bukti_potong_pph"
    _inherit = ["mail.thread"]
    _description = "Daftar Bukti Potong PPh"

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.model
    def _default_type_id(self):
        return False

    @api.model
    def _default_date(self):
        return datetime.now().strftime("%Y-%m-%d")

    @api.multi
    @api.depends(
        "state",
        "type_id.allow_confirm_group_ids",
        "type_id.allow_approve_group_ids",
        "type_id.allow_cancel_group_ids",
        "type_id.allow_reset_group_ids",
    )
    def _compute_policy(self):
        for daftar_bukpot in self:
            if self.env.user.id == SUPERUSER_ID:
                daftar_bukpot.confirm_ok = (
                    daftar_bukpot.approve_ok
                ) = daftar_bukpot.cancel_ok = daftar_bukpot.reset_ok = True
                continue

            daftar_bukpot_type = daftar_bukpot.type_id

            daftar_bukpot.confirm_ok = self._get_button_policy(
                daftar_bukpot_type, "confirm"
            )
            daftar_bukpot.approve_ok = self._get_button_policy(
                daftar_bukpot_type, "approve"
            )
            daftar_bukpot.cancel_ok = self._get_button_policy(
                daftar_bukpot_type, "cancel"
            )
            daftar_bukpot.reset_ok = self._get_button_policy(
                daftar_bukpot_type, "reset"
            )

    name = fields.Char(
        string="# Daftar Bukti Potong",
        required=True,
        default="/",
        copy=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    pemotong_pajak_id = fields.Many2one(
        string="Pemotong Pajak",
        comodel_name="res.partner",
    )
    type_id = fields.Many2one(
        string="Type of Daftar Bukti Potong PPh",
        comodel_name="l10n_id.daftar_bukti_potong_pph_type",
        ondelete="restrict",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date = fields.Date(
        string="Date",
        required=True,
        default=lambda self: self._default_date(),
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.multi
    @api.depends(
        "date",
    )
    def _compute_tax_period(self):
        obj_tax_period = self.env["l10n_id.tax_period"]
        for bukpot in self:
            try:
                bukpot.tax_period_id = obj_tax_period._find_period(bukpot.date)
            except Exception:
                bukpot.tax_period_id = False

    tax_period_id = fields.Many2one(
        string="Tax Period",
        comodel_name="l10n_id.tax_period",
        compute="_compute_tax_period",
        store=True,
    )
    ttd_mode = fields.Selection(
        string="Signature Mode",
        selection=[
            ("normal", "Pemotong Pajak/Pimpinan"),
            ("kuasa", "Kuasa Wajib Pajak"),
        ],
        default="normal",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    ttd_id = fields.Many2one(
        string="TTD",
        comodel_name="res.partner",
        required=True,
        readonly=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
        required=True,
        readonly=True,
    )
    confirm_ok = fields.Boolean(
        string="Confirm Ok",
        compute="_compute_policy",
        readonly=True,
    )
    approve_ok = fields.Boolean(
        string="Approve Ok",
        compute="_compute_policy",
        readonly=True,
    )
    cancel_ok = fields.Boolean(
        string="Cancel Ok",
        compute="_compute_policy",
        readonly=True,
    )
    reset_ok = fields.Boolean(
        string="Confirm Ok",
        compute="_compute_policy",
        readonly=True,
    )

    @api.multi
    def workflow_action_draft(self):
        for bukpot in self:
            bukpot.write(self._prepare_draft_data())

    @api.multi
    def workflow_action_confirm(self):
        for bukpot in self:
            bukpot.write(self._prepare_confirm_data())

    @api.multi
    def workflow_action_done(self):
        for bukpot in self:
            bukpot.write(self._prepare_done_data())

    @api.multi
    def workflow_action_cancel(self):
        for bukpot in self:
            bukpot.write(self._prepare_cancel_data())

    @api.multi
    def workflow_action_reset(self):
        for bukpot in self:
            bukpot.write(self._prepare_reset_data())

    @api.multi
    def _prepare_draft_data(self):
        self.ensure_one()
        data = {
            "state": "draft",
        }
        return data

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        data = {
            "state": "confirm",
        }
        return data

    @api.multi
    def _prepare_done_data(self):
        self.ensure_one()
        data = {
            "state": "done",
        }
        return data

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        data = {
            "state": "cancel",
        }
        return data

    @api.multi
    def _prepare_reset_data(self):
        self.ensure_one()
        data = {
            "state": "draft",
        }
        return data

    @api.model
    def _get_button_policy(self, daftar_bukpot_type, button_type):
        result = False
        user = self.env.user
        group_ids = user.groups_id.ids

        if button_type == "confirm":
            button_group_ids = daftar_bukpot_type.allow_confirm_group_ids.ids
        elif button_type == "approve":
            button_group_ids = daftar_bukpot_type.allow_approve_group_ids.ids
        elif button_type == "cancel":
            button_group_ids = daftar_bukpot_type.allow_cancel_group_ids.ids
        elif button_type == "reset":
            button_group_ids = daftar_bukpot_type.allow_reset_group_ids.ids

        if not button_group_ids:
            result = True
        else:
            if set(button_group_ids) & set(group_ids):
                result = True
        return result

    @api.model
    def _create_sequence(self, type_id):
        daftar_bukpot_type = self.env["l10n_id.daftar_bukti_potong_pph_type"].browse(
            type_id
        )
        if not daftar_bukpot_type.sequence_id:
            raise UserError(_("No sequence defined"))
        name = (
            self.env["ir.sequence"].next_by_id(daftar_bukpot_type.sequence_id.id) or "/"
        )
        return name

    @api.model
    def create(self, values):
        new_values = self._prepare_create_data(values)
        return super(DaftarBuktiPotongPPh, self).create(new_values)

    @api.model
    def _prepare_create_data(self, values):
        name = values.get("name", False)
        if not name or name == "/":
            values["name"] = self._create_sequence(values["type_id"])
        return values
