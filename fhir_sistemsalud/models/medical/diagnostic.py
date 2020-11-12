# * coding: utf8 *

from odoo import fields, models


class Diagnostic(models.Model):
    _name = "fhir.diagnostic"
    _description = "description"
    _rec_name = 'name'

    internal_code = fields.Char(string='Codigo interno')
    name = fields.Char(string='Nombre')
    cie10_code = fields.Char(string='Codigo cie10')
