# -*- coding: utf-8 -*-
import psycopg2, psycopg2.extras
import urllib2
import ConfigParser
from string import join
import os
import sys

class changestate():
    def __init__(self, estado_arg, id_arg, tabla):
        print (("LA TABLA ES ESTADO - ID : ", str(estado_arg), str(id_arg)))
        self._state_name = estado_arg
        self._id_reg = id_arg
        self._tabla = tabla
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
        #
        try:
            self.conn = psycopg2.connect(dbname=nameDB,user=userDB,password=passDB, host=hostDB)
        except psycopg2.DatabaseError as e:
            print (("Error de conexion con la BD local"))
            print ((e.pgerror))
        return self.conn

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
        try:
            conn2 = psycopg2.connect(dbname=nameDB, user=userDB, password=passDB, host=hostDB)
            #self.cursor = self.conn2.cursor()
        except psycopg2.DatabaseError as e:
            #logging.info("Error de conexion con la BD local")
            print ((e.pgerror))
        return conn2

    def changeState(self):
        print (("LA VARIABLE DENTRO DE FUNCION ES: "+ str(self._state_name)))
        print (("el ID DEL REGISTRO A MODIFICAR ES: "+ str(self._id_reg)))
        print (("TABLA A MODIFICAR ES: "+ str(self._tabla)))
        state_selec = self._state_name
        id_selec = self._id_reg
        tabla_selec = 'public.' + self._tabla
        print (("CARGANDO DATOS DE LA TABLA ..." ))
        self.conn = self.conect()
        self.cursor2gis = self.conn.cursor()
        #self._conectar()
        try:
            query = "UPDATE "+tabla_selec+" SET estado_legal = '" + state_selec+ "' WHERE id = " + str(id_selec)
            print (("CONSULTA: " + query))
            self.cursor2gis.execute(query)
        except psycopg2.Error as e:
            pass
            print ((e.pgerror))
        #self.conn.commit()
        #self.conn.close()
        self.conn.commit()
        self.conn.close()
        return {'value': {'encontrados_ids': False}}


estado = sys.argv[1]
id_reg = sys.argv[2]
tabla = sys.argv[3]
u = changestate(estado, id_reg, tabla)
u.changeState()