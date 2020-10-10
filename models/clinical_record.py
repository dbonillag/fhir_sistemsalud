# * coding: utf8 *

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ClinicalRecord(models.Model):
    _name = "fhir.clinical_record"
    _description = "description"

    patient_id = fields.Many2one("res.partner",  inverse_name = "clinical_record_as_patient_ids", string = "Paciente")
    doctor_id = fields.Many2one( "res.partner", inverse_name = "clinical_record_as_doctor_ids")
    atention_date = fields.Datetime(string = u"Fecha de atención")
    reason = fields.Text(string = 'Motivo de consulta')
    actual_disease = fields.Text(string = "Enfermedad actual")
    diagnoses_ids = fields.One2many("fhir.diagnoses", inverse_name = "clinical_record_id")
    procedures_ids = fields.Many2many("fhir.procedures", string = "Procedimientos")
    cr_correction_id = fields.Many2one("fhir.clinical_record") 
    state = fields.Selection([('new', 'nuevo'), ('open', 'nuevo'), ('canceled', 'Anulado')], string = 'Estado')
    active = fields.Boolean(string = 'activo')
