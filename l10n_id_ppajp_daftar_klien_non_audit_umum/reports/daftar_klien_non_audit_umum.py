# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models, tools


class DaftarKlienNonAuditUmum(models.Model):
    _name = "l10n_id.ppajp_daftar_klien_non_audit_umum"
    _description = "PPAJP - Daftar Klien Non Audit Umum"
    _auto = False

    name = fields.Char(
        string="Nomor Laporan",
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
        string="Penanggung Jawab",
        comodel_name="res.partner",
    )
    service_id = fields.Many2one(
        string="Jenis Jasa Yang Diberikan KAP",
        comodel_name="accountant.service",
    )
    sector_id = fields.Many2one(
        string="Bidang Usaha Klien",
        comodel_name="res.partner.sector",
    )

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
                    a.service_id AS service_id,
                    b.sector_id AS sector_id
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
            FROM rel_company_2_jasa_non_audit_umum AS c1
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
