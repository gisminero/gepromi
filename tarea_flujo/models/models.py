# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.exceptions import Warning

class flujolinea(models.Model):
    _name = 'tarea_flujo.flujolinea'
    _description = 'Lineas del Flujo de Tareas'
    tarea = fields.Many2one('tarea.tarea', 'Destino', copy=False, required=True)
    tarea_padre = fields.Many2one('tarea.tarea', 'Origen', copy=False, required=True, help="PRESIONAR el botón Editar Flujo al iniciar la carga de datos")
    descrip = fields.Char('Condiciones', required=False, help="""Indicar si hay condiciones especiales que conduzcan hacia esta tarea""")
    flujo_id = fields.Many2one('tarea_flujo.flujo', 'Flujo', required=1, ondelete='cascade', select=True)


    def suspendeflujo(self, tareas):
        s=0
        print("El valor almacenado" + str(proc_ini))
        tar = self.env['tarea.tarea'].browse(tareas)
        if tar!= False:
            if ((proc_ini=='1') and (tar.tipo =='5')):
                s=1+0
            return s

#    @api.constrains()
    def tareaSusp(self,tareap_id):
        tar = self.env['tarea.tarea'].browse(tareap_id)
        if tar!= False:
            if ((proc_ini=='1') and (tar.tipo =='5')):
                return{'warning':{
                                    'title':('Información'),
                                    'message':('Esta tarea solo puede usarse en un subproceso'),
                                    },
                        'value':{'tarea_padre':False}}

            else:
                 return {'value':{'tarea_padre':tareap_id}}

    ls=[]
#    @api.constrains()
    @api.depends('ls')
    def tareaInicial(self, tarea_id,tareapadre_id):
        sp=self.suspendeflujo(tarea_id)
        if sp ==1:
            return {'warning':{
                                'title':('Información'),
                                'message':('Esta tarea solo puede usarse en un subproceso'),
                                },
                    'value':{'tarea':False}
                   }
        else:
            lista=self.ls
            tarea = self.env['tarea.tarea'].browse(tareapadre_id)
            if (tareapadre_id!= False):
                if(tareapadre_id ==tarea_id):
                    return {'warning':{
                                        'title':('Información'),
                                        'message':('La tarea origen no puede ser igual a la tarea destino'),
                                        },
                            'value':{'tarea':False}}
                else:
                    if tarea.tipo =='3':
                        return {'warning':{
                                        'title':('Información'),
                                        'message':('La tarea origen no puede ser una tarea de tipo Final'),
                                        },
                            'value':{'tarea_padre':False}}
                    else:
                        if not[tareapadre_id,tarea_id] in lista:
                            lista.append([tareapadre_id,tarea_id])
                            print("El valor de lista:" + str(lista))
                            tareahijo = self.env['tarea.tarea'].browse(tarea_id)
                            if tareahijo.tipo == '3':
                                j=len(lista)
                                print("J ES: "+ str(j))
                                i=0
                                while j>0:
                                    print("I ES: "+ str(i))
                                    print("EL VALOR DE LA LISTA EN DESTINO:" + str(lista[i]))
                                    del lista[i]
                                    j=len(lista)
                                    print("J2 ES: "+ str(j))
                                    print("terminado")
                        else:
                            return{'warning':{
                                    'title':('Información'),
                                    'message':('Esta linea de flujo ya fue ingresada anteriormente'),
                                    },
                                    'value':{'tarea_padre':False,'tarea':False}}


class flujo(models.Model):
    _name = 'tarea_flujo.flujo'
    _description = 'Flujo de Tareas'
    name = fields.Many2one('procedimiento.procedimiento', 'Procedimiento', copy=False, required=True, help="""Luego de seleccionar Procedimiento, PRESIONAR el botón "Editar Flujo""""")
    lineflujo_ids = fields.One2many('tarea_flujo.flujolinea', 'flujo_id', 'Flujo Lines',)
    _sql_constraints =[('name_uniq', 'unique(name)', 'El flujo debe ser ùnico para cada tràmite')]
    observaciones = fields.Text(string='Observaciones', translate=True)

    proc_ini=0
    def obtener_id(self):
        active_id = self.env.context.get('id_activo')
        print("El valor del procedimiento en el flujo: " + str(active_id))
        procedim=self.env['procedimiento.procedimiento'].browse(active_id)
        print("Aqui obtengo quien inicio el procedimiento: "+ str(procedim.iniciado))
        global bandera
        bandera=True
        global proc_ini
        proc_ini=procedim.iniciado

    def crear_archivo(self,dic):
        newfile= open("archivo_flujo","w")
        print("El archivo se ha creado")

    def exportar(self):
        active_id = self.env.context.get('id_activo')
        datexp = self.env['tarea_flujo.flujolinea'].search([('flujo_id', '=', active_id)])
        diccionario={}
        lista=[]
        for row in datexp:
            dest=row.tarea_padre.id
            orig=row.tarea.id
            cond=row.descrip
            lista.append([dest,orig,cond])
        for i in range(len(lista)):
            indice=i
            flujo=lista[indice]
            lista1=[]
            for j in range(len(flujo)-1):
                indice1=j
                valor=flujo[indice1]
                ident=self.env['tarea.tarea'].search([('id', '=',valor)])
                dato=ident.name
                lista1.append(dato)
            lista1.append(flujo[len(flujo)-1])
            diccionario[indice]=lista1
        print("Diccionario:" + str(diccionario))
        archivo=self.crear_archivo(diccionario)
#        newfile= open("archivo_flujo","w")
#        print("El archivo se ha creado")
