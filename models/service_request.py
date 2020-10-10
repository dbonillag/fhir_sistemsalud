# * coding: utf8 *

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ServiceRequest(models.Model):
    _name = "fhir.service_request"
    _description = "description"
   
    code = fields.Char(string="Codigo", readonly = True)
    patient_id = fields.Many2one("res.partner", string = 'Paciente')
    organization_id = fields.Many2one("res.partner", string = 'Aseguradora')
    entry_date = fields.Datetime(string = u"Fecha de ingreso")
    discharge_date = fields.Datetime(string = u"Fecha de egreso")
    contact_ids = fields.One2many("fhir.contact", string = "Contactos", inverse_name = 'request_id')

