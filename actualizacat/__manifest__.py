# -*- coding: utf-8 -*-
{
    'name': "GeProMi Actualiza Catastro",

    'summary': """
        Actualización del Registro Catastral Minero Provincial""",

    'description': """
        Actualización del Registro Catastral Minero Provincial
    """,

    'author': "Gis Minero Nacional",
    'website': "http://www.gismineronacional.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'expediente'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        # La siguiente linea habilita el proceso que actualiza cada cierto tiempo, Se desactiva por desarrollo
        # 'data/auto_server.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}