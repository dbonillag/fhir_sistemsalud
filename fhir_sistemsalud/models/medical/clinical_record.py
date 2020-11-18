# * coding: utf8 *
import logging
from datetime import datetime, timedelta

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

MODEL = "fhir.clinical_record"
class ClinicalRecord(models.Model):
    _name = MODEL
    _description = MODEL

    code = fields.Char(string='Codigo')
    patient_id = fields.Many2one("res.partner",
                                 string="Paciente")
    doctor_id = fields.Many2one("res.partner",
                                string='Medico')
    atention_date = fields.Datetime(string=u"Fecha de atención",
                                    default=datetime.now() +
                                    timedelta(hours=5))
    reason = fields.Text(string='Motivo de consulta')
    actual_disease = fields.Text(string="Enfermedad actual")
    diagnoses_ids = fields.One2many("fhir.diagnoses",
                                    inverse_name="clinical_record_id",
                                    string='Diagnosticos')
    procedures_ids = fields.One2many("fhir.procedures",
                                     string="Procedimientos",
                                     inverse_name='cr_id')
    cr_correction_id = fields.Many2one(MODEL)
    state = fields.Selection([('new', 'Nuevo'),
                              ('accepted', 'Aceptado'),
                              ('canceled', 'Anulado')],
                             string='Estado',
                             default='new')
    service_id = fields.Many2one('fhir.service_request',
                                 string="Solicitud de servicio")

    # id del registro en el servidor FHIR
    id_fhir = fields.Char(string="Id en el servidor FHIR")

    # lista de registros clinicos del mismo
    # paciente obtenidos por interoperabilidad
    i15d_encounter_ids = fields.One2many("fhir.i15d.encounter",
                                         string="Historia clinica en la red",
                                         inverse_name='cr_id')

    @api.multi
    def close_encounter(self):
        self.service_id.write({
            'discharge_date': datetime.today(),
            'state': 'close'
        })

        self.write({
            'code': self.env['ir.sequence'].
            next_by_code('fhir.clinical_record'),
            'state': 'accepted'
        })

        self.write({'id_fhir': self.env['fhir.i15d.encounter']
                   .post_encounter(self)})

    @api.multi
    def search_network(self):

        for encounter_id in self.i15d_encounter_ids:
            self.write({'i15d_encounter_ids': [(2, encounter_id.id)]})
        # obtiene los registros por interoperabilidad
        i15d_encounter_ids = self.env['fhir.i15d.encounter'] \
            .get_encounter_by_patient(self.patient_id)
        _logger.info(u'%s' % i15d_encounter_ids)
        if i15d_encounter_ids:
            self.write({'i15d_encounter_ids': i15d_encounter_ids})

    @api.multi
    def fix_clinical_record(self):
        _logger.info('inicia el metodo')
        res = self.create(dict(
            code=self.env['ir.sequence'].
            next_by_code('fhir.clinical_record'),
            patient_id=self.patient_id.id,
            doctor_id=self.doctor_id.id,
            atention_date=self.atention_date,
            reason=self.reason,
            actual_disease=self.actual_disease,
            diagnoses_ids=self.copy_diagnoses(),
            procedures_ids=self.copy_procedures(),
            cr_correction_id=self.id,
            state='new',
            service_id=self.service_id.id
        ))
        _logger.info('crea el registro')
        self.state = 'canceled'
        _logger.info('cambia el estado')
        my_view = self.env.ref('fhir_sistemsalud.clinical_record_form_view')
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'fhir.clinical_record',
            'view_id': my_view.id,
            'view_mode': 'form',
            'res_id': res.id,
        }

    @api.multi
    def copy_diagnoses(self):
        _logger.info('entra a diagnosticos')
        diagnoses_ids = [(0, 0, {
            'diagnostic_id': line.diagnostic_id.id,
            'type_id': line.type_id.id,
            'priority': line.priority.id,
        }) for line in self.diagnoses_ids]
        _logger.info('termina diagnosticos')
        return diagnoses_ids

    @api.multi
    def copy_procedures(self):
        _logger.info('entra a procedimientos')
        procedures_ids = [(0, 0, {
            'activity_id': line.activity_id.id,
            'quantity': line.quantity,
            'notes': line.notes,
        }) for line in self.procedures_ids]
        _logger.info('termina procedimientos')
        return procedures_ids
