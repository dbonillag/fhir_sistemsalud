# * coding: utf8 *

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class PartnerFHIR(models.Model):
	# contacto puede ser paciente, medico u organización
	_inherit = "res.partner"
	
	_description = "description"

	_rec_name = 'name'

	
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
	name = fields.Char(string = "Nombre", required = False)

	

	@api.model
	def create(self, vals):
		
		res = super(PartnerFHIR, self).create(vals)
		if not res.name:
				raise ValidationError('Ingrese el nombre completo')

		if res.is_patient:
			if not res.name_1:
				raise ValidationError('Ingrese el primer nombre')
			if not res.lastname_1:
				raise ValidationError('Ingrese el primer apellido')
			if not res.gender:
				raise ValidationError('Ingrese el genero')
			res.id_fhir = self.env['fhir.i15d.patient'].post_patient(res)
		return res

	@api.multi
	def search_network(self):
		# busca el paciente en la red, si existe,lo crea automaticamente
		
		ref = self.ref
		
		patient_dict = self.env['fhir.i15d.patient'].get_patient(ref)
		if patient_dict:
			# patient_dict['doctype_id'] = self.doctype_id.id
			res = self.create(patient_dict)
			view_id = self.env.ref('fhir_sistemsalud.view_partner_form_fe')
			return {
				'type': 'ir.actions.act_window',
				'res_model': 'res.partner',
				'view_id': view_id.id,
				'view_mode': 'form',
				'res_id': res.id
			} 


		return False

