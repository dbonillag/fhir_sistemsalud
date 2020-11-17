# * coding: utf8 *

from odoo import fields, models


class DiagnosticType(models.Model):
    _name = "fhir.diagnostic_type"
    _description = "fhir.diagnostic_type"
    _rec_name = 'name'

    internal_code = fields.Char(string='Codigo interno')
    name = fields.Char(string='Nombre')
    i15d_code = fields.Char(string='Codigo i15d')
