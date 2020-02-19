# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from unidecode import unidecode
# from PyPDF2 import PdfFileWriter, PdfFileReader

class doc_digital_archivo(models.Model):
        _name = 'doc_digital.archivo'
        _order = "id asc"

        def default_archivo_name(self):
                nombre = "Adjunto.pdf"
                return nombre

        def user_emple(self, user_id):
                num_empl = self.env['hr.employee'].search_count([('user_id', '=', [user_id])])
                if num_empl < 1:
                        print(("No se encuentra el empleado asociado al usuario: " + str(user_id)))
                        return False
                elif num_empl > 1:
                        print(("Hay mas de un emplado asociado al usuario: " + str(user_id)))
                        return False
                else:
                        empl_obj = self.env['hr.employee'].search([('user_id', '=', [user_id])])
                        if empl_obj.id:
                                return empl_obj.id
                        else:
                                return False

        def _default_archivo_emple(self):
                user_id = self.env.user.id
                emple_id = self.user_emple(user_id)
                return emple_id

        name = fields.Char('Nombre', required=True, default=default_archivo_name, readonly=True)
        archivo = fields.Binary('Archivo', required=True, filters='*.png,*.gif')
        # archivo_name = fields.Char('Nombre Archivo', required=False)
        doc_digital_id = fields.Many2one('doc_digital', string='Doc. Digital')
        state = fields.Selection([('draft', 'Borrador'), ('active', 'Activo'), ],
                                 string='Estado', required=True, default="draft",
                                 help="Determina el estado del expediente")
        empleado_envia = fields.Many2one('hr.employee', 'Enviado por', readonly=True, default=_default_archivo_emple)

        def reload_view(self):
                action = {
                        'type': 'ir.actions.client',
                        'tag': 'reload',
                }
                return action

        def eliminar_linea(self):
                # print (("ELIMINAND0 LINEA"))
                active_id = self.env.context.get('id_activo')
                dda_obj = self.browse([active_id])
                doc_digital_id = dda_obj.doc_digital_id
                dda_obj.unlink()
                # print (("EL ID DE DOC DIGITAL ES: " + str(doc_digital_id.id)))
                return {
                        'name': "Documentos Digitales Asociados al Expediente",
                        'view_mode': 'form',
                        'res_id': doc_digital_id.id,
                        # 'view_id': self.env.ref('pase.form_enviar').id,
                        'res_model': 'doc_digital',
                        'type': 'ir.actions.act_window',
                        # 'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
                        # 'domain': [('id', 'in', ids_plantillas)],
                        # 'context': {'recibido': False, 'oficina_destino': False, 'observ_pase': ''},
                        'views': [[self.env.ref('doc_digital.form').id, "form"]],
                        'target': 'current',  # 'target': 'new',
                }

        @api.constrains('name')
        def onchange_nombre(self):
                nombre = self.name
                nombre_array = nombre.split('.')
                if len(nombre_array) > 2:
                        raise ValidationError(('El nombre de archivo solo puede tener un punto.'))
                if nombre_array[1] != 'pdf':
                        raise ValidationError(('Solo se admiten archivos .pdf.'))
                return True

        @api.constrains('archivo')
        def onchange_archivo(self):
                # output = PdfFileWriter()
                # input1 = PdfFileReader(open("document1.pdf", "rb"))
                # output.addPage(input1.getPage(0))
                # outputStream = open("PyPDF3-output.pdf", "wb")
                # output.write(outputStream)
                return True

        def verify_sign(public_key_loc, signature, data):
                '''
                Verifies with a public key from whom the data came that it was indeed
                signed by their private key
                param: public_key_loc Path to public key
                param: signature String signature to be verified
                return: Boolean. True if the signature is valid; False otherwise.
                fuente: https://gist.github.com/lkdocs/6519372
                '''
                from Crypto.PublicKey import RSA
                from Crypto.Signature import PKCS1_v1_5
                from Crypto.Hash import SHA256
                from base64 import b64decode
                pub_key = open(public_key_loc, "r").read()
                rsakey = RSA.importKey(pub_key)
                signer = PKCS1_v1_5.new(rsakey)
                digest = SHA256.new()
                # Assumes the data is base64 encoded to begin with
                digest.update(b64decode(data))
                if signer.verify(digest, b64decode(signature)):
                        return True
                return False

