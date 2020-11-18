# * coding: utf8 *

import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PartnerFHIR(models.Model):
    # contacto puede ser paciente, medico u organización
    _inherit = "res.partner"

    _description = "res.partner"

    _rec_name = 'name'

    name = fields.Char(index=True, required=False)

    ref = fields.Char(string="Identificador")
    doctype_id = fields.Many2one("fhir.doctype",
                                 string="Tipo de documento")
    name_1 = fields.Char(string="Primer nombre")
    name_2 = fields.Char(string="Segundo nombre")
    lastname_1 = fields.Char(string="Primer apellido")
    lastname_2 = fields.Char(string="Segundo apellido")
    gender = fields.Selection([("male", "Masculino"),
                               ("female", "Femenino"),
                               ("other", "Otro"),
                               ("unknown", "Desconocido")],
                              string="Genero")
    is_patient = fields.Boolean(string="Es paciente")
    is_doctor = fields.Boolean(string="Es Medico")
    is_insurer = fields.Boolean(string="Es asegurador")
    id_fhir = fields.Char(string="Id en el servidor FHIR")
    interoperate = fields.Boolean(string='Interoperar', default=True)

    @api.model
    def create(self, vals):

        _logger.info('nombre {}'.format(vals.get('name', False)))

        if vals.get('name', False) is False and vals.get('company_type',
                                                         'person'):
            _logger.info(u'Es persona')
            if not vals.get('name_1'):
                raise ValidationError('Ingrese el primer nombre')
            if not vals.get('lastname_1'):
                raise ValidationError('Ingrese el primer apellido')

            vals['name'] = (vals.get('name_1', '') or '') + " " + \
                           (vals.get('name_2', '') or '') + " " + \
                           (vals.get('lastname_1', '') or '') + " " + \
                           (vals.get('lastname_2', '') or '')
            _logger.info('nombre {}'.format(vals.get('name', False)))
            if vals.get('is_patient'):
                if not vals.get('gender', False):
                    raise ValidationError('Ingrese el genero')
                res = super(PartnerFHIR, self).create(vals)

                if res.interoperate:
                    res.id_fhir = self.env['fhir.i15d.patient'] \
                        .post_patient(res)
                return res
        else:
            _logger.info(u'Es compañia')
            res = super(PartnerFHIR, self).create(vals)
            return res

    @api.multi
    def write(self, vals):
        vals['name'] = self.write_name(vals)
        super(PartnerFHIR, self).write(vals)

    def write_name(self, vals):
        name = (vals.get('name_1') or self.name_1) + " " + \
               (vals.get('name_2') or self.name_2) + " " + \
               (vals.get('lastname_1') or self.lastname_1) + " " + \
               (vals.get('lastname_2') or self.lastname_2)
        return name

    @api.multi
    def search_network(self):
        # busca el paciente en la red,
        # si existe,lo crea automaticamente
        ref = self.ref
        patient_dict = self.env['fhir.i15d.patient'].get_patient(ref)
        if patient_dict:
            # patient_dict['doctype_id'] = self.doctype_id.id
            self.write(patient_dict)
            return
        raise ValidationError(
            'No se encontró el paciente con el documento %s en la red' % ref)
