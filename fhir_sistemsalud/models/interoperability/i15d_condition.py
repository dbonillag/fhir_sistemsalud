# -*- coding: utf-8 -*-
import logging

from openerp import fields, models, api

_logger = logging.getLogger(__name__)

ENDPOINT = 'Condition'


class I15dCondition(models.Model):
    _name = 'fhir.i15d.condition'

    _inherit = 'fhir.i15d.base'

    _rec_name = 'diagnostic'

    text = fields.Text(string='Texto', readonly=True)
    diagnostic_type = fields.Char(string='Tipo', readonly=True)
    diagnostic = fields.Char(string='Nombre diagnostico', readonly=True)
    diagnostic_code = fields.Char(string='Codigo CIE10', readonly=True)
    encuonter_id = fields.Many2one("fhir.i15d.encounter", inverse_name='diagnoses_ids', string="encuentro")

    @api.model
    def build_condition(self, diagnostic):
        # devuelve un diccionario con la condicion(diagnostico) construida de tal forma para que sea dependiente del encuentro
        dict_json = {

            'resourceType': 'Condition',

            'text': self.build_text(diagnostic),

            'verificationStatus': self.build_verification_status(diagnostic),

            'code': self.build_code(diagnostic),

            'subject': self.build_subject(diagnostic.clinical_record_id)

        }

        return dict_json

    def build_text(self, diagnostic):
        dict_text = {}

        dict_text['status'] = 'additional'
        dict_text['div'] = "<div xmlns=\"http://www.w3.org/1999/xhtml\">PRIORIDAD: %s</div>" % diagnostic.priority.name
        return dict_text

    def build_verification_status(self, diagnostic):
        dict_json = {
            'coding': [{
                'system': 'http://terminology.hl7.org/CodeSystem/condition-ver-status',
                "code": diagnostic.type_id.i15d_code,
                "display": diagnostic.type_id.name

            }]

        }
        return dict_json

    def build_code(self, diagnostic):
        dict_json = {
            'coding': [{
                'system': 'https://icd.who.int/browse10/2010/en',
                "code": diagnostic.diagnostic_id.cie10_code,
                "display": diagnostic.diagnostic_id.name

            }]

        }
        return dict_json

    def build_subject(self, clinical_record):
        # referencia de paciente al que pertenece el registro clinico
        dict_json = {}
        url = self.get_url() + '/Patient/' + (clinical_record.patient_id.id_fhir or 'na')
        dict_json['reference'] = url
        dict_json['type'] = 'Patient'
        dict_json['display'] = '%s (%s)' % (clinical_record.patient_id.name, clinical_record.patient_id.ref)
        return dict_json

    def create_condition_list(self, diagnosis):
        condition_list = []

        for dx in diagnosis:
            res = self.create({
                'text': dx['text']['div'],
                'diagnostic_type': dx['verificationStatus']['coding'][0]['display'],
                'diagnostic': dx['code']['coding'][0]['display'],
                'diagnostic_code': dx['code']['coding'][0]['code']
            })
            condition_list.append(res.id)

        return [(6, 0, condition_list)]
