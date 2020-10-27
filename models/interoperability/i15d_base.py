# -*- coding: utf-8 -*-
from openerp import fields, models, api

import logging
_logger = logging.getLogger(__name__)


class I15dBase(models.Model):
	_name = 'fhir.i15d.base'


	def get_url(self):
		ICPSudo = self.env['ir.config_parameter'].sudo()
		token = ICPSudo.get_param('fhir.server_url')
		return token


	def get_headers(self):
		ICPSudo = self.env['ir.config_parameter'].sudo()
		token = ICPSudo.get_param('fhir.access_token')
		return {
			'Authorization': 'Bearer '+token,
			'Content-Type': 'application/json'
		}