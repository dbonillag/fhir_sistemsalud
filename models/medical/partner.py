# * coding: utf8 *

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PartnerFHIR(models.Model):
	_inherit = "res.partner"
	
	_description = "description"

	
	ref = fields.Char(string = "Identificador")
	doctype_id = fields.Many2one("fhir.doctype", string = "Tipo de documento")
	name_1 = fields.Char(string = "Primer nombre")
	name_2 = fields.Char(string = "Segundo nombre")
	lastname_1 = fields.Char(string = "Primer apellido")
	lastname_2 = fields.Char(string = "Segundo apellido")
	gender = fields.Selection([("male", "Masculino"),("female", "Femenino"), ("other", "Otro"), ("unknown", "Desconocido")], string = "Genero")
	is_patient = fields.Boolean(string = "Es paciente")
	is_doctor = fields.Boolean(string = "Es Medico")
	is_insurer =fields.Boolean(string = "Es asegurador")
	id_fhir = fields.Char(string = "Id en el servidor FHIR")

	

