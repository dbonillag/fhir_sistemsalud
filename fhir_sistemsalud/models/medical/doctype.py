# * coding: utf8 *

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class DocType(models.Model):
    _name = "fhir.doctype"
    _rec_name = 'name'
    _description = "description"

    code = fields.Char("Codigo")
    name = fields.Char("Tipo de documento")