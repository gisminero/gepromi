# -*- coding: utf-8 -*-
from odoo import http

# class Gisupdate(http.Controller):
#     @http.route('/gisupdate/gisupdate/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gisupdate/gisupdate/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gisupdate.listing', {
#             'root': '/gisupdate/gisupdate',
#             'objects': http.request.env['gisupdate.gisupdate'].search([]),
#         })

#     @http.route('/gisupdate/gisupdate/objects/<model("gisupdate.gisupdate"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gisupdate.object', {
#             'object': obj
#         })