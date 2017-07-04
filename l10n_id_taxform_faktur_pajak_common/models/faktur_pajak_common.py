# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp import models, fields, api
import openerp.addons.decimal_precision as dp
from datetime import datetime


class FakturPajakCommon(models.AbstractModel):
    _name = "l10n_id.faktur_pajak_common"
    _description = "Faktur Pajak"
    _inherit = ["mail.thread"]

    @api.depends(
        "transaction_type_id",
    )
    @api.multi
    def _compute_jenis_transaksi(self):
        for fp in self:
            fp.enofa_jenis_transaksi = fp.transaction_type_id.code

    @api.depends(
        "transaction_type_id",
    )
    @api.multi
    def _compute_fg_pengganti(self):
        for fp in self:
            fp.enofa_fg_pengganti = fp.fp_state

    @api.depends(
        "name",
    )
    @api.multi
    def _compute_nomor_dokumen(self):
        for fp in self:
            fp.enofa_nomor_dokumen = fp.name

    @api.depends(
        "creditable",
    )
    @api.multi
    def _compute_is_creditable(self):
        for fp in self:
            fp.enofa_is_creditable = fp.creditable

    @api.depends(
        "seller_branch_id",
        "buyer_branch_id",
        "fp_direction",
    )
    @api.multi
    def _compute_nama(self):
        for fp in self:
            fp.enofa_nama = "-"
            if fp.fp_direction == "keluaran":
                self.enofa_nama = fp.buyer_branch_id.name
            elif fp.fp_direction == "masukan":
                self.enofa_nama = fp.seller_branch_id.name

    @api.depends(
        "seller_branch_id",
        "buyer_branch_id",
        "fp_direction",
    )
    @api.multi
    def _compute_alamat_lengkap(self):
        for fp in self:
            fp.enofa_alamat_lengkap = "-"
            if fp.fp_direction == "keluaran":
                self.enofa_alamat_lengkap = fp.buyer_branch_id.enofa_address
            elif fp.fp_direction == "masukan":
                self.enofa_alamat_lengkap = fp.seller_branch_id.enofa_address

    @api.depends(
        "seller_branch_id",
        "buyer_branch_id",
        "fp_direction",
    )
    @api.multi
    def _compute_npwp(self):
        for fp in self:
            fp.enofa_npwp = "000000000000000"
            if fp.fp_direction == "keluaran":
                if fp.seller_branch_id.vat:
                    self.enofa_npwp = fp.buyer_branch_id.npwp
            elif fp.fp_direction == "masukan":
                if fp.buyer_branch_id.vat:
                    self.enofa_npwp = fp.seller_branch_id.npwp

    @api.depends(
        "date",
    )
    @api.multi
    def _compute_tanggal_dokumen(self):
        for fp in self:
            fp.enofa_tanggal_dokumen = "-"
            if fp.date:
                fp.enofa_tanggal_dokumen = datetime.strptime(
                    fp.date, "%Y-%m-%d").strftime(
                        "%d/%m/%Y")

    @api.depends(
        "taxform_period_id",
    )
    @api.multi
    def _compute_masa_pajak(self):
        for fp in self:
            fp.enofa_masa_pajak = fp.taxform_period_id.code

    @api.depends(
        "taxform_year_id",
    )
    @api.multi
    def _compute_tahun_pajak(self):
        for fp in self:
            fp.enofa_tahun_pajak = fp.taxform_year_id.code

    @api.depends(
        "base",
    )
    @api.multi
    def _compute_jumlah_dpp(self):
        for fp in self:
            fp.enofa_jumlah_dpp = int(fp.base_company_currency)

    @api.depends(
        "ppn_amount",
    )
    @api.multi
    def _compute_jumlah_ppn(self):
        for fp in self:
            fp.enofa_jumlah_ppn = int(fp.ppn_amount)

    @api.depends(
        "ppnbm_amount",
    )
    @api.multi
    def _compute_jumlah_ppnbm(self):
        for fp in self:
            fp.enofa_jumlah_ppnbm = int(fp.ppnbm_amount)

    @api.depends(
        "date",
    )
    @api.multi
    def _compute_taxform_period(self):
        for fp in self:
            fp.taxform_period_id = False
            if self.date:
                fp.taxform_period_id = self.env["l10n_id.tax_period"].\
                    _find_period(self.date).id

    @api.depends(
        "taxform_period_id",
    )
    @api.multi
    def _compute_taxform_year(self):
        for fp in self:
            fp.taxform_year_id = False
            if fp.taxform_period_id:
                fp.taxform_year_id = fp.taxform_period_id.year_id.id

    @api.depends(
        "type_id",
    )
    def _compute_transaction_type(self):
        for fp in self:
            fp.allowed_transaction_type_ids = fp.type_id.\
                allowed_transaction_type_ids.ids

    @api.depends(
        "type_id",
        "transaction_type_id",
    )
    def _compute_tax_code(self):
        obj_dpp_code = self.env["l10n_id.faktur_pajak_allowed_dpp_tax_code"]
        obj_ppn_code = self.env["l10n_id.faktur_pajak_allowed_ppn_tax_code"]
        obj_ppnbm_code = self.env[
            "l10n_id.faktur_pajak_allowed_ppnbm_tax_code"]
        for fp in self:
            criteria = [
                ("type_id", "=", fp.type_id.id),
                ("transaction_type_id", "=", fp.transaction_type_id.id),
            ]
            dpp_codes = obj_dpp_code.search(criteria)
            for dpp_code in dpp_codes:
                fp.allowed_dpp_tax_code_ids += dpp_code.tax_code_ids
            ppn_codes = obj_ppn_code.search(criteria)
            for ppn_code in ppn_codes:
                fp.allowed_ppn_tax_code_ids += ppn_code.tax_code_ids
            ppnbm_codes = obj_ppnbm_code.search(criteria)
            for ppnbm_code in ppnbm_codes:
                fp.allowed_ppnbm_tax_code_ids += ppnbm_code.tax_code_ids

    @api.depends(
        "type_id",
    )
    def _compute_additional_flag(self):
        for fp in self:
            fp.allowed_additional_flag_ids = fp.type_id.\
                allowed_additional_flag_ids.ids

    @api.depends(
        "type_id",
    )
    @api.multi
    def _compute_allow_reverse(self):
        for fp in self:
            fp.allow_reverse = fp.type_id.allow_reverse

    @api.depends(
        "type_id",
    )
    @api.multi
    def _compute_allow_multiple_reference(self):
        for fp in self:
            fp.allow_multiple_reference = fp.type_id.allow_multiple_reference

    @api.depends(
        "reverse_id",
    )
    @api.multi
    def _compute_nomor_dokumen_balik(self):
        for fp in self:
            fp.enofa_nomor_dokumen_balik = "-"
            if fp.reverse_id:
                fp.enofa_nomor_dokumen_balik = fp.reverse_id.name

    @api.depends(
        "reverse_id",
    )
    @api.multi
    def _compute_tanggal_dokumen_balik(self):
        for fp in self:
            fp.enofa_tanggal_dokumen_balik = "-"
            if fp.reverse_id:
                fp.enofa_tanggal_dokumen_balik = datetime.strptime(
                    fp.reverse_id.date, "%Y-%m-%d").strftime(
                        "%d/%m/%Y")

    @api.depends(
        "reference_id",
        "reference_ids",
        "allow_multiple_reference",
    )
    @api.multi
    def _compute_all_reference(self):
        for fp in self:
            if fp.type_id.allow_multiple_reference:
                fp.all_reference_ids = fp.reference_ids.ids
            else:
                fp.all_reference_ids = fp.reference_id and \
                    [fp.reference_id.id] or False

    @api.depends(
        "type_id",
    )
    @api.multi
    def _compute_allow_creditable(self):
        for fp in self:
            fp.allow_creditable = fp.type_id.allow_creditable

    @api.depends(
        "type_id",
    )
    @api.multi
    def _compute_allow_substitute(self):
        for fp in self:
            fp.allow_substitute = fp.type_id.allow_substitute

    name = fields.Char(
        string="# Faktur Pajak",
        required=True,
        readonly=True,
        default="/",
        states={
            "draft": [("readonly", False)],
        },
    )

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        readonly=True,
        default=lambda self: self._default_company_id(),
        states={
            "draft": [("readonly", False)],
        },
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        required=True,
        readonly=True,
        states={
            "draft": [("readonly", False)]},
    )

    @api.model
    def _default_company_currency(self):
        return self.env.user.company_id.currency_id.id

    company_currency_id = fields.Many2one(
        string="Company Currency",
        comodel_name="res.currency",
        required=True,
        readonly=True,
        default=lambda self: self._default_company_currency(),
        states={
            "draft": [("readonly", False)]},
    )

    @api.model
    def _default_fp_direction(self):
        fp_type = self._get_faktur_pajak_type()
        if fp_type:
            return fp_type.fp_direction
        else:
            return "keluaran"

    fp_direction = fields.Selection(
        string="Jenis Faktur Pajak",
        selection=[
            ("masukan", "Masukan"),
            ("keluaran", "Keluaran"),
        ],
        required=True,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
        default=lambda self: self._default_fp_direction(),
    )
    transaction_type_id = fields.Many2one(
        string="Transaction Type",
        comodel_name="l10n_id.faktur_pajak_transaction_type",
        required=True,
        readonly=True,
        states={
            "draft": [("readonly", False)]},
    )

    @api.model
    def _get_faktur_pajak_type(self):
        return False

    @api.model
    def _default_faktur_pajak_type(self):
        fp_type = self._get_faktur_pajak_type()
        if fp_type:
            return fp_type.id
        else:
            return False

    type_id = fields.Many2one(
        string="Type",
        comodel_name="l10n_id.faktur_pajak_type",
        required=True,
        default=lambda self: self._default_faktur_pajak_type(),
    )

    @api.model
    def _default_fp_state(self):
        return "0"

    fp_state = fields.Selection(
        string="Normal/Penggantian?",
        selection=[
            ("0", "Normal"),
            ("1", "Penggantian"),
        ],
        required=True,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
        default=lambda self: self._default_fp_state(),
    )

    @api.model
    def _default_seller_partner(self):
        if self._default_fp_direction() == "keluaran":
            return self.env.user.company_id.partner_id.id

    seller_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Seller",
        required=True,
        default=lambda self: self._default_seller_partner(),
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    seller_branch_id = fields.Many2one(
        comodel_name="res.partner",
        string="Seller Branch",
        required=True,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )

    @api.model
    def _default_buyer_partner(self):
        if self._default_fp_direction() == "masukan":
            return self.env.user.company_id.partner_id.id

    buyer_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Buyer",
        required=True,
        default=lambda self: self._default_buyer_partner(),
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    buyer_branch_id = fields.Many2one(
        comodel_name="res.partner",
        string="Buyer Branch",
        required=True,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    base = fields.Float(
        string="Base",
        digits_compute=dp.get_precision("Account"),
        required=True,
        readonly=True,
        states={
            "draft": [("readonly", False)]},
    )
    base_company_currency = fields.Float(
        string="Base in Company Currency",
        digits_compute=dp.get_precision("Account"),
        required=True,
        readonly=True,
        states={
            "draft": [("readonly", False)]},
    )
    ppn_amount = fields.Float(
        string="PPn Amount",
        digits_compute=dp.get_precision("Account"),
        required=True,
        readonly=True,
        states={
            "draft": [("readonly", False)]},
    )
    ppnbm_amount = fields.Float(
        string="PPnBm Amount",
        digits_compute=dp.get_precision("Account"),
        required=True,
        readonly=True,
        states={
            "draft": [("readonly", False)]},
    )
    date = fields.Date(
        string="Document Date",
        required=True,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    taxform_period_id = fields.Many2one(
        string="Masa Pajak",
        comodel_name="l10n_id.tax_period",
        compute="_compute_taxform_period",
        store=True,
    )
    taxform_year_id = fields.Many2one(
        string="Tahun Pajak",
        comodel_name="l10n_id.tax_year",
        compute="_compute_taxform_year",
        store=True,
    )
    note = fields.Text(
        string="Note",
    )
    allow_multiple_reference = fields.Boolean(
        string="Allow Multiple Doc. References",
        compute="_compute_allow_multiple_reference",
        store=False,
    )
    reference_id = fields.Many2one(
        string="Doc. Reference",
        comodel_name="account.move.line",
        readonly=True,
        states={
            "draft": [("readonly", False)]},
    )
    reference_ids = fields.Many2many(
        string="Doc. References",
        comodel_name="account.move.line",
        relation="rel_fp_dummy",
        readonly=True,
        states={
            "draft": [("readonly", False)]},
    )
    all_reference_ids = fields.Many2many(
        string="Doc. References",
        comodel_name="account.move",
        relation="rel_fp_all_dummy",
        compute="_compute_all_reference",
        store=True,
    )
    allowed_transaction_type_ids = fields.Many2many(
        string="Allowed Transaction Type",
        comodel_name="l10n_id.faktur_pajak_transaction_type",
        compute="_compute_transaction_type",
        store=False,
    )
    allowed_dpp_tax_code_ids = fields.Many2many(
        string="Allowed DPP Tax Codes",
        comodel_name="account.tax.code",
        compute="_compute_tax_code",
        store=False,
    )
    allowed_ppn_tax_code_ids = fields.Many2many(
        string="Allowed PPn Tax Codes",
        comodel_name="account.tax.code",
        compute="_compute_tax_code",
        store=False,
    )
    allowed_ppnbm_tax_code_ids = fields.Many2many(
        string="Allowed PPnBm Tax Codes",
        comodel_name="account.tax.code",
        compute="_compute_tax_code",
        store=False,
    )
    allowed_additional_flag_ids = fields.Many2many(
        string="Allowed Additional Flags",
        comodel_name="l10n_id.faktur_pajak_additional_flag",
        compute="_compute_additional_flag",
        store=False,
    )
    additional_flag_id = fields.Many2one(
        string="Additional Flag",
        comodel_name="l10n_id.faktur_pajak_additional_flag",
        readonly=True,
        states={
            "draft": [("readonly", False)]},
    )
    reverse_id = fields.Many2one(
        string="Reverse From",
        comodel_name="l10n_id.faktur_pajak_common",
        readonly=True,
        states={
            "draft": [("readonly", False)]},
    )
    allow_reverse = fields.Boolean(
        string="Allow to Reverse Document",
        compute="_compute_allow_reverse",
        store=False,
    )
    substitute_id = fields.Many2one(
        string="Substitute For",
        comodel_name="l10n_id.faktur_pajak_common",
        readonly=True,
        states={
            "draft": [("readonly", False)]},
    )
    allow_substitute = fields.Boolean(
        string="Allow to Substitute Document",
        compute="_compute_allow_substitute",
        store=False,
    )
    allow_creditable = fields.Boolean(
        string="Allow to Creditable",
        compute="_compute_allow_creditable",
        store=False,
    )

    @api.model
    def _default_creditable(self):
        return "0"

    creditable = fields.Selection(
        string="Bisa Dikreditkan?",
        selection=[
            ("0", "Tidak Dikreditkan"),
            ("1", "Dikreditkan"),
        ],
        required=True,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
        default=lambda self: self._default_creditable(),
    )
    state = fields.Selection(
        string="State",
        required=True,
        readonly=True,
        default="draft",
        track_visibility="onchange",
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Waiting for Approval"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
    )
    # E-NOFA FIELDS
    enofa_jenis_transaksi = fields.Char(
        string="KD_JENIS_TRANSAKSI",
        compute="_compute_jenis_transaksi",
        store=False,
    )
    enofa_fg_pengganti = fields.Char(
        string="FG_PENGGANTI",
        compute="_compute_fg_pengganti",
        store=False,
    )
    enofa_nomor_dokumen = fields.Char(
        string="NOMOR_DOKUMEN",
        compute="_compute_nomor_dokumen",
        store=False,
    )
    enofa_masa_pajak = fields.Char(
        string="MASA_PAJAK",
        compute="_compute_masa_pajak",
        store=False,
    )
    enofa_tahun_pajak = fields.Char(
        string="TAHUN_PAJAK",
        compute="_compute_tahun_pajak",
        store=False,
    )
    enofa_tanggal_dokumen = fields.Char(
        string="TANGGAL_DOKUMEN",
        compute="_compute_tanggal_dokumen",
        store=False,
    )
    enofa_npwp = fields.Char(
        string="NPWP",
        compute="_compute_npwp",
        store=False,
    )
    enofa_nama = fields.Char(
        string="NAMA",
        compute="_compute_nama",
        store=False,
    )
    enofa_alamat_lengkap = fields.Char(
        string="ALAMAT_LENGKAP",
        compute="_compute_alamat_lengkap",
        store=False,
    )
    enofa_jumlah_dpp = fields.Char(
        string="JUMLAH_DPP",
        compute="_compute_jumlah_dpp",
        store=False,
    )
    enofa_jumlah_ppn = fields.Char(
        string="JUMLAH_PPN",
        compute="_compute_jumlah_ppn",
        store=False,
    )
    enofa_jumlah_ppnbm = fields.Char(
        string="JUMLAH_DPP",
        compute="_compute_jumlah_ppnbm",
        store=False,
    )
    enofa_is_creditable = fields.Char(
        string="IS_CREDITABLE",
        compute="_compute_is_creditable",
        store=False,
    )
    enofa_nomor_dokumen_balik = fields.Char(
        string="-",
        compute="_compute_nomor_dokumen_balik",
        store=False,
    )
    enofa_tanggal_dokumen_balik = fields.Char(
        string="-",
        compute="_compute_tanggal_dokumen_balik",
        store=False,
    )

    @api.multi
    def workflow_action_confirm(self):
        for fp in self:
            fp.write(
                fp._prepare_confirm_data())

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        return {
            "state": "confirmed",
        }

    @api.multi
    def workflow_action_done(self):
        for fp in self:
            fp.write(
                fp._prepare_done_data())

    @api.multi
    def _prepare_done_data(self):
        self.ensure_one()
        return {
            "state": "done",
        }

    @api.multi
    def workflow_action_cancel(self):
        for fp in self:
            fp.write(
                fp._prepare_cancel_data())

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        return {
            "state": "cancelled",
        }

    @api.multi
    def workflow_action_reset(self):
        for fp in self:
            fp.write(
                fp._prepare_reset_data())

    @api.multi
    def _prepare_reset_data(self):
        self.ensure_one()
        return {
            "state": "draft",
        }

    @api.onchange("seller_partner_id")
    def onchange_seller(self):
        if self.seller_partner_id:
            partner = self.seller_partner_id.commercial_partner_id
            if self.seller_branch_id:
                branch = self.seller_branch_id.commercial_partner_id
                if partner != branch:
                    self.seller_branch_id = False
            else:
                self.seller_branch_id = self.seller_partner_id
        else:
            self.seller_branch_id = False

    @api.onchange(
        "reference_ids",
        "reference_id",
    )
    def onchange_all_reference(self):
        obj_line = self.env["account.move.line"]
        if self.fp_direction == "masukan":
            partner_id = self.seller_partner_id and \
                self.seller_partner_id.id or 0
        else:
            partner_id = self.buyer_partner_id and \
                self.buyer_partner_id.id or 0
        criteria = [
            ("move_id", "in", self.all_reference_ids.ids),
            ("tax_code_id", "in", self.allowed_dpp_tax_code_ids.ids),
            ("partner_id", "=", partner_id),
        ]
        for line in obj_line.search(criteria):
            if line.currency_id:
                self.base += abs(line.amount_currency)
            else:
                self.base += abs(line.tax_amount)
            self.base_company_currency += abs(line.tax_amount)
        criteria = [
            ("move_id", "in", self.all_reference_ids.ids),
            ("tax_code_id", "in", self.allowed_ppn_tax_code_ids.ids),
            ("partner_id", "=", partner_id),
        ]
        for line in obj_line.search(criteria):
            self.ppn_amount += abs(line.tax_amount)
        criteria = [
            ("move_id", "in", self.all_reference_ids.ids),
            ("tax_code_id", "in", self.allowed_ppnbm_tax_code_ids.ids),
            ("partner_id", "=", partner_id),
        ]
        for line in obj_line.search(criteria):
            self.ppnbm_amount += abs(line.tax_amount)

    @api.onchange("buyer_partner_id")
    def onchange_buyer(self):
        if self.buyer_partner_id:
            partner = self.buyer_partner_id.commercial_partner_id
            if self.buyer_branch_id:
                branch = self.buyer_branch_id.commercial_partner_id
                if partner != branch:
                    self.buyer_branch_id = False
            else:
                self.buyer_branch_id = self.buyer_partner_id
        else:
            self.buyer_branch_id = False

    @api.onchange("company_id")
    def onchange_company_id(self):
        self.currency_id = False

        if self.company_id:
            self.currency_id = self.company_id.currency_id.id
