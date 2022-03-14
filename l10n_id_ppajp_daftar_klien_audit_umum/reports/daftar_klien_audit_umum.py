# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models, tools


class DaftarKlienAuditUmum(models.Model):
    _name = "l10n_id.ppajp_daftar_klien_audit_umum"
    _description = "PPAJP - Daftar Klien Audit Umum"
    _auto = False

    name = fields.Char(
        string="Nomor Laporan Auditor Independen",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
    )
    partner_id = fields.Many2one(
        string="Nama",
        comodel_name="res.partner",
    )
    contact_address = fields.Char(
        string="Alamat",
        related="partner_id.contact_address",
        store=False,
    )
    npwp = fields.Char(
        string="NPWP",
    )
    date = fields.Date(
        string="Tanggal Laporan",
    )
    date_start = fields.Date(string="Awal Tahun Buku")
    date_end = fields.Date(string="Awal Tahun Buku")
    signing_accountant_id = fields.Many2one(
        string="Penandatangan Laporan Auditor Independen (LAI)",
        comodel_name="res.partner",
    )
    report_opinion_id = fields.Many2one(
        string="Opini",
        comodel_name="accountant.report_opinion",
    )
    go_public_description = fields.Char(
        string="Go Publik/Non Go Publik",
    )
    sector_id = fields.Many2one(
        string="Bidang Usaha",
        comodel_name="res.partner.sector",
    )
    total_net_profit = fields.Float(string="Laba/Rugi Bersih")
    total_asset = fields.Float(string="Total Aset")

    def _select(self):
        select_str = """
             SELECT a.id AS id,
                    a.company_id AS company_id,
                    a.name AS name,
                    a.partner_id AS partner_id,
                    CASE
                        WHEN b.vat IS NOT NULL THEN RIGHT(b.vat, -2)
                        ELSE '-'
                    END AS npwp,
                    a.date AS date,
                    a.date_start AS date_start,
                    a.date_end AS date_end,
                    a.signing_accountant_id AS signing_accountant_id,
                    a.report_opinion_id AS report_opinion_id,
                    CASE
                        WHEN b.go_public IS NOT NULL THEN 'Go Publik'
                        ELSE 'Non Go Publik'
                    END AS go_public_description,
                    b.sector_id AS sector_id,
                    a.total_net_profit AS total_net_profit,
                    a.total_asset as total_asset
        """
        return select_str

    def _from(self):
        from_str = """
                accountant_report AS a
        """
        return from_str

    def _where(self):
        where_str = """
            WHERE a.state = 'valid'
        """
        return where_str

    def _join(self):
        join_str = """
        JOIN res_partner AS b
            ON a.partner_id = b.id
        JOIN (
            SELECT  c1.company_id,
                    c1.service_id
            FROM rel_company_2_jasa_audit_umum AS c1
        ) AS c ON   a.service_id = c.service_id AND
                    a.company_id = c.company_id
        """
        return join_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        cr.execute(
            """CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            %s
        )"""
            % (self._table, self._select(), self._from(), self._join(), self._where())
        )
