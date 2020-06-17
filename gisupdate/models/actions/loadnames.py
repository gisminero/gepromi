# -*- coding: utf-8 -*-
import psycopg2, psycopg2.extras
import urllib2
import ConfigParser
from string import join
import os
from time import sleep

class loadtables():
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
        print ("CONECTANDO DB--...." +  nameDB + " - " +  userDB + " - " +  passDB + " - " +  hostDB)
        #self.conn = psycopg2.connect(dbname='nacion',user='postgres',password='23462', host='localhost')
        try:
            self.conn2 = psycopg2.connect(dbname=nameDB, user=userDB, password=passDB, host=hostDB)
            #self.cursor = self.conn2.cursor()
        except psycopg2.DatabaseError as e:
            #logging.info("Error de conexion con la BD local")
            print ((e.pgerror))
        return self.conn2

    def validColumnNames(self, cursor3, tablename):
        obligatory = ['id', 'expediente', 'nombre', 'titular', 'mineral', 'estado_legal']
        #"create_date", "write_date"]
        print (("VALIDANDO CAMPOS DE TABLA... "+ tablename))
        for field in obligatory:
            print (("VALIDANDO CAMPO... "+ field))
            try:
                #query = """SELECT * FROM %s WHERE %s IS NULL"""
                query = """SELECT %s FROM %s"""
                res = cursor3.execute(query % (field, tablename))
                res = True
            except (Exception, psycopg2.DatabaseError) as error:
                res = False
                print (("FALTA CAMPOS OBLIGATORIO:", field))
                break
        return res

    def validColumnNames2(self, cursor3, tablename):
        obligatory = ['id', 'expediente', 'nombre', 'titular', 'mineral', 'estado_legal']
        #A continuacion debera colocar la cantidad de campos obligatorios menos uno
        cant_obligatory = 5
        #"create_date", "create_date"]
        print (("VALIDANDO CAMPOS DE TABLA... "+ tablename))
        try:
            #query = """SELECT * FROM %s WHERE %s IS NULL"""
            query = """SELECT *
                        FROM information_schema.columns
                        WHERE table_schema = 'public'
                          AND table_name  = '%s'"""
            cursor3.execute(query % (tablename))
            #res = True
        except (Exception, psycopg2.DatabaseError) as error:
                print (("ERROR", error))
        contar_campos = 1
        res = False
        for field in self.cursor3.fetchall():
            if contar_campos > cant_obligatory:
                res = True
            if field[3] in obligatory:
                print ((" ***************CAMPOS DE LA TABLA: ", field[3], ' EN OBLIGATORIO'))
                contar_campos = contar_campos + 1
            #else:
                #print ((" ***************CAMPOS DE LA TABLA: ", field[3], ' no esta en OBLIGATORIO'))
        return res

    def loadTableNames2(self):
        #print (("Script Temporizado..."))
        sleep(7)
        results = []
        self.conn2 = self.conectodoo()
        self.cursor2odoo = self.conn2.cursor()
        self.cursor2odoo.execute('DELETE FROM public.tablesgis_tablesgis CASCADE')
        #self.conn2.commit()
        #print (("EL PUERTO EN LA BASE ES ..." + str(baseObj.port)))
        print (("CARGANDO TABLAS..." ))
        self.cursor2 = self.conect()
        self.cursor3 = self.conect()
        #self._conectar()
        try:
            self.cursor2.execute("""SELECT table_name
                                FROM information_schema.tables
                                WHERE table_schema='public' AND table_type='BASE TABLE'""" )
        except psycopg2.Error as e:
            pass
            print ((e.pgerror))
        #self.conn.commit()
        #self.conn.close()
        for row in self.cursor2.fetchall():
            results.append(dict(zip("1", row)))
            #self.env['tablesgis.tablesgis'].create({'name': str(row)})
            if self.validColumnNames2(self.cursor3, join(row)):
                try:
                    print (("DARIOINSERTANDO EL VALOR ES: " + join(row)))
                    self.cursor2odoo.execute('INSERT INTO public.tablesgis_tablesgis(create_uid, create_date, name, write_uid, cod, write_date)'\
                                ' VALUES (%s, %s, %s, %s, %s, %s)', (1, '2018-12-05 12:44:51.572921',
                                join(row), 1, join(row), '2018-12-05 12:44:51.572921'))
                except psycopg2.Error as e:
                    pass
                    print ((e.pgerror))
        #print (("TABLAS ENCONTRADAS: "+str(results)))
        self.conn2.commit()
        #self.cursor2odoo.close()
        return {'value': {'encontrados_ids': False}}

u = loadtables()
u.loadTableNames2()