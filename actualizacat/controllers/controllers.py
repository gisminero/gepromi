# -*- coding: utf-8 -*-
from odoo import http

# class Actualizacat(http.Controller):
#     @http.route('/actualizacat/actualizacat/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/actualizacat/actualizacat/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('actualizacat.listing', {
#             'root': '/actualizacat/actualizacat',
#             'objects': http.request.env['actualizacat.actualizacat'].search([]),
#         })

#     @http.route('/actualizacat/actualizacat/objects/<model("actualizacat.actualizacat"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('actualizacat.object', {
#             'object': obj
#         })