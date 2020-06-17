# -*- coding: utf-8 -*-

from odoo import models, fields, api
import os
from unidecode import unidecode

class gisupdatetable(models.Model):


    _name = 'gisupdatetable.gisupdatetable'

    id_gis = fields.Integer('Id en Gis', readonly = True)
    name = fields.Char('Expediente', readonly = True)
    nombre = fields.Char('Nombre', readonly = False)
    titular = fields.Char('Titular', readonly = False)
    mineral = fields.Char('Mineral', readonly = False)
    estado_legal_actual = fields.Char('Estado Legal Actual', readonly = False)
    estado_legal = fields.Many2one('estado_legal.estado_legal', 'Nuevo Estado Legal', copy=False, required=False)
    tabla = fields.Char('Tabla', readonly = True)

    #@api.multi
    #def write(self, values):
        #print self.env.context
        ##if self.env.context.get('id'):
        ##active_id = self._context('active_ids')
        #active_id = self.env.context.get('active_ids')
        #obj_gis_table = self.browse(active_id)
        #print (("  OBJETO "+ obj_gis_table.name))
        ##else:
            ##nombre_tabla = " Sin Nombre Tabla "
        #print (("VALORES " + str(values) + "VALOR FILTRADO "+ str(values['estado_legal'])) )
        ##objtabla = self.env['tablesgis.tablesgis'].browse(tabla_id)
        ##tabla = str(objtabla[0].name)
        #print (("llamando a UPDATER... "))
        #res = super(gisupdatetable, self).write(values)
        #return res

    def setStatus(self, tabla, id_gis, id_estado):
        #objtabla = self.env['tablesgis.tablesgis'].browse(tabla_id)
        #tabla = str(objtabla[0].name)
        print (("LLLAMANSO" + tabla+ " -", str(id_gis), str(id_estado)))
        #print (("CONTEXTO ID TABLA: "+ str()))
        objestado = self.env['estado_legal.estado_legal'].browse(id_estado)
        estado = str(unidecode(objestado[0].name))
        estado_odoo = objestado[0].name
        if tabla is not False:
            #print (("EL NOMBRE DE LA TABLA DENTRO DEL IF ES ", tabla ))
            os.system("python /opt/odoo/server/addonsgis/gisupdate/models/actions/changestate.py '" + estado + "' " + str(id_gis)+ ' ' + tabla)
            self.write({'value': {'estado_legal_actual': estado_odoo}})
        return {'value': {'estado_legal_actual': estado_odoo}}

    def estado_legal_str(self, estado_num):
        estado_legal_str = ''
        return estado_legal_str

    def write(self, vals):
        print (("Id de Odoo " + str(self.id)))
        odoo_obj = self.env['gisupdatetable.gisupdatetable']
        odoo_obj_select = odoo_obj.browse([self.id])
        tabla_str = str(odoo_obj_select.tabla)
        id_gis_str = str(odoo_obj_select.id_gis)
        print (("TABLA: " + tabla_str + " ID GIS: " + id_gis_str))
        print (("LISTO PARA ACTUALOZAR"))
        print ((str(vals)))
        for valor in vals:
            if valor != 'estado_legal' and valor != 'estado_legal_actual':
                nombre_val = str(valor)
                print (("EL PAR ES: " + str(valor)))
                valor_val = str(vals[valor])
                print (("EL VALOR DEL PAR ES: " + str(vals[valor])))
                os.system("python /opt/odoo/server/addonsgis/gisupdate/models/actions/changefield.py '" + nombre_val + "' '" + valor_val +"' " + str(id_gis_str)+ ' ' + tabla_str)
        res = super(gisupdatetable, self).write(vals)
        return res

    #lista_id = fields.Many2one('gisupdate.gisupdate', 'Flujo', ondelete='cascade', select=True)
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
