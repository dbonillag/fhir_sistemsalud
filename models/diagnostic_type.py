# * coding: utf8 *

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class DiagnosticType(models.Model):
    _name = "fhir.diagnostic_type"
    _description = "description"

    internal_code = fields.Char(string = 'Codigo interno')
    name = fields.Char(string = 'Nombre') 
    i15d_code = fields.Char(string = 'Codigo i15d')  