# -*- coding: utf-8 -*-
import psycopg2, psycopg2.extras
import urllib2
import ConfigParser
from string import join
import os
import sys

class loadtable():
    def __init__(self, tabla_arg, user_arg):
        print (("LA TABLA ES: "+ str(tabla_arg)))
        self._table_name = tabla_arg
        self._user_id = user_arg
        #print (("LA VARIABLE GLOBAL ES: "+ str(_table_name)))

    def conect(self):
        thisfolder = os.path.dirname(os.path.abspath(__file__))
        initfile = os.path.join(thisfolder, 'config.ini')
        config = ConfigParser.ConfigParser()
        config.read(initfile)
        ##Publicacion
        #self.host = config.get('Publicacion', 'host')
        #self.port = config.get('Publicacion', 'port')
        self.codprov = config.get('Publicacion', 'codprov')
        #DATABASE
        nameDB = config.get('DB', 'nameDBgis')
        userDB = config.get('DB', 'userDBgis')
        passDB = config.get('DB', 'passDBgis')
        hostDB = config.get('DB', 'hostDBgis')
        print ("CONECTANDO DB--....", nameDB)
        self.conn = psycopg2.connect(dbname=nameDB, user=userDB, password=passDB, host=hostDB)
        #self.conn = psycopg2.connect(dbname='nacion',user='postgres',password='23462', host='localhost')
        try:
            self.cursor = self.conn.cursor()
        except psycopg2.DatabaseError as e:
            #logging.info("Error de conexion con la BD local")
            print ((e.pgerror))
        if self.cursor:
            #logging.info("Conexion correcta con la BD local: " + nameDB)
            print (("Conexion correcta con la BD local: " + nameDB))
        else:
            print ("Error de conexion con la BD local")
        return self.cursor

    def conectodoo(self):
        thisfolder = os.path.dirname(os.path.abspath(__file__))
        initfile = os.path.join(thisfolder, 'config.ini')
        config = ConfigParser.ConfigParser()
        config.read(initfile)
        ##Publicacion
        #self.host = config.get('Publicacion', 'host')
        #self.port = config.get('Publicacion', 'port')
        self.codprov = config.get('Publicacion', 'codprov')
        #DATABASE
        nameDB = config.get('DB', 'nameDBodoo')
        userDB = config.get('DB', 'userDBodoo')
        passDB = config.get('DB', 'passDBodoo')
        hostDB = config.get('DB', 'hostDBodoo')
        print ("CONECTANDO DB--....", nameDB)
        #self.conn = psycopg2.connect(dbname='nacion',user='postgres',password='23462', host='localhost')
        try:
            conn2 = psycopg2.connect(dbname=nameDB, user=userDB, password=passDB, host=hostDB)
            #self.cursor = self.conn2.cursor()
        except psycopg2.DatabaseError as e:
            #logging.info("Error de conexion con la BD local")
            print ((e.pgerror))
        return conn2

    def loadTable(self):
        print (("LA VARIABLE DENTRO DE FUNCION ES: "+ str(self._table_name)))
        print (("LA VARIABLE USUARIO DENTRO DE FUNCION ES: "+ str(self._user_id)))
        tabla_selecc = self._table_name
        user_selecc = self._user_id
        self.conn2 = self.conectodoo()
        self.cursor2odoo = self.conn2.cursor()
        self.cursor2odoo.execute("DELETE FROM public.gisupdatetable_gisupdatetable CASCADE WHERE (create_uid = '"+str(user_selecc)+"')")
        #self.conn2.commit()
        #print (("EL PUERTO EN LA BASE ES ..." + str(baseObj.port)))
        print (("CARGANDO DATOS DE LA TABLA ..." ))
        self.cursor2gis = self.conect()
        #self._conectar()
        try:
            self.cursor2gis.execute("SELECT COALESCE(expediente, '-' ), COALESCE(nombre, '-' ), COALESCE(titular, '-' ), COALESCE(mineral, '-'), COALESCE(id, 0), COALESCE(estado_legal, '') FROM public."+tabla_selecc+" "\
                            "ORDER BY id ASC")
        except psycopg2.Error as e:
            #pass
            print (("ERROR EN SELECT: " + e.pgerror))
        #self.conn.commit()
        #self.conn.close()
        i = 1
        for row in self.cursor2gis.fetchall():
            #results.append(dict(zip("1", row[0], row[1], row[2])))
            print (("expte: "+ str(row[0])+ "  nombre: "+ str(row[1]) + "  titular: "+str(row[2])+ "   mineral: "+str(row[3])+ "   id: "+str(row[4]) ))
            if row[1] ==  "":
                print(("NO HAY TIPO"))
            try:
                #print ((str(i) + " - INSERTANDO EL VALOR ES: " + join(row)))
                self.cursor2odoo.execute('INSERT INTO public.gisupdatetable_gisupdatetable'\
                            '(create_uid, create_date, name, write_uid, nombre, write_date, titular, mineral, id_gis, estado_legal_actual, tabla) VALUES '\
                            '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                            (user_selecc, '2018-12-05 12:44:51.0', row[0], user_selecc, row[1], '2018-12-05 12:44:51.572921', row[2], row[3], row[4], row[5], tabla_selecc))
                #self.conn2.commit()
            except psycopg2.Error as e:
                #pass
                print (("ERROR EN INSERT: " + e.pgerror))
            i = i + 1
        #print (("TABLAS ENCONTRADAS: "+str(results)))
        self.conn2.commit()
        self.cursor2odoo.close()
        return {'value': {'encontrados_ids': False}}


tabla = sys.argv[1]
user = sys.argv[2]
u = loadtable(tabla, user)
u.loadTable()