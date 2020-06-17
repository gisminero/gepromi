# -*- coding: utf-8 -*-

from odoo import models, fields, api
from base import base
import psycopg2, psycopg2.extras
import urllib2
import ConfigParser
import os
from string import join
import time

class tablesfind(models.Model):
    _name = 'tablesfind.tablesfind'
    id_gis = fields.Integer('Id en Gis?')
    name = fields.Char('Expediente')
    titular = fields.Char('Titular')
    mineral = fields.Char('Mineral')
    estado_legal = fields.Many2one('estado_legal.estado_legal', 'Estado Legal', copy=False, required=False)
    #lista_id = fields.Many2one('gisupdate.gisupdate', 'Flujo', ondelete='cascade', select=True)
    #value = fields.Integer()
    #value2 = fields.Float(compute="_value_pc", store=True)
    #description = fields.Text()

class tablesgis(models.Model):
    _name = 'tablesgis.tablesgis'
    cod = fields.Char('Codigo')
    name = fields.Char('Nombre')

    def __init__(self, uid, cr):
        super(tablesgis, self).__init__( uid, cr)
        #HABILITAR PARA LA INSTALACION
        #os.system("python /opt/odoo/server/addonsgis/gisupdate/models/actions/loadnames.py")


class gisupdate(models.Model):
    _name = 'gisupdate.gisupdate'
    #tabla = fields.Selection(selection=[('canteras_f2', 'canteras_f2'),
                                                #('canteras_f3', 'canteras_f3'),
                                                #('cateos_f2', 'cateos_f2'),
                                                #('cateos_f2', 'cateos_f3')],
                                                #string='Tabla a Buscar')
    tabla = fields.Many2one('tablesgis.tablesgis', 'Tabla de Busqueda', copy=False, required=False)
    #expte = fields.Char('Expediente a Buscar')
    #titular = fields.Char('Titular')
    #mineral = fields.Char('Mineral')
    #ingreso = fields.Char('Ingreso')
    #estado_legal = fields.Many2one('estado_legal.estado_legal', 'Estado Legal', copy=False, required=False)


    @api.depends('value')
    def _value_pc(self):
        self.value2 = float(self.value) / 100

    def tableNameFromId(self, tabla_id):
        objtabla = self.env['tablesgis.tablesgis'].browse(tabla_id)
        tabla = str(objtabla[0].name)
        return tabla

    def callVista(self):
        print self.env.context
        if self.env.context.get('id_tabla'):
            tabla_id = self.env.context.get('id_tabla')
            nombre_tabla = self.tableNameFromId(tabla_id)
        else:
            nombre_tabla = " Sin Nombre Tabla "
        if self.env.context.get('uid'):
            user_id = self.env.context.get('uid')
        return {
            'name': nombre_tabla.upper(),
            'view_type': 'form',
            'view_mode': 'tree, form',
            'view_id': self.env.ref('gisupdatetable.list').id,
            'res_model': 'gisupdatetable.gisupdatetable',
            'type': 'ir.actions.act_window',
            'context': {
                #'id_activo': self.env.context['active_id'],
                'nombre_tabla': "CATEOS PRUEBA",
                },
            #'target': 'current',
            'domain': [('create_uid', '=', user_id)],
            'views': [[False, "tree"], [False, "form"]],
            #'target': 'new', #ESTA OPCION ABRE UN POP UP, MUY INTERESANTE
            }


    def callTabla(self, tabla_id):
        print (("CONTEXTO"))
        print self.env.context
        #id_tabla_context = self.env.context.get('id_tabla')
        if self.env.context.get('uid'):
            user_id = self.env.context.get('uid')
        #else:
            #nombre_tabla = " Sin Nombre Tabla "
        print (("CONTEXTO ID TABLA: "+ str()))
        time.sleep(2)
        if tabla_id is not False:
            tabla = self.tableNameFromId(tabla_id)
            print (("EL NOMBRE DE LA TABLA DENTRO DEL IF ES ", tabla ))
            os.system('python /opt/odoo/server/addonsgis/gisupdate/models/actions/loadtable.py ' + tabla + ' '+ str(user_id))
        return {'value': {'encontrados_ids': False}}

    #def callResult(self, id_form, expte_search, tabla, context):
        #print (("LA BUSQUEDA SE ESTA REALIZANDO", str(id_form), str(expte_search), str(tabla) ))
        #activo = context.get('active_id')
        #print ((" ACTIVO " + str(activo)))
        #return {'value': {'encontrados_ids': False}}


    def loadTable(self, tabla_select):
        #print (("CARGANDO TABLA ..." + str(tabla_select) + " COD PROV "+ str(base.test())))
        print (("CARGANDO TABLA ..." + str(tabla_select) ))
        return {'value': {'encontrados_ids': False}}


