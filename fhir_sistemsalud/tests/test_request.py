# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2020 Daniel Bonilla
#    @author Daniel Bonilla Guevara <dbonillag_1@uqvirtual.edu.co>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.tests.common import TransactionCase
from openerp.exceptions import AccessError

import logging
_logger = logging.getLogger(__name__)


class TestRequest(TransactionCase):

    def setUp(self):
        super(TestRequest, self).setUp()
        self.model = self.env['fhir.service_request']
        self.user_model = self.env['res.users']
        self.main_company = self.env.ref('base.main_company')
        partner_manager = self.env.ref('base.group_partner_manager')
        self.group_admin = self.env.ref(
            'fhir_sistemsalud.group_fhir_administrator')
        self.group_nurse = self.env.ref('fhir_sistemsalud.group_fhir_nurse')
        self.group_doctor = self.env.ref('fhir_sistemsalud.group_fhir_doctor')

        # No enviar confirmacion para el reinicio de clave
        contex = {'no_reset_password': True}

        self.admin_user = self.user_model.with_context(contex).create(dict(
            name="Administrador",
            company_id=self.main_company.id,
            login="admin_test",
            email="admin@fhir.co",
            color=1,
            function='Friend',
            date='2020-11-10',
            groups_id=[(6, 0, [self.group_admin.id, partner_manager.id])]
        ))
        self.nurse_user = self.user_model.with_context(contex).create(dict(
            name="Enfermera",
            company_id=self.main_company.id,
            login="nurse_test",
            email="nurse@fhir.co",
            date='2020-11-10',
            groups_id=[(6, 0, [self.group_nurse.id, partner_manager.id])]
        ))
        self.doctor_user = self.user_model.with_context(contex).create(dict(
            name="Medico",
            company_id=self.main_company.id,
            login="doctor_test",
            email="test@fhir.co",
            date='2020-11-10',
            groups_id=[(6, 0, [self.group_doctor.id, partner_manager.id])]
        ))

        self.request = self.model.create(
            {
                'code': 'test_000',
                'state': 'draft'
            }
        )

    def test_crear(self):

        # Validar que una solicitud de servicio se
        # pueda crear con el usuario enfermera
        usr = self.nurse_user.id
        self.request1 = self.model.sudo(usr).create(
            {
                'code': 'test_001',
                'state': 'draft'
            }
        )

        # No permitir crear solicitudes de
        # servicio de parte de un administrador
        with self.assertRaises(AccessError):
            usr = self.admin_user.id
            self.request2 = self.model.sudo(usr).create(
                {
                    'code': 'test_002',
                    'state': 'draft'
                }
            )

        # No permitir crear solicitudes de servicio de parte de un doctor
        with self.assertRaises(AccessError):
            usr = self.doctor_user.id
            self.request3 = self.model.sudo(usr).create(
                {
                    'code': 'test_003',
                    'state': 'draft'
                }
            )

    def test_modificar(self):
        state = 'open'

        usr = self.nurse_user.id
        self.request.sudo(usr).write({'state': state})
        self.assertEqual(self.request.state, state)

        # No permite al administrador modificar solicitudes de servicio
        with self.assertRaises(AccessError):
            usr = self.admin_user.id
            self.request.sudo(usr).write({'state': state})

        # No permite al doctro modificar solicitudes de servicio
        with self.assertRaises(AccessError):
            usr = self.doctor_user.id
            self.request.sudo(usr).write({'state': state})

    def test_consultar(self):

        usr = self.nurse_user.id
        request_ids = self.model.sudo(usr).search([])
        self.assertNotEqual(len(request_ids), 0)

        usr = self.admin_user.id
        request_ids = self.model.sudo(usr).search([])
        self.assertNotEqual(len(request_ids), 0)

        usr = self.doctor_user.id
        request_ids = self.model.sudo(usr).search([])
        self.assertNotEqual(len(request_ids), 0)

    def test_eliminar(self):

        usr = self.nurse_user.id
        with self.assertRaises(AccessError):
            self.request.sudo(usr).unlink()

        with self.assertRaises(AccessError):
            usr = self.admin_user.id
            self.request.sudo(usr).unlink()

        with self.assertRaises(AccessError):
            usr = self.doctor_user.id
            self.request.sudo(usr).unlink()
