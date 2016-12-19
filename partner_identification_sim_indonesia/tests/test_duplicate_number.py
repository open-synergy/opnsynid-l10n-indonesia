# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import openerp.tests.common as common
from psycopg2 import IntegrityError


class TestParterIndentificationSIMIndonesia(common.TransactionCase):

    def test_duplicate(self):
        # Data Object
        obj_res_partner =\
            self.env['res.partner']

        # Data Partner
        partner_1 = obj_res_partner.create(
            {'name': 'Test Partner 1'})
        partner_2 = obj_res_partner.create(
            {'name': 'Test Partner 2'})

        # Data Category
        category =\
            self.env.ref(
                'partner_identification_sim_indonesia.'
                'partner_identification_SIM_A_category'
            )

        # Check
        vals_1 = {
            'name': '5450534001717',
            'category_id': category.id
        }
        partner_1.write({'id_numbers': [(0, 0, vals_1)]})

        vals_2 = {
            'name': '5450534001717',
            'category_id': category.id
        }
        with self.assertRaises(IntegrityError):
            partner_2.write({'id_numbers': [(0, 0, vals_2)]})
