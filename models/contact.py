# * coding: utf8 *

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Contact(models.Model):
	_name = "fhir.contact"
	_description = "description"

	code =  fields.Char(string = "Codigo")
	partner_id = fields.Many2one(string = "Contacto", comodel_name = "res.partner")
	relationship = fields.Selection([("C", "Contacto de emergencia"),("E", "Empleador"), ("F", "Entidad gubernamental"), ("I", "Aseguradora"), ("N", "Pariente cercano"), ("S", "Entidad estatal"), ("U", "Desconocido")], string = "Relación con el paciente")
	request_id = fields.Many2one(string = "Solicitud de servicio", comodel_name = "fhir.service_request", inverse_name = 'contact_ids')