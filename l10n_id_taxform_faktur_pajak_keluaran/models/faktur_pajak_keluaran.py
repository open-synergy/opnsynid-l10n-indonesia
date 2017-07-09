# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp import models, fields, api
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class FakturPajakKeluaran(models.Model):
    _name = "l10n_id.faktur_pajak_keluaran"
    _description = "Faktur Pajak Keluaran"
    _inherit = ["l10n_id.faktur_pajak_common"]

    @api.model
    def _get_faktur_pajak_type(self):
        return self.env.ref(
            "l10n_id_taxform_faktur_pajak_keluaran.fp_type_fp_keluaran")

    @api.depends(
        "all_reference_ids",
    )
    @api.multi
    def _compute_allowed_invoice_ids(self):
        result_line = self.env["account.invoice.line"]
        for fp in self:
            for inv in fp.all_reference_ids:
                result_line += inv.invoice_line
            fp.allowed_invoice_line_ids = result_line

    @api.depends(
        "additional_flag_id",
    )
    @api.multi
    def _compute_keterangan_tambahan(self):
        for fp in self:
            fp.enofa_id_keterangan_tambahan = fp.additional_flag_id and \
                fp.additional_flag_id.id or "-"

    @api.depends(
        "fp_payment",
    )
    def _compute_fg_uang_muka(self):
        for fp in self:
            fp.enofa_fg_uang_muka = fp.fp_payment

    @api.depends(
        "note",
    )
    def _compute_referensi(self):
        for fp in self:
            fp.enofa_referensei = fp.note

    @api.depends(
        "faktur_pajak_line_ids",
        "faktur_pajak_line_ids.subtotal_company_currency",
        "faktur_pajak_line_ids.ppn_amount",
        "faktur_pajak_line_ids.ppnbm_amount",
        "advance_payment_fp_ids",
        "advance_move_line_ids",
        "advance_move_line_ids.debit",
        "advance_move_line_ids.credit",
        "advance_ppn_move_line_ids",
        "advance_ppn_move_line_ids.debit",
        "advance_ppn_move_line_ids.credit",
        "advance_ppnbm_move_line_ids",
        "advance_ppnbm_move_line_ids.debit",
        "advance_ppnbm_move_line_ids.credit",
    )
    @api.multi
    def _compute_tax(self):
        for fp in self:
            dpp = ppn = ppnbm = um_dpp = um_ppn = um_ppnbm = 0.0
            for line in fp.faktur_pajak_line_ids:
                dpp += line.subtotal_company_currency
                ppnbm = line.ppnbm_amount
            ppn = int(0.1 * dpp)
            ppnbm = int(ppnbm)
            if fp.fp_payment == "0":
                um_dpp = um_ppn = um_ppnbm = 0
            elif fp.fp_payment == "1":
                for advance in fp.advance_move_line_ids:
                    um_dpp += abs(advance.debit - advance.credit)
                um_dpp = int(um_dpp)
                for advance_ppn in fp.advance_ppn_move_line_ids:
                    um_ppn += abs(advance_ppn.debit - advance_ppn.credit)
                for advance_ppnbm in fp.advance_ppnbm_move_line_ids:
                    um_ppnbm += abs(advance_ppnbm.debit - advance_ppnbm.credit)
            elif fp.fp_payment == "2":
                for advance in fp.advance_payment_fp_ids:
                    um_dpp += int(advance.enofa_uang_muka_dpp)
                    um_ppn += int(advance.enofa_uang_muka_ppn)
                    um_ppnbm += int(advance.enofa_uang_muka_ppnbm)
            fp.enofa_jumlah_dpp = dpp
            fp.enofa_jumlah_ppn = ppn
            fp.enofa_jumlah_ppnbm = ppnbm
            fp.enofa_uang_muka_dpp = um_dpp
            fp.enofa_uang_muka_ppn = um_ppn
            fp.enofa_uang_muka_ppnbm = um_ppnbm

    @api.depends(
        "nomor_seri_id",
        "seller_branch_id",
        "fp_state",
        "transaction_type_id",
        "transaction_type_id.code",
        "taxform_year_id",
    )
    @api.multi
    def _compute_nomor_dokumen(self):
        for fp in self:
            fp.enofa_nomor_dokumen = "%s%s%s%s%s" % (
                fp.transaction_type_id.code,
                fp.fp_state,
                fp.seller_branch_id.ref,
                fp.taxform_year_id and fp.taxform_year_id.code or "-",
                fp.nomor_seri_id.name,
            )

    @api.model
    def _default_fp_payment(self):
        return "0"

    fp_payment = fields.Selection(
        string="Normal/Uang Muka/Pelunasan?",
        selection=[
            ("0", "Normal"),
            ("1", "Uang Muka"),
            ("2", "Pelunasan"),
        ],
        required=True,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
        default=lambda self: self._default_fp_payment(),
    )
    nomor_seri_id = fields.Many2one(
        string="Nomor Seri FP",
        comodel_name="l10n_id.nomor_seri_faktur_pajak",
        required=False,
        readonly=True,
        states={
            "draft": [("readonly", False)]},
    )
    faktur_pajak_line_ids = fields.One2many(
        comodel_name="l10n_id.faktur_pajak_line",
        inverse_name="faktur_pajak_id",
        string="Faktur Pajak Line",
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    advance_payment_fp_ids = fields.Many2many(
        string="Advance Payment FK",
        comodel_name="l10n_id.faktur_pajak_keluaran",
        relation="rel_fk_2_dp_fk",
        column1="fk_id",
        column2="advance_fk_id",
    )
    reference_id = fields.Many2one(
        string="Doc. Reference",
        comodel_name="account.invoice",
    )
    reference_ids = fields.Many2many(
        string="Doc. References",
        comodel_name="account.invoice",
        relation="rel_fp_keluaran_2_invoice",
        column1="fp_keluaran_id",
        column2="invoice_id",
    )
    all_reference_ids = fields.Many2many(
        string="Doc. References",
        comodel_name="account.invoice",
        relation="rel_fp_keluaran_2_all_invoice",
        compute="_compute_all_reference",
        column1="fp_keluaran_id",
        column2="invoice_id",
        store=True,
    )
    reverse_id = fields.Many2one(
        comodel_name="l10n_id.faktur_pajak_keluaran",
    )
    substitute_id = fields.Many2one(
        comodel_name="l10n_id.faktur_pajak_keluaran",
    )
    allowed_invoice_line_ids = fields.Many2many(
        string="Allowed Invoice Lines",
        comodel_name="account.invoice.line",
        relation="rel_fp_2_allowed_invoice_line",
        column1="faktur_pajak_id",
        column2="line_id",
        readonly=True,
        store=False,
        compute="_compute_allowed_invoice_ids",
    )
    advance_move_line_ids = fields.Many2many(
        string="Advance Payment Move Lines",
        comodel_name="account.move.line",
        relation="rel_fp_2_advance_move_line",
        column1="fp_id",
        column2="line_id",
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    advance_ppn_move_line_ids = fields.Many2many(
        string="Advance Payment PPn Move Lines",
        comodel_name="account.move.line",
        relation="rel_fp_2_advance_ppn_move_line",
        column1="fp_id",
        column2="line_id",
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    advance_ppnbm_move_line_ids = fields.Many2many(
        string="Advance Payment PPnBm Move Lines",
        comodel_name="account.move.line",
        relation="rel_fp_2_advance_ppnbm_move_line",
        column1="fp_id",
        column2="line_id",
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    # Change string of several enofa fields
    enofa_nomor_dokumen = fields.Char(
        string="NOMOR_FAKTUR",
    )
    enofa_tanggal_dokumen = fields.Char(
        string="TANGGAL_FAKTUR",
    )
    enofa_jumlah_ppn = fields.Integer(
        compute="_compute_tax",
        string="JUMLAH_DPP",
    )
    enofa_jumlah_ppnbm = fields.Integer(
        string="JUMLAH_PPNBM",
        compute="_compute_tax",
    )
    enofa_jumlah_dpp = fields.Integer(
        string="JUMLAH_PPN",
        compute="_compute_tax",
    )
    # E-Nova additional fields
    enofa_id_keterangan_tambahan = fields.Char(
        string="ID_KETERANGAN_TAMBAHAN",
        compute="_compute_keterangan_tambahan",
        store=False,
    )
    enofa_fg_uang_muka = fields.Char(
        string="FG_UANG_MUKA",
        compute="_compute_fg_uang_muka",
        store=False,
    )
    enofa_uang_muka_dpp = fields.Integer(
        string="UANG_MUKA_DPP",
        compute="_compute_tax",
        store=False,
    )
    enofa_uang_muka_ppn = fields.Integer(
        string="UANG_MUKA_PPN",
        compute="_compute_tax",
        store=False,
    )
    enofa_uang_muka_ppnbm = fields.Integer(
        string="UANG_MUKA_PPNBM",
        compute="_compute_tax",
        store=False,
    )
    enofa_referensi = fields.Char(
        string="REFERENSI",
        compute="_compute_referensi",
        store=False,
    )

    def onchange_all_reference(self):
        return True

    @api.constrains(
        "nomor_seri_id",
        "state",
    )
    def _check_nomor_seri(self):
        if self.state == "confirmed" and \
                not self.nomor_seri_id:
            strWarning = _("Please select nomor seri FK")
            raise UserError(strWarning)

    @api.multi
    def workflow_action_confirm(self):
        super(FakturPajakKeluaran, self).workflow_action_confirm()
        for fp in self:
            fp.nomor_seri_id.mark_used(fp)

    @api.multi
    def workflow_action_cancel(self):
        super(FakturPajakKeluaran, self).workflow_action_cancel()
        for fp in self:
            fp.nomor_seri_id.mark_unused()
            fp.nomor_seri_id = False
            fp.name = "/"

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        result = super(FakturPajakKeluaran, self)._prepare_confirm_data()
        name = "%s%s.%s-%s.%s" % (
            self.transaction_type_id.code,
            self.fp_state,
            self.seller_branch_id.ref,
            self.taxform_year_id and self.taxform_year_id.code or "-",
            self.nomor_seri_id.name,
        )
        result["name"] = name
        return result

    @api.multi
    def button_load_invoice_line(self):
        self.ensure_one()
        criteria = [
            ("faktur_pajak_id", "=", self.id),
            ]
        self.env["l10n_id.faktur_pajak_line"].search(
            criteria).unlink()
        line_data = []
        allowed_ppn_ids = self.allowed_ppn_tax_code_ids.ids
        allowed_ppnbm_ids = self.allowed_ppnbm_tax_code_ids.ids

        for inv in self.all_reference_ids:
            for line in inv.invoice_line:
                ppn_tax = False
                ppnbm_tax = False
                for tax in line.invoice_line_tax_id:
                    if not tax.tax_code_id or ppn_tax:
                        continue
                    if tax.tax_code_id.id in allowed_ppn_ids:
                        ppn_tax = tax
                    if tax.tax_code_id.id in allowed_ppnbm_ids:
                        ppnbm_tax = tax
                if ppn_tax:
                    line_data.append((0, 0, {
                        "date": inv.date_invoice,
                        "invoice_line_id": line.id,
                        "name": line.product_id.name,
                        "product_id": line.product_id.id,
                        "quantity": line.quantity,
                        "price_unit": line.price_subtotal /
                        line.quantity,
                        "ppn_tax_id": ppn_tax.id,
                        "ppnbm_tax_id": ppnbm_tax and ppnbm_tax.id or False,
                    }))
        self.write({
            "faktur_pajak_line_ids": line_data,
        })


class FakturPajakLine(models.Model):
    _name = "l10n_id.faktur_pajak_line"
    _description = "Faktur Pajak Line"

    @api.depends(
        "quantity",
        "price_unit",
    )
    @api.multi
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.currency_id.round(
                line.price_unit * line.quantity)
            line.subtotal_company_currency = line.currency_id.compute(
                line.subtotal,
                line.company_currency_id,
                round=True,
            )

    @api.depends(
        "product_id",
    )
    @api.multi
    def _compute_kode_objek(self):
        for line in self:
            line.enofa_kode_objek = line.product_id and \
                line.product_id.default_code or "-"

    @api.depends(
        "name",
    )
    @api.multi
    def _compute_nama(self):
        for line in self:
            line.enofa_nama = line.name or "-"

    @api.depends(
        "price_unit",
    )
    @api.multi
    def _compute_harga_satuan(self):
        for line in self:
            line.enofa_harga_satuan = line.price_unit

    @api.depends(
        "quantity",
    )
    @api.multi
    def _compute_jumlah_barang(self):
        for line in self:
            line.enofa_jumlah_barang = line.quantity

    @api.depends(
        "subtotal",
    )
    @api.multi
    def _compute_harga_total(self):
        for line in self:
            line.enofa_harga_total = line.subtotal

    @api.multi
    def _compute_diskon(self):
        for line in self:
            line.enofa_diskon = "0"

    @api.depends(
        "subtotal",
    )
    @api.multi
    def _compute_dpp(self):
        for line in self:
            line.enofa_dpp = line.subtotal

    @api.depends(
        "ppn_amount",
    )
    @api.multi
    def _compute_ppn(self):
        for line in self:
            line.enofa_ppn = line.ppn_amount

    @api.depends(
        "ppnbm_tax_id",
    )
    @api.multi
    def _compute_tarif_ppnbm(self):
        for line in self:
            line.enofa_tarif_ppnbm = 0.0
            if line.ppnbm_tax_id:
                line.enofa_tarif_ppnbm = line.ppnbm_tax_id.amount * 100.00

    @api.depends(
        "ppnbm_amount",
    )
    @api.multi
    def _compute_ppnbm(self):
        for line in self:
            line.enofa_ppnbm = line.ppnbm_amount

    name = fields.Char(
        string="Description",
        required=True,
        size=255,
    )
    date = fields.Date(
        string="Date",
        required=True,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        required=True,
    )
    invoice_line_id = fields.Many2one(
        string="Invoice Line",
        comodel_name="account.invoice.line",
        required=False,
    )

    @api.depends(
        "subtotal_company_currency",
        "ppn_tax_id",
        "ppnbm_tax_id",
    )
    @api.multi
    def _compute_tax(self):
        for line in self:
            line.ppn_amount = line.ppnbm_amount = 0.0
            if line.ppn_tax_id:
                tax = line.ppn_tax_id.compute_all(
                    line.subtotal_company_currency, 1.0)
                line.ppn_amount = tax["total_included"] - tax["total"]
            if line.ppnbm_tax_id:
                tax = line.ppnbm_tax_id.compute_all(
                    line.subtotal_company_currency, 1.0)
                line.ppnbm_amount = tax["total_included"] - tax["total"]

    ppn_tax_id = fields.Many2one(
        string="PPn Tax",
        comodel_name="account.tax",
        required=True,
    )
    ppn_amount = fields.Float(
        string="PPn Amount",
        compute="_compute_tax",
        store=True,
    )
    ppnbm_tax_id = fields.Many2one(
        string="PPnBm Tax",
        comodel_name="account.tax",
    )
    ppnbm_amount = fields.Float(
        string="PPnBm Amount",
        compute="_compute_tax",
        store=True,
    )
    faktur_pajak_id = fields.Many2one(
        comodel_name="l10n_id.faktur_pajak_keluaran",
        string="# Faktur Pajak",
        ondelete="cascade",
    )
    company_currency_id = fields.Many2one(
        string="Company Currency",
        comodel_name="res.currency",
        related="faktur_pajak_id.company_id.currency_id",
        store=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="faktur_pajak_id.currency_id",
        store=True,
    )
    price_unit = fields.Float(
        string="Price Unit",
        required=True,
        default=1.0,
    )
    quantity = fields.Float(
        string="Qty.",
        required=True,
        defaul=1.0,
    )
    subtotal = fields.Float(
        string="Subtotal",
        compute="_compute_subtotal",
        store=True,
    )
    subtotal_company_currency = fields.Float(
        string="Subtotal in Company Currency",
        compute="_compute_subtotal",
        store=True,
    )

    enofa_kode_objek = fields.Char(
        string="KODE_OBJEK",
        compute="_compute_kode_objek",
        store=False,
    )
    enofa_nama = fields.Char(
        string="NAMA",
        compute="_compute_nama",
        store=False,
    )
    enofa_harga_satuan = fields.Char(
        string="HARGA_SATUAN",
        compute="_compute_harga_satuan",
        store=False,
    )
    enofa_jumlah_barang = fields.Char(
        string="JUMLAH_BARANG",
        compute="_compute_jumlah_barang",
        store=False,
    )
    enofa_harga_total = fields.Char(
        string="HARGA_TOTAL",
        compute="_compute_harga_total",
        store=False,
    )
    enofa_diskon = fields.Char(
        string="DISKON",
        compute="_compute_diskon",
        store=False,
    )
    enofa_dpp = fields.Char(
        string="DPP",
        compute="_compute_dpp",
        store=False,
    )
    enofa_ppn = fields.Char(
        string="PPN",
        compute="_compute_ppn",
        store=False,
    )
    enofa_tarif_ppnbm = fields.Char(
        string="TARIF_PPNBM",
        compute="_compute_tarif_ppnbm",
        store=False,
    )
    enofa_ppnbm = fields.Char(
        string="PPNBM",
        compute="_compute_ppnbm",
        store=False,
    )

    @api.onchange(
        "product_id",
        "invoice_line_id",
    )
    def onchange_product(self):
        self.name = False
        self.invoice_line_ids = False
        self.quantity = 0.0
        self.price_unit = 0.0
        result = {}
        allowed_line_ids = self.faktur_pajak_id.allowed_invoice_line_ids.ids
        if self.invoice_line_id:
            self.quantity = self.invoice_line_id.quantity
            self.product_id = self.invoice_line_id.product_id
        if self.product_id:
            self.name = self.product_id.name
            self.price_unit = self.product_id.lst_price
        if self.invoice_line_id and self.product_id:
            self.price_unit = self.invoice_line_id.price_subtotal_gross / \
                self.invoice_line_id.quantity
        result["domain"] = {
            "invoice_line_ids": [
                ("product_id", "=", self.product_id.id),
                ("price_unit", "=", self.price_unit),
                ("id", "in", allowed_line_ids),
            ],
        }
        return result
