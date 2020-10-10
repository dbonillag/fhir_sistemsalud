# * coding: utf8 *

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class doctype(models.Model):
    _name = "fhir.doctype"
    _rec_name = 'name'
    _description = "description"

    code = fields.Char("Codigo")
    name = fields.Char("Nombre")