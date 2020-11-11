# * coding: utf8 *
from datetime import datetime, timedelta


from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class ClinicalRecord(models.Model):
    _name = "fhir.clinical_record"
    _description = "description"

    code = fields.Char(string = 'Codigo')
    patient_id = fields.Many2one("res.partner",  string = "Paciente")
    doctor_id = fields.Many2one( "res.partner", string = 'Medico')
    atention_date = fields.Datetime(string = u"Fecha de atención", default = datetime.now() + timedelta(hours = 5))
    reason = fields.Text(string = 'Motivo de consulta')
    actual_disease = fields.Text(string = "Enfermedad actual")
    diagnoses_ids = fields.One2many("fhir.diagnoses", inverse_name = "clinical_record_id", string = 'Diagnosticos')
    procedures_ids = fields.One2many("fhir.procedures", string = "Procedimientos", inverse_name = 'cr_id')
    cr_correction_id = fields.Many2one("fhir.clinical_record") 
    state = fields.Selection([('new', 'Nuevo'), ('accepted', 'Aceptado'), ('canceled', 'Anulado')], string = 'Estado', default = 'new')
    service_id = fields.Many2one('fhir.service_request', string = "Solicitud de servicio")

    # id del registro en el servidor FHIR
    id_fhir = fields.Char(string = "Id en el servidor FHIR")

    #lista de registros clinicos del mismo paciente obtenidos por interoperabilidad
    i15d_encounter_ids = fields.One2many("fhir.i15d.encounter", string = "Historia clinica en la red", inverse_name = 'cr_id')


    @api.multi
    def close_encounter(self):
        self.service_id.write({
            'discharge_date' : datetime.today(),
            'state' : 'close'
        })


        self.write({
            'code' : self.env['ir.sequence'].next_by_code('fhir.clinical_record'),
            'state' : 'accepted'
        })

        
        self.write({ 'id_fhir' : self.env['fhir.i15d.encounter'].post_encounter(self) })

    @api.multi
    def search_network(self):

        for encounter_id in self.i15d_encounter_ids:
            self.write({'i15d_encounter_ids' : [(2, encounter_id.id)]})
        # obtiene los registros por interoperabilidad
        i15d_encounter_ids = self.env['fhir.i15d.encounter'].get_encounter_by_patient(self.patient_id)
        _logger.info(u'%s'%i15d_encounter_ids)
        if i15d_encounter_ids:
            self.write({'i15d_encounter_ids' : i15d_encounter_ids})


 