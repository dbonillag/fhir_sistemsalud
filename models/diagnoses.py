# * coding: utf8 *

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Diagnoses(models.Model):
    _name = "fhir.diagnoses"
    _description = "description"

    diagnostic_id = fields.Many2one("fhir.diagnostic") 
    tipo_id = fields.Many2one("fhir.diagnostic_type") 
    priority = fields.Many2one("fhir.priority")
    clinical_record_id = fields.Many2one("fhir.clinical_record",  inverse_name = 'diagnoses_ids')
    
