# * coding: utf8 *

from odoo import fields, models


class DocType(models.Model):
    _name = "fhir.doctype"
    _rec_name = 'name'
    _description = "fhir.doctype"

    code = fields.Char("Codigo")
    name = fields.Char("Tipo de documento")
