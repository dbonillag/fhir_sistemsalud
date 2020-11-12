# * coding: utf8 *
import logging
from datetime import datetime, timedelta

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ServiceRequest(models.Model):
    _name = "fhir.service_request"
    _description = "description"

    code = fields.Char(string="Codigo")
    patient_id = fields.Many2one("res.partner",
                                 string='Paciente')
    organization_id = fields.Many2one("res.partner",
                                      string='Aseguradora')
    entry_date = fields.Datetime(string=u"Fecha de ingreso",
                                 default=datetime.now() + timedelta(hours=5))
    discharge_date = fields.Datetime(string=u"Fecha de egreso")
    contact_ids = fields.One2many("fhir.contact",
                                  string="Contactos",
                                  inverse_name='request_id')
    state = fields.Selection([('draft', 'Borrador'),
                              ('open', 'Abierto'),
                              ('close', 'Cerrado')],
                             string="Estado",
                             default="draft")

    @api.multi
    def open_service(self):
        self.env['fhir.clinical_record'].sudo().create({
            'patient_id': self.patient_id.id,
            'service_id': self.id
        })

        self.code = self.env['ir.sequence'].next_by_code('fhir.service_request')

        self.write({
            'state': 'open'
        })

        view_id = self.env.ref('fhir_sistemsalud.clinical_record_form_view')
        # return {
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'fhir.clinical_record',
        #     'view_id': view_id.id,
        #     'view_mode': 'form',
        #     'res_id': cr_new.id,
        # }  
        return
