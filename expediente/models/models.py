# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from unidecode import unidecode
import string

class expediente(models.Model):
    _name = 'expediente.expediente'
    #_order = "momento_inicio desc"
    #Se cambia el orden a la fecha de ultima modificacion
    _order = "write_date desc"

    def default_user_id(self):
        return self.env.context.get("default_user_id", self.env.user)

    def default_user_id_view(self):
        return self.env.context.get("default_user_id", self.env.user).id

    #@api.depends('provincia')
    def default_expte(self):
        state_id = self.env.user.company_id.state_id.id
        if state_id == 561:
            next_seq = self.env['ir.sequence'].next_by_code('sec_expediente')
        elif state_id == 566:
            next_seq = ''
        else:
            next_seq = ''
        return str(next_seq)

    def depart_user(self):
        user_id = self.env.context.get("default_user_id", self.env.user).id
        id_depart = self.userdepart(user_id)
        #print (("EL ID DE DEPARTAMENTO ES :" + str(id_depart)))
        return [id_depart]

    def vista_mi_ofi_texto(self):
        user = self.env.context.get("default_user_id", self.env.user)
        id_depart = self.userdepart(user)
        #user_id = self.env.context.get('uid')
        return "---: " + str(id_depart)

    # @api.one
    # @api.depends('recibido')
    def solic_nombre(self, solicitante, name, provincia):
        prov = self.env.user.company_id.state_id.name
        pase_obj = self.env['pase.pase']
        ret_name = name
        if prov == 'Jujuy':
            if solicitante:
                parte_name = string.split(name, '-')
                ret_name = parte_name[0] + '-' + str(solicitante[0])+'-'+parte_name[2]
            return {'value': {'name': ret_name}}
        else:
            return {'value': {'name': ret_name}}

    @api.one
    @api.depends('provincia')
    def _compute_state(self):
        self.provincia = self.env.user.company_id.state_id

    def default_state(self):
        return self.env.user.company_id.state_id

    @api.one
    @api.depends('recibido')
    def _is_recept_doc(self):
        id_active = self.id
        if id_active:
            pase_obj = self.env['pase.pase']
            res = pase_obj.ultima_condicion_recibido(id_active)
            self.recibido = res

    @api.one
    @api.depends('state')
    def _archivar_exped(self):
        self.state = 'archive'

    name = fields.Char('Expediente', required=True, readonly=False, default=default_expte)
    state = fields.Selection([('draft', 'Borrador'), ('active', 'Activo'),
        ('archive', 'Archivo')], string='Estado', required=True, default="draft",
        help="Determina el estado del expediente")
    procedimiento_id = fields.Many2one('procedimiento.procedimiento','Tramite', required=True)
    solicitante = fields.Char('Solicitante', required=True)
    folios = fields.Integer('Folios', help='', default=1)
    estado_legal_actual = fields.Char('Estado Legal Actual', required=False, readonly=True)
    estado_legal_actual_id = fields.Many2one('estado_legal.estado_legal', string='Estado Legal Actual', required=False)
    mineral = fields.Many2many('mineral',string='Mineral',required=False, domain=[('active', '=', True)])
    nombre_pedimento = fields.Char('Nombre Pedimento', required=False)
    user_creador_id = fields.Many2one('res.users','Creado por', required=False, readonly=True, default=default_user_id)
    momento_inicio = fields.Datetime('Creado el', readonly=True, default=fields.Datetime.now)
    active = fields.Boolean('Activo', default=True, readonly=True)
    ultimo_pase_id = fields.Integer('Id Ultimo Movimiento', readonly=True)
    ubicacion_actual = fields.Many2one('hr.department','Ubicacion Actual', readonly=True)
    oficina_destino = fields.Many2one('hr.department','Oficina Destino', readonly=False)
    recibido = fields.Boolean('Recibido', readonly=True, compute=_is_recept_doc, store=False)
    observ_pase = fields.Text(string='Observaciones de Pase', translate=True)
    provincia = fields.Many2one('res.country.state', string="Provincia", default=default_state, readonly=True)#, store=True
    departamento = fields.Many2many('departamento.departamento', string="Departamento",required=False, domain=[('active', '=', True)])
    #departamento = fields.Many2one('departamento.departamento', string="Departamento")
    observaciones = fields.Text(string='Observaciones', translate=True)
    empleado = fields.Many2one('hr.employee','Empleado Asignado', readonly=False)
    #_sql_constraints =[('name_uniq_exp', 'unique(name)', 'El numero de Expediente debe ser único para cada trámite')]

    def userdepart(self, user_id):
        num_empl = self.env['hr.employee'].search_count([('user_id', '=', [user_id])])
        if num_empl < 1:
            print (("No se encuentra el empleado asociado al usuario: " + str(user_id)))
            return False
        elif num_empl > 1:
            print (("Hay mas de un emplado asociado al usuario: " + str(user_id)))
            return False
        else:
            empl_obj = self.env['hr.employee'].search([('user_id', '=', [user_id])])
            if empl_obj.department_id.id:
                return empl_obj.department_id.id
            else:
                print (("EL EMPLEADO NO TIENE OFICINA ASIGNADA"))
                return False

    def activar(self):
        active_id = self.env.context.get('id_activo')
        print (("ACTIVANDO .... " + str(active_id)))
        user_id = self.env.user.id
        #print ((" CONTEXTO ACTIVANDO ... : " + str(self.env.context)))
        expte_obj = self.browse([active_id])
        depart_id = self.userdepart(user_id)
        if depart_id:
            pase_obj = self.env['pase.pase']
            pase_obj.create({'folios': 1, 'user_origen_id': user_id,
                        'user_recep_id': user_id,
                        'name': str(expte_obj.name), 'expediente_id' : active_id,
                        'depart_origen_id': depart_id,
                        'depart_destino_id': depart_id,
                        'fecha_hora_recep': fields.datetime.now()})
            #self._cr.execute("""INSERT INTO public.pase_pase(
                    #folios, user_origen_id, name, expediente_id,
                    #depart_origen_id, depart_destino_id, fecha_hora_envio)
                    #VALUES (1, %s, '%s', %s, %s, %s);"""
                    #% (user_id, expte_obj.name, active_id,
                    #depart_id, depart_id, ))
            expte_obj.write({'state': "active", "recibido": True})
        else:
            raise ValidationError(('El empleado no tiene oficina asignada o se encuentra asignado a varias oficinas'))
        return True

    def aviso(self, titulo, mensaje):
        print(('PROBANDO EL SEGUNDO POP '))
        view = self.env.ref('sh_message.sh_message_wizard')
        view_id = view and view.id or False
        context = dict(self._context or {})
        context['message'] = mensaje
        return {
            'name': titulo,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context,
            }

    def validacion(self, campo, valor):
        if campo == "folios":
            if valor < 2:
                print (("VALIDACION DE FOLIOS"))
                self.aviso("Validacion Folios", "Debe cargar el numero de folios.")
                return False
        elif campo =="destino":
            print(("VALIDACION DE DESTINO 11"))
            if not valor:
                print (("VALIDACION DE DETINO 22"))
                self.aviso("Validacion Destino", "Debe ingresar oficina destino.")
                return False
        else:
            return True

    def reload_view(self):
        action = {
                'type': 'ir.actions.client',
                'tag': 'reload',
        }
        return action

    def mi_oficina_view(self):
        user_id = self.env.user.id
        depart_user_id = self.userdepart(user_id)
        if depart_user_id > 0:
            action = {
                'name': "Expedientes en Mi Oficina",
                'view_mode': 'tree, form',
                'res_model': 'expediente.expediente',
                'type': 'ir.actions.act_window',
                'domain': [('ubicacion_actual', '=', self.env['expediente.expediente'].depart_user())],
                'views': [[self.env.ref('expediente.mi_oficina_list').id, "tree"], [self.env.ref('expediente.form').id, "form"]],
                }
        return action

    def cancel_return_mi_oficina(self):
        tipo_retorno = self.env.context.get('vista_padre')
        #print ((str(tipo_retorno)))
        #print((str(self.env.context)))
        user_id = self.env.user.id
        depart_user_id = self.userdepart(user_id)
        # if tipo_retorno == 'view':
        #     #print (("VOLVIENDO POR VISTA TREE"))
        if depart_user_id > 0:
            action = {
                'name': "Expedientes en Mi Oficina",
                'view_mode': 'tree, form',
                'res_model': 'expediente.expediente',
                'type': 'ir.actions.act_window',
                'domain': [('ubicacion_actual', '=', self.env['expediente.expediente'].depart_user())],
                'views': [[self.env.ref('expediente.mi_oficina_list').id, "tree"], [self.env.ref('expediente.form').id, "form"]],
                }
            return action
        # else:
        #     print (("VOLVIENDO POR TRUE"))
            return True

    def recibir_view(self):
        user_id = self.env.user.id
        depart_user_id = self.userdepart(user_id)
        if depart_user_id > 0:
            action = {
                'name': "Expedientes a Recibir",
                'view_mode': 'tree, form',
                'res_model': 'expediente.expediente',
                'type': 'ir.actions.act_window',
                'domain': [('recibido', '=', False), ('oficina_destino', '=', self.env['expediente.expediente'].depart_user())],
                'views': [[self.env.ref('expediente.list_recibir').id, "tree"], [self.env.ref('expediente.form').id, "form"]],
                }
        return action

    def enviar(self):
        active_id = self.env.context.get('id_activo')
        #self = self.with_context(get_sizes=True)
        print (("ENVIANDO .... " + str(active_id)))
        #print(("CONTEXTO .... " + str(self.env.context)))
        #self.env.context = False
        #print(("CONTEXTO DESPUES DE BORRAR.... " + str(self.env.context)))
        user_id = self.env.user.id
        #print (())
        expte_obj = self.browse([active_id])
        #print (("OBJETO.... " + str(expte_obj.name)))
        depart_id = self.userdepart(user_id)
        #CONSULTANDO PASES
        pase_obj = self.env['pase.pase']
        #pase_res = pase_obj.obtener_ultimo_pase(active_id, depart_id)
        #LA LINEA ANTERIOR CORRESPONDE AL OBTENER ULTIMO PASE ANTES DE LA ULTIMA REVISION DE 29-08-19
        #FIN CONSULTANDO PASES
        if self.recibido:
            #NUEVO PASE A OFICINA
            #self.write({'observaciones': False})
            if depart_id:
                return {
                'name': "Enviando Documento",
                'view_mode': 'form',
                'res_id': active_id,
                #'view_id': self.env.ref('pase.form_enviar').id,
                'res_model': 'expediente.expediente',
                'type': 'ir.actions.act_window',
                #'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
                #'domain': [('recibido', '=', False), ('oficina_destino', '=', self.env['expediente.expediente'].depart_user())],
                'context': {'recibido': False, 'oficina_destino': False, 'observ_pase': '', 'id_activo': active_id},
                'views': [[self.env.ref('expediente.form_enviar').id, "form"]],
                'target': 'new',
                'flags': {'form': {'action_buttons': False}},
                }
            else:
                raise ValidationError(('El empleado no tiene oficina asignada o se encuentra asignado a varias oficinas'))
        else:
            if not expte_obj.oficina_destino.name:
                of_enviado = "-"
            else:
                of_enviado = unidecode(expte_obj.oficina_destino.name)
            if depart_id:
                return {
                'name': "EL DOCUMENTO SE ENCUENTRA ENVIADO A: " + str(of_enviado),
                'view_mode': 'form',
                'res_id': active_id,
                #'view_id': self.env.ref('pase.form_enviar').id,
                'res_model': 'expediente.expediente',
                'type': 'ir.actions.act_window',
                #'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
                #'domain': [('recibido', '=', False), ('oficina_destino', '=', self.env['expediente.expediente'].depart_user())],
                #A CONTINUACION REVISAR EL PRESENTE CONTEXTO LUEGO DE LA MODIFICACION
                'context': {'of_enviado': of_enviado},
                'views': [[self.env.ref('expediente.form_enviado').id, "form"]],
                'target': 'new',
                'flags': {'form': {'action_buttons': False}},
                }
            else:
                raise ValidationError(('El empleado no tiene oficina asignada o se encuentra asignado a varias oficinas'))
        return True

    def enviar_conf(self):
        active_id = self.env.context.get('id_activo')
        #print (("EL ID ACTIVO ESSSS:  .... " + str(active_id)))
        fojas_new = self.env.context.get('fojas_new')
        destino_new = self.env.context.get('oficina_destino_new')
        observaciones_new = self.env.context.get('observaciones_new')
        #La siguiente variable tiene dos valores form y view
        retorno = 'view'
        retorno = self.env.context.get('vista_padre')
        #print(("MOSTRANDO CONTEXT:  .... " + str(self.env.context)))
        #print(("VALOR DE RETORNO:  .... " + str(retorno)))
        #VALIDACION
        if not observaciones_new:
            observaciones_new = "-"
        # if not destino_new:
        #     raise ValidationError(('Debe seleccionar oficina destino.'))
        # if not fojas_new:
        #     raise ValidationError(('Debe asignar numero de fojas.'))
        #self.validacion("folios", fojas_new)
        # self.validacion("destino", destino_new)
        #FIN VALIDACION
        user_id = self.env.user.id
        expte_obj = self.browse([active_id])
        #print (("OBJETO.... " + str(expte_obj.name)))
        depart_id = self.userdepart(user_id)
        if depart_id:
            pase_obj = self.env['pase.pase']
            pase_obj.create({'user_origen_id': user_id,
                        'name': str(expte_obj.name), 'expediente_id': active_id,
                        'depart_origen_id': depart_id,
                        'depart_destino_id': destino_new,
                        'folios': fojas_new,
                        'observ_pase': observaciones_new})
            expte_obj.write({'folios': fojas_new,
                        'recibido': False,
                        'oficina_destino': destino_new,
                        'observ_pase': observaciones_new})
        else:
            raise ValidationError(('El empleado no tiene oficina asignada o se encuentra asignado a varias oficinas'))
        if retorno == 'view':
            print(("VOLVIENTDO POR TREE"))
            return self.mi_oficina_view()
        else:
            print (("VOLVIENTDO POR TRUE"))
            return {
                'name': "Retorno al Formulario Expediente",
                'view_mode': 'form',
                'res_id': active_id,
                # 'view_id': self.env.ref('pase.form_enviar').id,
                'res_model': 'expediente.expediente',
                'type': 'ir.actions.act_window',
                # 'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
                # 'domain': [('recibido', '=', False), ('oficina_destino', '=', self.env['expediente.expediente'].depart_user())],
                # A CONTINUACION REVISAR EL PRESENTE CONTEXTO LUEGO DE LA MODIFICACION
                # 'context': {'of_enviado': of_enviado},
                'views': [[self.env.ref('expediente.form').id, "form"]],
                # 'target': 'new',
                # 'flags': {'form': {'action_buttons': False}},
            }
            #return True
        # res = {'type': 'ir.actions.client', 'tag': 'reload'}
        # return res

    def recibir_conf(self):
        active_id = self.env.context.get('id_activo')
        #fojas_new = self.env.context.get('fojas_new')
        #destino_new = self.env.context.get('oficina_destino_new')
        #print (("Enviando .... " + str(active_id)))
        user_id = self.env.user.id
        #print (())
        expte_obj = self.browse([active_id])
        print (("RECIBIENDO EXPEDIENTE.. " + str(expte_obj.name)))
        depart_id = self.userdepart(user_id)
        if depart_id:
            print (("GRAbando la recepcion"))
            pase_obj = self.env['pase.pase'].search([('user_recep_id', '=', False), ('expediente_id', '=', active_id)], order="fecha_hora_envio desc", limit=1)
            pase_obj.write({'user_recep_id': user_id,
                        'fecha_hora_recep': fields.datetime.now()})
            expte_obj.write({'recibido': True,
                        'oficina_destino': False,
                        'ubicacion_actual': depart_id,
                        'observ_pase': ''})
        else:
            raise ValidationError(('El empleado no tiene oficina asignada o se encuentra asignado a varias oficinas'))
        #return {'type': 'ir.actions.act_window_close'}
        return self.recibir_view()

    def recibir(self):
        print (("RECIBIENDO DOCUMENTO"))
        #pase_obj = self.env['pase.pase']
        #if not pase_obj:
            #raise ValidationError(('Debe instalar el modulo de pases.'))
        #active_id = self.env.context.get('active_ids')
        active_id = self.env.context.get('id_activo')
        #print (("ENVIANDO .... " + str(active_id)))
        user_id = self.env.user.id
        #print (())
        expte_obj = self.browse([active_id])
        #print (("OBJETO.... " + str(expte_obj.name)))
        depart_id = self.userdepart(user_id)
        if depart_id:
            return {
            'name': "Recibiendo Documento",
            'view_mode': 'form',
            'res_id': active_id,
            #'view_id': self.env.ref('pase.form_enviar').id,
            'res_model': 'expediente.expediente',
            'type': 'ir.actions.act_window',
            #'domain': [('ubicacion_actual', '=', env['expediente.expediente'].depart_user())],
            'context': {'recibido': True, 'ubicacion_actual': depart_id},
            'views': [[self.env.ref('expediente.form_recibir').id, "form"]],
            'target': 'new', #ESTA OPCION ABRE UN POP UP, MUY INTERESANTE
            }
        else:
            raise ValidationError(('El empleado no tiene oficina asignada o se encuentra asignado a varias oficinas'))
        return True

    def onchange_recibido_false(self):
        return {'value': {'recibido': False}}

    @api.depends('value')
    def _value_pc(self):
        self.value2 = float(self.value) / 100


    def movimientos(self):
        print (("MOVIMIENTOS DEL DOCUMENTO"))
        tipo_lista = self.env.context.get('tipo_historia')
        #pase_obj = self.env['pase.pase']
        #if not pase_obj:
            #raise ValidationError(('Debe instalar el modulo de pases.'))
        #active_id = self.env.context.get('active_ids')
        #print (("CONTEXTO " + str(self.env.context) ))
        active_id = self.env.context.get('id_activo')
        print (("ENVIANDO .... " + str(active_id)))
        user_id = self.env.user.id
        #print (())
        expte_obj = self.browse([active_id])
        print (("OBJETO.... " + str(expte_obj.name)))
        depart_id = self.userdepart(user_id)
        if tipo_lista == 'tarea':
            return {
            'name': "Movimientos Segun Tareas del Documento: " + expte_obj.name,
            'view_mode': 'tree',
            #'res_id': active_id, #SOLO PARA FORM
            'res_model': 'seguimiento_linea',
            'type': 'ir.actions.act_window',
            'domain': [('seguimiento_id.expediente_id', '=', active_id)],
            #'context': {'recibido': True, 'ubicacion_actual': depart_id},
            'views': [[self.env.ref('tarea_flujo_exp.seguimiento_linea_list').id, "tree"]],
            'target': 'new',
            'tag': 'reload',
            }
        if depart_id:
            return {
            'name': "Movimientos del Documento " + expte_obj.name,
            'view_mode': 'tree',
            #'res_id': active_id, #SOLO PARA FORM
            'res_model': 'pase.pase',
            'type': 'ir.actions.act_window',
            'domain': [('expediente_id', '=', active_id)],
            #'context': {'recibido': True, 'ubicacion_actual': depart_id},
            'views': [[self.env.ref('pase.list').id, "tree"]],
            'target': 'new',
            'tag': 'reload',
            }
        else:
            raise ValidationError(('El empleado no tiene oficina asignada o se encuentra asignado a varias oficinas'))
        return True

    class estado_legal(models.Model):
        _name = 'estado_legal.estado_legal'
        _inherit = 'estado_legal.estado_legal'
        _description = "Traer permisos de modulo estado_legal"
        # _table = 'mrp_recep'
        # _order = "id desc"
        # tarea_actual = fields.Many2one('tarea.tarea', 'Tarea Actual', required=False, readonly=True)
        # tarea_proxima = fields.Many2one('tarea.tarea', 'Tarea Prox.', required=False, readonly=False)
        #otro_campo = fields.Boolean('Otro Campo', required=False, readonly=True)

        # info_tarea = fields.Text(string='Info', translate=True)

        @api.multi
        @api.depends("emeu_sector_id.emeu_education_ids")
        def _get_education_domain(self):
            return True
            """
            for object in self:
                    education_list = []
                    if object.emeu_sector_id.id:
                            education_ids = object.emeu_sector_id.emeu_education_ids
                            education_list = [x.id for x in education_ids]
                    object.education_list = [(6, 0, education_list)]
            """