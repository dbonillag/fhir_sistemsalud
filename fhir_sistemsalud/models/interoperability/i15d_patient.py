# -*- coding: utf-8 -*-

import json
import logging

import requests
from openerp import models, api
from openerp.exceptions import ValidationError

_logger = logging.getLogger(__name__)

ENDPOINT = "/Patient"


class I15dPatient(models.Model):
    # clase encargada de servir de intermediario entre el modelo de datos del paciente del sistema y el paciente del
    # servidor FHIR
    _name = 'fhir.i15d.patient'

    _inherit = 'fhir.i15d.base'

    @api.model
    def post_patient(self, patient):

        headers = self.get_headers()
        patient_dict = self.build_patient(patient)

        url = self.get_url() + ENDPOINT

        patient_json = json.dumps(patient_dict)

        _logger.info(patient_json)

        response = requests.request("POST", url, headers=headers, data=patient_json)

        _logger.info(response.text.encode('utf8'))

        if str(response.status_code)[:1] != '2':
            raise ValidationError(
                u"Ocurrió un error al enviar el paciente por interoperabilidad: %s" % response.text.encode('utf8'))

        response_dict = json.loads(response.text.encode('utf8'))

        return response_dict['id']

    def build_patient(self, patient):
        dict_base = {}
        dict_base['id'] = str(patient.id)
        dict_base['resourceType'] = "Patient"
        dict_base['identifier'] = self.build_identifier_list(patient)
        dict_base['active'] = True
        dict_base['name'] = self.build_name_list(patient)
        dict_base['gender'] = patient.gender
        return dict_base

    def build_identifier_list(self, patient):
        # construye la sección respectiva al identificador natural del registro clinico
        dict_id = {}
        dict_id['use'] = 'official'
        dict_id['value'] = patient.ref

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

    def test_post_patient(self):

        json_m = '''
        {
           "resourceType":"Patient",
           "active":true,
           "name":[
              {
                 "use":"official",
                 "family":"qqq",
                 "given":[
                    "james",
                    "kirk"
                 ]
              },
              {
                 "use":"usual",
                 "given":[
                    "jim"
                 ]
              }
           ],
           "gender":"male",
           "birthDate":"2000-12-25"
        }
        '''

        url = "https://sistemsalud-fhir.azurehealthcareapis.com/Patient"

        # credentials = self.authenticate_client_key()
        headers = {
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6ImtnMkxZczJUMENUaklmajRydDZKSXluZW4zOCIsImtpZCI6ImtnMkxZczJUMENUaklmajRydDZKSXluZW4zOCJ9.eyJhdWQiOiJodHRwczovL3Npc3RlbXNhbHVkLWZoaXIuYXp1cmVoZWFsdGhjYXJlYXBpcy5jb20iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC81OWUwN2I3OC04YWJkLTRmMGMtYWI5MC1mOGJkZDJiMmQ1MzAvIiwiaWF0IjoxNjAzNjQ3NjU5LCJuYmYiOjE2MDM2NDc2NTksImV4cCI6MTYwMzY1MTU1OSwiYWNyIjoiMSIsImFpbyI6IkFXUUFtLzhSQUFBQWt2VklDcXEyU2VsQ1lUcGw4YVhER2J0SldXNFZEWHM0TU5JL0dUNU5sMGVMTmpnZGpKcFVEK2hFMVhHVVlUbVkvNllxQzRORjhTRlkwdG1uUFZKd3J6dHF3SkdYN2U4akZlU0dvaHJkeSs0aFkxWUlFREhISGxMd09uWVFPQU5FIiwiYWx0c2VjaWQiOiIxOmxpdmUuY29tOjAwMDMwMDAwMjZEMUZBNTgiLCJhbXIiOlsicHdkIiwibWZhIl0sImFwcGlkIjoiMDRiMDc3OTUtOGRkYi00NjFhLWJiZWUtMDJmOWUxYmY3YjQ2IiwiYXBwaWRhY3IiOiIwIiwiZW1haWwiOiJkYW5pdmFyYTIwMDhAb3V0bG9vay5lcyIsImZhbWlseV9uYW1lIjoiQm9uaWxsYSIsImdpdmVuX25hbWUiOiJEYW5pZWwiLCJpZHAiOiJsaXZlLmNvbSIsImlwYWRkciI6IjE5MS44OS4xNDIuODgiLCJuYW1lIjoiRGFuaWVsIEJvbmlsbGEiLCJvaWQiOiJjYWQ3ZjUyOS0yMWIwLTQ4N2MtOTZkMS04NDgxMzI1Njc0YWYiLCJwdWlkIjoiMTAwMzIwMDBFQTIxREFGOCIsInJoIjoiMC5BQUFBZUh2Z1diMktERS1ya1BpOTByTFZNSlYzc0FUYmpScEd1LTRDLWVHX2UwWjFBT1EuIiwic2NwIjoidXNlcl9pbXBlcnNvbmF0aW9uIiwic3ViIjoiU0dmNFY2NHBrdE13NlZkUlpod2k5RzNTSW5zcTR0bFNoeW5iVHY0YmFLQSIsInRpZCI6IjU5ZTA3Yjc4LThhYmQtNGYwYy1hYjkwLWY4YmRkMmIyZDUzMCIsInVuaXF1ZV9uYW1lIjoibGl2ZS5jb20jZGFuaXZhcmEyMDA4QG91dGxvb2suZXMiLCJ1dGkiOiJyY0pJSG1QeURFU051ZTFfclhWeUFBIiwidmVyIjoiMS4wIn0.YVYpJAVpaBHwzO82Tj27HRlJR5pAeruHP3dY7dvSeyYo0BaQBF6ZlpGrZmWG5L3AQBoyu2MYwy5HB4appe-xhcpsCQNxSzfljvzXNBkr1WO84d86CjzkgG1rgj3p5bLXpW8K84NUF0Mn9Cm_X5baNFliPgQbSA1KlLqgIxHcPECu2jftUn9OJ5HmxfRhS0Hv2jyy5sVULRWx0uMTwWQ8tSuHuo-Ml5LluhdqI-pEoS1wObKecXrnUNI48lLCWaJLPLQWTCy_Ov5MScbbuYfBcfJxItcNiADeg-agKa6mj4MQOX8inVcLGQ5ZdpqWx_9Jg2pcKAHPH6wbDFSnSqK7Qw',
            'Content-Type': 'application/json'
        }

        # _logger.info(json.dumps(credentials.token))

        response = requests.request("POST", url, headers=headers, data=json_m)

        _logger.info(response.text.encode('utf8'))

        return

    def get_patient(self, ref):

        headers = self.get_headers()
        url = self.get_url() + ENDPOINT + '?identifier=' + ref
        response = requests.request("GET", url, headers=headers, data={})

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
        # crea un diccionario con los datos necesarios para crear un paciente nuevo en el sistema
        return {
            'ref': patient_dict['identifier'][0]['value'],
            'name_1': patient_dict['name'][0]['given'][0],
            'name_2': patient_dict['name'][0]['given'][1] if len(patient_dict['name'][0]['given']) == 3 else '',
            'lastname_2': patient_dict['name'][0]['given'][2] if len(patient_dict['name'][0]['given']) == 3 else
            patient_dict['name'][0]['given'][1],
            'lastname_1': patient_dict['name'][0]['family'],
            'gender': patient_dict['gender'],
            'is_patient': True,
            'id_fhir': patient_dict['id'],
            'name': patient_dict['name'][0]['text']
        }
