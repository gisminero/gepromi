# -*- coding: utf-8 -*-
{
    'name': "GIS Update 1",

    'summary': """
        Actualizar datos del Registro Catstral Minero""",

    'description': """
        Actualizar datos del Registro Catstral Minero
    """,

    'author': "GIS Minero Nacional",
    'website': "http://www.gismineronacional.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'estado_legal'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        #'security/gisupdate_security.xml',
        #'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'auto_install': True,
}