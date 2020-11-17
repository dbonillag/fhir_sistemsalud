# * coding: utf8 *

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class Priority(models.Model):
    _name = "fhir.priority"
    _description = "fhir.priority"
    _rec_name = 'name'

    internal_code = fields.Char(string='Codigo interno')
    name = fields.Char(string='Nombre')
    i15d_code = fields.Char(string='Codigo i15d')
