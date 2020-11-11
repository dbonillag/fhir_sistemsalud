# * coding: utf8 *

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class Priority(models.Model):
    _name = "fhir.priority"
    _description = "description"
    _rec_name = 'name'

    internal_code = fields.Char(string = 'Codigo interno')
    name = fields.Char(string = 'Nombre') 
    i15d_code = fields.Char(string = 'Codigo i15d') 