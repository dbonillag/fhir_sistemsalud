# -*- coding: utf-8 -*-

import json
import logging

import requests
from openerp import models, api
from openerp.exceptions import ValidationError

_logger = logging.getLogger(__name__)

ENDPOINT = "/Patient"


class I15dPatient(models.Model):
    # clase encargada de servir de intermediario entre
    # el modelo de datos del paciente del sistema y
    # el paciente del servidor FHIR
    _name = 'fhir.i15d.patient'

    _inherit = 'fhir.i15d.base'

    @api.model
    def post_patient(self, patient):

        headers = self.get_headers()
        patient_dict = self.build_patient(patient)

        url = self.get_url() + ENDPOINT

        patient_json = json.dumps(patient_dict)

        _logger.info(patient_json)

        response = requests.request("POST",
                                    url,
                                    headers=headers,
                                    data=patient_json)

        _logger.info(response.text.encode('utf8'))

        if str(response.status_code)[:1] != '2':
            raise ValidationError(
                u'''Ocurrió un error al enviar el
                paciente por interoperabilidad: %s'''
                % response.text.encode('utf8'))

        response_dict = json.loads(response.text.encode('utf8'))

        return response_dict['id']

    def build_patient(self, patient):
        dict_base = {'id': str(patient.id),
                     'resourceType': "Patient",
                     'identifier': self.build_identifier_list(patient),
                     'active': True,
                     'name': self.build_name_list(patient),
                     'gender': patient.gender}
        return dict_base

    def build_identifier_list(self, patient):
        # construye la sección respectiva
        # al identificador natural del registro clinico
        dict_id = {'use': 'official', 'value': patient.ref}

        return [dict_id]

    def build_name_list(self, patient):

        given = []
        given.append(patient.name_1) if patient.name_1 else ''
        given.append(patient.name_2) if patient.name_2 else ''
        given.append(patient.lastname_2) if patient.lastname_2 else ''

        official_name = {
            "use": 'official',
            'text': patient.name,
            'family': patient.lastname_1,
            'given': given

        }

        return [official_name]

    def get_patient(self, ref):

        headers = self.get_headers()
        url = self.get_url() + ENDPOINT + '?identifier=' + ref
        response = requests.request("GET",
                                    url,
                                    headers=headers,
                                    data={})

        if str(response.status_code)[:1] != '2':
            _logger.info(response.text.encode('utf8'))
            raise ValidationError("Ocurrió un error al obtener el paciente")

        response_dict = json.loads(response.text.encode('utf8'))

        _logger.info(response_dict['entry'])

        entry = response_dict.get('entry', False)
        if entry:
            return self.create_patient(entry[0]['resource'])
        return False

    def create_patient(self, patient_dict):
        # crea un diccionario con los datos necesarios para crear un
        # paciente nuevo en el sistema
        patient_name = patient_dict['name'][0]['given']
        return {
            'ref': patient_dict['identifier'][0]['value'],
            'name_1': patient_name[0],
            'name_2': patient_name[1] if len(patient_name) == 3 else '',
            'lastname_2': patient_name[2] if len(patient_name) == 3 else
            patient_name[1],
            'lastname_1': patient_dict['name'][0]['family'],
            'gender': patient_dict['gender'],
            'is_patient': True,
            'id_fhir': patient_dict['id'],
            'name': patient_dict['name'][0]['text']
        }
