# -*- coding: utf-8 -*-
from odoo import http

# class Gisupdatetable(http.Controller):
#     @http.route('/gisupdatetable/gisupdatetable/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gisupdatetable/gisupdatetable/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gisupdatetable.listing', {
#             'root': '/gisupdatetable/gisupdatetable',
#             'objects': http.request.env['gisupdatetable.gisupdatetable'].search([]),
#         })

#     @http.route('/gisupdatetable/gisupdatetable/objects/<model("gisupdatetable.gisupdatetable"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gisupdatetable.object', {
#             'object': obj
#         })