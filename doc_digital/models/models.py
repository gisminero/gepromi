# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from unidecode import unidecode

class doc_digital_archivo(models.Model):
        _name = 'doc_digital.archivo'
        _order = "id desc"

        name = fields.Char('Nombre', required=True)
        archivo = fields.Binary('Archivo', required=False)
        doc_digital_id = fields.Many2one('hr.employee', string='Doc. Digital')
        state = fields.Selection([('draft', 'Borrador'), ('active', 'Activo'), ],
                                 string='Estado', required=True, default="draft",
                                 help="Determina el estado del expediente")

class doc_digital(models.Model):
        _name = 'doc_digital'
        _order = "write_date desc"

        name = fields.Char('Nombre', readonly=False, required=False)
        descrip = fields.Char('Descripcion', required=False)
        expediente_id = fields.Many2one('expediente.expediente', 'Id Expediente', required=True)
        archivos_id = fields.One2many('doc_digital.archivo', 'doc_digital_id', string='Archivos Asociados')

        def _get_permiso_asignacion(self):
                desired_group_name = self.env['res.groups'].search([('name', '=', 'Asignacion')])
                is_desired_group = self.env.user.id in desired_group_name.users.ids
                if is_desired_group:
                        #print(("EL USUARIO SE ENCUENTRA HABILITADO PARA INSERTAR EXPEDIENTES"))
                        return True
                else:
                        #print(("NOOO EL USUARIO SE ENCUENTRA HABILITADO INSERTAR EXPEDIENTES"))
                        return False


class expediente(models.Model):
        _name = 'expediente.expediente'
        _inherit = 'expediente.expediente'
        _description = "Agregar Asociacion con Flujos de Tareas"

        # empleado_seg = fields.Many2one('hr.employee', 'Empleado Asignado', readonly=False)
        # empleado_seg = fields.Char('Tenencia de Expte.', readonly=True, store=True)

        def administrar_digitales(self):
                active_id = self.env.context.get('id_activo')
                # print (("ENVIANDO .... " + str(active_id)))
                user_id = self.env.user.id
                # print (())
                expte_obj = self.browse([active_id])
                # tiene_flujo_asociado = self.tiene_flujo(expte_obj.procedimiento_id.id)
                depart_actual_id = expte_obj.ubicacion_actual
                if not depart_actual_id:
                        print(("No hay oficina actual asignada."))
                # CONSULTANDO PLANTILLAS PARA OFICINA Y TAREA ACTUAL
                if expte_obj.tarea_actual:
                        doc_digital_obj_cant = self.env['doc_digital'].search_count(
                                [('expediente_id', '=', expte_obj.id)])
                        doc_digital_obj = self.env['doc_digital'].search(
                                [('expediente_id', '=', expte_obj.id)])
                else:
                        doc_digital_obj_cant = self.env['doc_digital'].search_count(
                                [('expediente_id', '=', expte_obj.id)])
                        doc_digital_obj = self.env['doc_digital'].search(
                                [('expediente_id', '=', expte_obj.id)])
                if doc_digital_obj_cant > 0:
                        # NUEVO PASE A OFICINA
                        return {
                                'name': "Documentos Digitales Asociados al Expediente",
                                'view_mode': 'form',
                                'res_id': doc_digital_obj[0].id,
                                # 'view_id': self.env.ref('pase.form_enviar').id,
                                'res_model': 'doc_digital',
                                'type': 'ir.actions.act_window',
                                # 'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
                                #'domain': [('id', 'in', ids_plantillas)],
                                #'context': {'recibido': False, 'oficina_destino': False, 'observ_pase': ''},
                                'views': [[self.env.ref('doc_digital.form').id, "form"]],
                                'target': 'new',
                        }
                return True