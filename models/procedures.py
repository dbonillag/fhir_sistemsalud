# * coding: utf8 *

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Procedures(models.Model):
    _name = "fhir.procedures"
    _description = "description"

    cr_id = fields.Many2one("fhir.clinical_record", string = 'Registro clinico')
    activity_id = fields.Many2one("product.product", string = 'Actividad') 
    quantity = fields.Float(string = 'Cantidad')
    notes = fields.Text(string = 'Notas')