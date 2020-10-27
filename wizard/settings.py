# -*- coding: utf-8 -*-


import requests

from openerp import fields, models, api

import logging
_logger = logging.getLogger(__name__)

class FHIRServerSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	server_url = fields.Char(string='URL del servidor FHIR')
	access_token = fields.Text(string='Token de acceso')

	#resto de configuracion en el video https://www.youtube.com/watch?v=MsVoYPQ4-J4&t=494s



	def set_values(self):
		res = super(FHIRServerSettings, self).set_values()
		self.env['ir.config_parameter'].set_param('fhir.server_url', self.server_url)
		self.env['ir.config_parameter'].set_param('fhir.access_token', self.access_token)
		return res

	@api.model
	def get_values(self):
		res = super(FHIRServerSettings, self).get_values()
		ICPSudo = self.env['ir.config_parameter'].sudo()
		server_url = ICPSudo.get_param('fhir.server_url')
		access_token = ICPSudo.get_param('fhir.access_token')
		res.update(
			server_url = server_url,
			access_token = access_token
		)
		return res