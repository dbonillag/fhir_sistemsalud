# * coding: utf8 *

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Diagnostic(models.Model):
    _name = "fhir.diagnostic"
    _description = "description"

    internal_code = fields.Char(string = 'Codigo interno')
    name = fields.Char(string = 'Nombre') 
    cie10_code = fields.Char(string = 'Codigo cie10')  