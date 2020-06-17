# -*- coding: utf-8 -*-
from odoo import models, fields, api
class tablesgis(models.Model):
    _name = 'tablesgis.tablesgis'
    cod = fields.Char('Codigo')
    name = fields.Char('Nombre')

    def __init__(self, uid, cr):
        super(tablesgis, self).__init__( uid, cr)
        #self.loadTableNames()
        #print (("INICIANDO LA CLASE ..."))