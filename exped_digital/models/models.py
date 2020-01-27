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

        def administrar_digitales(self):
                active_id = self.env.context.get('id_activo')
                # print (("ENVIANDO .... " + str(active_id)))
                user_id = self.env.user.id
                # print (())
                expte_obj = self.browse([active_id])
                tiene_flujo_asociado = self.tiene_flujo(expte_obj.procedimiento_id.id)
                depart_actual_id = expte_obj.ubicacion_actual
                if not depart_actual_id:
                        print(("No hay oficina actual asignada."))
                # CONSULTANDO PLANTILLAS PARA OFICINA Y TAREA ACTUAL
                if tiene_flujo_asociado and expte_obj.tarea_actual:
                        plant_rel_proced_obj_cant = self.env['plantilla.rel'].search_count(
                                [('tarea_id', '=', expte_obj.tarea_actual.id)])
                        plant_rel_proced_obj = self.env['plantilla.rel'].search(
                                [('tarea_id', '=', expte_obj.tarea_actual.id)])
                else:
                        plant_rel_proced_obj_cant = self.env['plantilla.rel'].search_count(
                                [('procedimiento_id', '=', expte_obj.procedimiento_id.id)])
                        plant_rel_proced_obj = self.env['plantilla.rel'].search(
                                [('procedimiento_id', '=', expte_obj.procedimiento_id.id)])
                # print(("Cantidad de plantillas relacionadas con el tramite: " + str(plant_rel_proced_obj)))
                ids_plantillas = []
                ids_plantillas_rel = []
                for rel in plant_rel_proced_obj:
                        for plant in rel:
                                print((str(plant.id)))
                                ids_plantillas_rel.append(plant.id)
                ids_plantillas_rel_str = ''
                for i in ids_plantillas_rel:
                        if ids_plantillas_rel_str == '':
                                ids_plantillas_rel_str = '(' + str(i)
                        else:
                                ids_plantillas_rel_str = ids_plantillas_rel_str + ", " + str(i)
                if ids_plantillas_rel_str != '':
                        ids_plantillas_rel_str = ids_plantillas_rel_str + ')'
                        # print (("La lista STRING de encontrados es: " + ids_plantillas_rel_str))
                        self.env.cr.execute(
                                """SELECT plantilla_vacia_id FROM plantilla_rel_plantilla_vacia_rel WHERE plantilla_rel_id IN """ + ids_plantillas_rel_str + """;""")
                        plant_rel_ids = self.env.cr.fetchall()
                        # print (("SALIDA: " + str(plant_rel_ids)))
                        for e in plant_rel_ids:
                                ids_plantillas.append(e)
                # FIN OBTENER LAS RELACIONES
                if plant_rel_proced_obj_cant > 0:
                        # NUEVO PASE A OFICINA
                        return {
                                'name': "Plantillas Asociadas a la Tarea/Tramite",
                                'view_mode': 'tree',
                                # 'res_id': active_id,
                                # 'view_id': self.env.ref('pase.form_enviar').id,
                                'res_model': 'plantilla.vacia',
                                'type': 'ir.actions.act_window',
                                # 'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
                                'domain': [('id', 'in', ids_plantillas)],
                                'context': {'recibido': False, 'oficina_destino': False, 'observ_pase': ''},
                                'views': [[self.env.ref('plantilla.vacia_list').id, "tree"]],
                                'target': 'new',
                        }
                else:
                        return {
                                'name': "No se Encontraron Plantillas Asociadas a la Tarea/Tramite",
                                'view_mode': 'tree',
                                # 'res_id': active_id,
                                # 'view_id': self.env.ref('pase.form_enviar').id,
                                'res_model': 'plantilla.vacia',
                                'type': 'ir.actions.act_window',
                                # 'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
                                'domain': [('id', 'in', ids_plantillas)],
                                'context': {'recibido': False, 'oficina_destino': False, 'observ_pase': ''},
                                'views': [[self.env.ref('plantilla.vacia_list').id, "tree"]],
                                'target': 'new',
                        }
                return True