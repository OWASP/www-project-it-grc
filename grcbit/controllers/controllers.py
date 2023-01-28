# -*- coding: utf-8 -*-
# from odoo import http


# class Grcbit(http.Controller):
#     @http.route('/grcbit/grcbit', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/grcbit/grcbit/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('grcbit.listing', {
#             'root': '/grcbit/grcbit',
#             'objects': http.request.env['grcbit.grcbit'].search([]),
#         })

#     @http.route('/grcbit/grcbit/objects/<model("grcbit.grcbit"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('grcbit.object', {
#             'object': obj
#         })
