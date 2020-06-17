# -*- coding: utf-8 -*-
{
    'name': "GIS Update 2",

    'summary': """
        Modificar Estado Legal""",

    'description': """
        Modificar Estado Legal
    """,

    'author': "GIS Minero Nacional",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'gisupdate', 'estado_legal'],

    # always loaded
    'data': [
        'security/gisupdatetable_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}