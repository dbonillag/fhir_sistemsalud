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
    name = fields.Char(string="Nombre",
                       required=False)

    @api.model
    def create(self, vals):
        context = self._context

        if vals.get('name', '') == '' and not vals.get('is_company', False):
            if not vals.get('name_1', '') == '':
                raise ValidationError('Ingrese el primer nombre')
            if not vals.get('lastname_1', '') == '':
                raise ValidationError('Ingrese el primer apellido')
            vals['name'] = vals.get('name_1', '') + vals.get('name_2', '') \
                + vals.get('lastname_1', '') + vals.get('lastname_2', '')
            if vals.get('is_patient', False):
                if not vals.get('gender', False):
                    raise ValidationError('Ingrese el genero')
                res = super(PartnerFHIR, self).create(vals)
                if not context.get('no_interoperate', False):
                    res.id_fhir = self.env['fhir.i15d.patient'].post_patient(res)
                return res
        else:
            res = super(PartnerFHIR, self).create(vals)
            return res

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
