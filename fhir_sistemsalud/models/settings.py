# -*- coding: utf-8 -*-


import logging

from odoo import fields, models, api

_logger = logging.getLogger(__name__)

ir_config_parameter = 'ir.config_parameter'


class FHIRServerSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    fhir_server_url = fields.Char(string='URL del servidor FHIR')
    fhir_access_token = fields.Text(string='Token de acceso')

    def set_values(self):
        res = super(FHIRServerSettings, self).set_values()
        self.env[ir_config_parameter].sudo().set_param(
            'fhir.fhir_server_url', self.fhir_server_url)
        self.env[ir_config_parameter].sudo().set_param(
            'fhir.fhir_access_token', self.fhir_access_token)
        return res

    @api.model
    def get_values(self):
        res = super(FHIRServerSettings, self).get_values()
        icp_sudo = self.env[ir_config_parameter].sudo()
        fhir_server_url = icp_sudo.get_param('fhir.fhir_server_url')
        fhir_access_token = icp_sudo.get_param('fhir.fhir_access_token')
        res.update(
            fhir_server_url=fhir_server_url,
            fhir_access_token=fhir_access_token
        )
        return res
