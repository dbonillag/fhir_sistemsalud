# * coding: utf8 *

import logging

from openerp import fields, models, api

_logger = logging.getLogger(__name__)

ENDPOINT = 'Procedure'


class I15dProcedure(models.Model):
    _name = 'fhir.i15d.procedure'

    _inherit = 'fhir.i15d.base'

    _rec_name = 'name'

    text = fields.Text(string="texto", readonly=True)

    name = fields.Char(string="Procedimiento", readonly=True)

    code = fields.Char(string="Codigo", readonly=True)

    encuonter_id = fields.Many2one("fhir.i15d.encounter",
                                   inverse_name='procedures_ids',
                                   string="encuentro")

    @api.model
    def build_procedure(self, procedure):
        # devuelve un diccionario con el procedimiento
        # construido de tal forma para que sea dependiente del encuentro
        dict_json = {

            'resourceType': 'Procedure',

            "status": "preparation",

            'text': self.build_text(procedure),

            'code': self.build_code(procedure),

            'subject': self.build_subject(procedure.cr_id)

        }

        return dict_json

    def build_text(self, procedure):
        # sección con las notas del procedimiento
        dict_text = {'status': 'additional',
                     'div': '''<div xmlns=\"http://www.w3.org/1999/xhtml\">
                     NOTAS: %s \n CANTIDAD: %s</div>''' % (
                         procedure.notes, procedure.quantity)}

        return dict_text

    def build_code(self, procedure):
        dict_json = {
            ''
            'coding': [{
                'system': 'https://cpockets.com/cups',
                "code": procedure.activity_id.default_code,
                "display": procedure.activity_id.name

            }]

        }
        return dict_json

    def build_subject(self, clinical_record):
        # referencia de paciente al que pertenece el registro clinico
        dict_json = {}
        patient_id = clinical_record.patient_id
        url = self.get_url() + '/Patient/' + (patient_id.id_fhir or 'na')
        dict_json['reference'] = url
        dict_json['type'] = 'Patient'
        dict_json['display'] = '%s (%s)' % (patient_id.name,
                                            patient_id.ref)
        return dict_json

    def create_procedure_list(self, procedures):
        procedure_list = []

        for procedure in procedures:
            res = self.create({
                'text': procedure['text']['div'],
                'name': procedure['code']['coding'][0]['display'],
                'code': procedure['code']['coding'][0]['code']
            })
            procedure_list.append(res.id)

        return [(6, 0, procedure_list)]
