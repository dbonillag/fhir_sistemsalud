# -*- coding: utf-8 -*-

import json
import logging

import requests
from openerp import fields, models, api
from openerp.exceptions import ValidationError

_logger = logging.getLogger(__name__)

ENDPOINT = '/Encounter'


class I15dEncounter(models.Model):
    _name = 'fhir.i15d.encounter'

    _inherit = 'fhir.i15d.base'

    _rec_name = 'atention_date'

    id_server = fields.Char(string="Id en el servidor FHIR", readonly=True)

    atention_date = fields.Datetime(string=u"Fecha de atención", readonly=True)
    text = fields.Text(string='Texto', readonly=True)
    diagnoses_ids = fields.One2many("fhir.i15d.condition", string='Diagnosticos', inverse_name='encuonter_id',
                                    readonly=True)
    procedures_ids = fields.One2many("fhir.i15d.procedure", string="Procedimientos", inverse_name='encuonter_id',
                                     readonly=True)
    cr_id = fields.Many2one("fhir.clinical_record", string="Historias en la red", inverse_name='i15d_encounter_ids',
                            readonly=True)

    @api.model
    def post_encounter(self, clinical_record):

        headers = self.get_headers()
        encounter_dict = self.build_encounter(clinical_record)

        url = self.get_url() + ENDPOINT

        encounter_json = json.dumps(encounter_dict)

        _logger.info(encounter_json)

        response = requests.request("POST", url, headers=headers, data=encounter_json)

        _logger.info(response.text.encode('utf8'))

        if str(response.status_code)[:1] != '2':
            raise ValidationError("Ocurrió un error al enviar la historia clinica por interoperabilidad")

        response_dict = json.loads(response.text.encode('utf8'))

        return response_dict['id']

    def build_encounter(self, clinical_record):
        diagnosis_result = self.build_diagnosis_list(clinical_record)
        dict_base = {'id': str(clinical_record.id), 'resourceType': "Encounter",
                     'text': self.build_text(clinical_record),
                     'identifier': self.build_identifier_list(clinical_record),
                     'period': self.build_period(clinical_record), 'subject': self.build_subject(clinical_record),
                     'contained': diagnosis_result['contained'], 'diagnosis': diagnosis_result['diagnosis'],
                     'status': "finished", 'class': self.build_class(clinical_record)}

        return dict_base

    def build_text(self, clinical_record):
        dict_text = {'status': 'additional',
                     'div': "<div xmlns=\"http://www.w3.org/1999/xhtml\">MOTIVO DE CONSULTA: %s \n ENFERMEDAD ACTUAL: %s </div>" % (
                         clinical_record.reason, clinical_record.actual_disease)}

        return dict_text

    def build_identifier_list(self, clinical_record):
        # construye la sección respectiva al identificador natural del registro clinico
        dict_id = {'use': 'official', 'value': clinical_record.code}

        return [dict_id]

    def build_period(self, clinical_record):
        # Contruye el periodo durante el cual se realizó el encuentro
        dict_json = {'start': self.format_datetime(clinical_record.atention_date),
                     'end': self.format_datetime(clinical_record.service_id.discharge_date)}
        return dict_json

    def format_datetime(self, dat):
        # formatea la fecha
        return dat.strftime("%Y-%m-%d")

    def build_subject(self, clinical_record):
        # referencia de paciente al que pertenece el registro clinico
        dict_json = {}
        url = self.get_url() + '/Patient/' + (clinical_record.patient_id.id_fhir or 'na')
        dict_json['reference'] = url
        dict_json['type'] = 'Patient'
        dict_json['display'] = '%s (%s)' % (clinical_record.patient_id.name, clinical_record.patient_id.ref)
        return dict_json

    def build_diagnosis_list(self, clinical_record):
        # Lista de diagnosticos
        list_diagnosis_content = []
        list_diagnosis_references = []
        i15d_condition_model = self.env['fhir.i15d.condition']
        i15d_procedure_model = self.env['fhir.i15d.procedure']

        for i, diagnostic in enumerate(clinical_record.diagnoses_ids, start=1):
            dict_contained_condition = i15d_condition_model.build_condition(diagnostic, )
            dict_contained_condition['id'] = 'condition-' + str(i)
            dict_reference_condition = {
                "condition": {'reference': '#' + dict_contained_condition['id']}
            }
            list_diagnosis_content.append(dict_contained_condition)
            list_diagnosis_references.append(dict_reference_condition)

        for j, procedure in enumerate(clinical_record.procedures_ids, start=1):
            dict_contained_procedure = i15d_procedure_model.build_procedure(procedure)
            dict_contained_procedure['id'] = 'procedure-' + str(j)
            dict_reference_procedure = {
                "condition": {'reference': '#' + dict_contained_procedure['id']}
            }
            list_diagnosis_content.append(dict_contained_procedure)
            list_diagnosis_references.append(dict_reference_procedure)

        return {
            'contained': list_diagnosis_content,
            'diagnosis': list_diagnosis_references
        }

    def build_class(self, clinical_record):

        return {
            "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
            "code": "AMB",
            "display": "ambulatory"
        }

    def get_encounter_by_patient(self, patient):

        headers = self.get_headers()
        url = self.get_url() + ENDPOINT + '?subject=Patient/' + patient.id_fhir
        response = requests.request("GET", url, headers=headers, data={})

        if str(response.status_code)[:1] != '2':
            _logger.info(response.text.encode('utf8'))
            raise ValidationError("Ocurrió un error al enviar la historia clinica por interoperabilidad")

        response_dict = json.loads(response.text.encode('utf8'))

        entry = response_dict.get('entry', False)
        if entry:
            _logger.info(entry)
            return self.create_encounter_list(entry)
        return False

    def create_encounter_list(self, encounters):

        i15d_encounter_list = []

        for encounter in encounters:
            i15d_encounter = self.create_encounter(encounter['resource'])
            i15d_encounter_list.append((0, 0, i15d_encounter))
        return i15d_encounter_list

    def create_encounter(self, encounter):
        new_encounter = {'atention_date': encounter['period']['start'], 'text': encounter['text']['div']}
        diagnosis = [dx for dx in encounter['contained'] if dx['resourceType'] == 'Condition']
        procedure = [dx for dx in encounter['contained'] if dx['resourceType'] == 'Procedure']
        # diagnosis_ids = [dx.id for dx in self.env['fhir.i15d.condition'].create_condition_list()]

        # procedure_ids = [dx.id for dx in self.env['fhir.i15d.procedure'].create_procedure_list()]
        new_encounter['diagnoses_ids'] = self.env['fhir.i15d.condition'].create_condition_list(diagnosis)
        new_encounter['procedures_ids'] = self.env['fhir.i15d.procedure'].create_procedure_list(procedure)
        return new_encounter
