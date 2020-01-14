# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from unidecode import unidecode

class exped_digital_linea(models.Model):
        _name = 'exped_digital_linea'
        _order = "write_date desc"


class exped_digital(models.Model):
        _name = 'exped_digital'
        _order = "write_date desc"

        def _get_permiso_asignacion(self):
                desired_group_name = self.env['res.groups'].search([('name', '=', 'Asignacion')])
                is_desired_group = self.env.user.id in desired_group_name.users.ids
                if is_desired_group:
                        #print(("EL USUARIO SE ENCUENTRA HABILITADO PARA INSERTAR EXPEDIENTES"))
                        return True
                else:
                        #print(("NOOO EL USUARIO SE ENCUENTRA HABILITADO INSERTAR EXPEDIENTES"))
                        return False

        # recibido = fields.Boolean('Recibido', readonly=True, compute=_is_recept_doc, store=False)
        name = fields.Char('Nombre Exped', readonly=True, store=True)

class expediente(models.Model):
        _name = 'expediente.expediente'
        _inherit = 'expediente.expediente'
        _description = "Agregar Asociacion con Flujos de Tareas"

        # empleado_seg = fields.Many2one('hr.employee', 'Empleado Asignado', readonly=False)
        # empleado_seg = fields.Char('Tenencia de Expte.', readonly=True, store=True)