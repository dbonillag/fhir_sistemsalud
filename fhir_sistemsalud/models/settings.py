# -*- coding: utf-8 -*-


import logging

from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class FHIRServerSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    fhir_server_url = fields.Char(string='URL del servidor FHIR')
    fhir_access_token = fields.Text(string='Token de acceso')

    # resto de configuracion en el video https://www.youtube.com/watch?v=MsVoYPQ4-J4&t=494s

    def set_values(self):
        res = super(FHIRServerSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('fhir.fhir_server_url', self.fhir_server_url)
        self.env['ir.config_parameter'].sudo().set_param('fhir.fhir_access_token', self.fhir_access_token)
        return res

    @api.model
    def get_values(self):
        res = super(FHIRServerSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        fhir_server_url = ICPSudo.get_param('fhir.fhir_server_url')
        fhir_access_token = ICPSudo.get_param('fhir.fhir_access_token')
        res.update(
            fhir_server_url=fhir_server_url,
            fhir_access_token=fhir_access_token
        )
        return res
