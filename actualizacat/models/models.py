# -*- coding: utf-8 -*-

from odoo import models, fields, api
import ConfigParser
import os
import psycopg2
import traceback
from unidecode import unidecode
from odoo.exceptions import UserError, ValidationError

class actualizacat(models.Model):
    _name = 'actualizacat.actualizacat'

    procedimiento_id = fields.Many2one('procedimiento.procedimiento', 'Tramite', required=True)
    tablacat = fields.Char(required=True)



class expediente(models.Model):

    _name = 'expediente.expediente'
    _inherit = 'expediente.expediente'
    _description = "Agregar acciones en el cambio de estado legal"

    #Obtener Tabla Correspondiente al Tramite Seleccionado
    def tabla_reg_catastral(self, tramite_id):
        actualizacat_obj = self.env['actualizacat.actualizacat']
        actualizacat_ids_encontrados = actualizacat_obj.search([('procedimiento_id', '=', tramite_id)], limit=1)
        # print (("IDS ENCONTRADOS " + str(actualizacat_ids_encontrados)))
        if actualizacat_ids_encontrados:
            print (("La Tabla obtenida para el tramite es: " + str(actualizacat_ids_encontrados[0].tablacat)))
            return str(actualizacat_ids_encontrados[0].tablacat)
        else:
            print(("No se encontro tabla relacionada con el tramite."))
            return False

    #Conectarse al la base del registro catastral
    def conect(self):
        thisfolder = os.path.dirname(os.path.abspath(__file__))
        initfile = os.path.join(thisfolder, 'config.ini')
        config = ConfigParser.ConfigParser()
        config.read(initfile)
        ##Publicacion
        self.codprov = config.get('Publicacion', 'codprov')
        #DATABASE
        nameDB = config.get('DB', 'nameDBgis')
        userDB = config.get('DB', 'userDBgis')
        passDB = config.get('DB', 'passDBgis')
        hostDB = config.get ('DB', 'hostDBgis')
        print ("CONECTANDO DB--....", nameDB)
        print ("USER--....", userDB)
        print ("PASS--....", passDB)
        print ("HOST--....", hostDB)
        #
        try:
            conn = psycopg2.connect(dbname=nameDB,user=userDB,password=passDB, host=hostDB)
        except psycopg2.DatabaseError as e:
            print (("Error de conexion con la BD local"))
            print ((e))
            print ((e.pgcode))
            print ((e.pgerror))
            print ((traceback.format_exc()))
        return conn

    def update_valor_registro(self, tabla_selec, state_selec, exp_buscar):
        """ Actualizar el valor del registro catastrol """
        # sql = """UPDATE %s
        #             SET estado_legal = %s
        #             WHERE expediente = %s"""
        query = "UPDATE " + tabla_selec + " SET estado_legal = '" + state_selec + "' WHERE expediente = '" + exp_buscar + "'"
        print (("CONSULTA : " + query))
        conn = None
        updated_rows = 0
        try:
            # connect to the PostgreSQL database
            conn = self.conect()
            # create a new cursor
            cur = conn.cursor()
            # execute the UPDATE  statement
            # cur.execute(sql, (tabla_selec, state_selec, exp_buscar))
            cur.execute(query,)
            # get the number of updated rows
            updated_rows = cur.rowcount
            # Commit the changes to the database
            conn.commit()
            # Close communication with the PostgreSQL database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return updated_rows

    #Buscar el registro a actualizar
    #Actualizar el Registro
    def actualizar_registro(self, exp_buscar, state_selec, tramite_id):
        # tabla_modificar = "minas"
        tabla_modificar = self.tabla_reg_catastral(tramite_id)
        if tabla_modificar != 'minas':
            return False
        print (("TABLA A MODIFICAR ES: "+ str(tabla_modificar)))
        tabla_selec = 'public.' + tabla_modificar
        print (("CARGANDO DATOS DE LA TABLA ... ->>" + tabla_selec))
        cant = self.update_valor_registro(tabla_selec, state_selec, exp_buscar)
        print (("CANTIDAD DE REGISTROS MODIFICADOS: " + str(cant)))
        """
        self.conn = self.conect()
        self.cursor2gis = self.conn.cursor()
        try:
            query = "UPDATE "+tabla_selec+" SET estado_legal = '" + state_selec+ "' WHERE expediente = '" + exp_buscar + "'"
            print (("CONSULTA: " + query))
            self.cursor2gis.execute(query)
        except psycopg2.Error as e:
            pass
            print ((e.pgerror))
        self.conn.commit()
        self.conn.close()
        """
        return True

    #Trigger al cambiar el estado legal actual
    @api.multi
    @api.onchange('estado_legal_actual_id')
    def _change_estado_legal(self):
        print (("#### VALORES OBTENIDOS ####"))
        print (("Numero de Expediente: " + unidecode(self.name)))
        print (("Valor a asignar: " + unidecode(self.estado_legal_actual_id.name)))
        print (("Tramite: " + unidecode(self.procedimiento_id.name)))
        self.actualizar_registro(self.name, self.estado_legal_actual_id.name, self.procedimiento_id.id)

    def tramite_configurado(self, tramite_id):
        conf_obj = self.env['actualizacat.actualizacat']
        conf_encontrados = conf_obj.search([('procedimiento_id', '=', tramite_id)])
        if conf_encontrados:
            return True
        else:
            return False

    def actualiza_todos(self):
        print(("ACTUALIZANDO A TRAVES DE TEMPORIZADOR"))
        exp_obj = self.env['expediente.expediente']
        exp_encontrados = exp_obj.search([('state', '=', 'active')])
        count = 1
        for exp in exp_encontrados:
            print (("Exp. N* " + str(count) + " : "+ str(exp.name)))
            # self.actualizar_registro(exp.name, exp.estado_legal_actual, exp.procedimiento_id.id)
            if self.tramite_configurado(exp.procedimiento_id.id) and exp.estado_legal_actual != False:
                print (("TRAMITE CONFIGURADO"))
                self.actualizar_registro(exp.name, exp.estado_legal_actual, exp.procedimiento_id.id)
            else:
                print (("------------------"))
            count = count + 1
        print (("**"))
        return True