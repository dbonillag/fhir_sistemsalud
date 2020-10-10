# * coding: utf8 *

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Patient(models.Model):
	_inherit = "res.partner"
	_name = "res.partner"
	_description = "description"

	ref = fields.Char("Identificador")
	doctype_id = fields.Many2one("fhir.doctype", string = "Tipo de documento")
	name_1 = fields.Char(string = "Primer nombre")
	name_2 = fields.Char(string = "Segundo nombre")
	lastname_1 = fields.Char(string = "Primer apellido")
	lastname_2 = fields.Char(string = "Segundo apellido")
	gender = fields.Selection([("male", "Masculino"),("female", "Femenino"), ("other", "Otro"), ("unknown", "Desconocido")], string = "Genero")
	clinical_record_as_patient_ids = fields.One2many("fhir.clinical_record",  inverse_name = "patient_id", string = "Registros clinicos")
	clinical_record_as_doctor_ids = fields.One2many("fhir.clinical_record",  inverse_name = "doctor_id", string = "Consultas")
	

