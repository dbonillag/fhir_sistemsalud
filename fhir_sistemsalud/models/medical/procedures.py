# * coding: utf8 *

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class Procedures(models.Model):
    _name = "fhir.procedures"
    _description = "fhir.procedures"

    cr_id = fields.Many2one("fhir.clinical_record", string='Registro clinico')
    activity_id = fields.Many2one("product.product", string='Actividad')
    quantity = fields.Float(string='Cantidad')
    notes = fields.Text(string='Notas')