class doc_digital(models.Model):
        _name = 'doc_digital'
        _order = "write_date desc"

        name = fields.Char('Nombre', readonly=False, required=False)
        descrip = fields.Char('Descripcion', required=False)
        expediente_id = fields.Many2one('expediente.expediente', 'Id Expediente', required=True)
        archivos_id = fields.One2many('doc_digital.archivo', 'doc_digital_id', string='Archivos Asociados')
        _sql_constraints = [('exp_uniq_doc_digital', 'unique(expediente_id)', 'El panel de archivos asociados a un expediente debe ser único')]

        def _get_permiso_asignacion(self):
                desired_group_name = self.env['res.groups'].search([('name', '=', 'Asignacion')])
                is_desired_group = self.env.user.id in desired_group_name.users.ids
                if is_desired_group:
                        #print(("EL USUARIO SE ENCUENTRA HABILITADO PARA INSERTAR EXPEDIENTES"))
                        return True
                else:
                        #print(("NOOO EL USUARIO SE ENCUENTRA HABILITADO INSERTAR EXPEDIENTES"))
                        return False

        def user_emple(self, user_id):
                num_empl = self.env['hr.employee'].search_count([('user_id', '=', [user_id])])
                if num_empl < 1:
                        print(("No se encuentra el empleado asociado al usuario: " + str(user_id)))
                        return False
                elif num_empl > 1:
                        print(("Hay mas de un emplado asociado al usuario: " + str(user_id)))
                        return False
                else:
                        empl_obj = self.env['hr.employee'].search([('user_id', '=', [user_id])])
                        if empl_obj.id:
                                return empl_obj.id
                        else:
                                return False

        def activar_archivos(self):
                print (("ACTIVANDO LOS ARCHIVOS ADJUNTOS EN EL EXPEDIENTE"))
                active_id = self.env.context.get('id_activo')
                doc_digital_obj = self.browse([active_id])
                user_id = self.env.user.id
                emple_id = self.user_emple(user_id)
                print (("QUE TRAE DESDE EL :" + str(emple_id)))
                for archivo in doc_digital_obj.archivos_id:
                        if archivo.state == 'draft' and archivo.empleado_envia.id == emple_id:
                                archivo.write({'state':  'active'})
                        print(("NOMBRE DE ARCHIVO: " + str(archivo.name)))
                return True

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
                #####################################
                # depart_actual_expte_id = expte_obj.ubicacion_actual
                depart_user_actual_id = self.userdepart(user_id)
                if not depart_user_actual_id:
                        print(("No hay oficina actual asignada."))
                if depart_user_actual_id != depart_actual_id.id:
                        print(("No pertenece a la misma oficina que el expediente."))
                        raise ValidationError(
                                ('Solo puede acceder a esta informacion si el expediente se encuentra en la oficina.'))
                ################################
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
                                'target': 'current', #'target': 'new',
                        }
                else:
                        return {
                                'name': "Documentos Digitales Asociados al Expediente",
                                'view_mode': 'form',
                                # 'res_id': doc_digital_obj[0].id,
                                'res_model': 'doc_digital',
                                'type': 'ir.actions.act_window',
                                # 'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
                                #'domain': [('id', 'in', ids_plantillas)],
                                'context': {'default_expediente_id': expte_obj.id, 'default_name': expte_obj.name},
                                'views': [[self.env.ref('doc_digital.form').id, "form"]],
                                'target': 'current', #'target': 'new',
                        }
                return True