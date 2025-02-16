# -*- coding: utf-8 -*-
# from odoo import http


# class GrcbitGpt(http.Controller):
#     @http.route('/grcbit_gpt/grcbit_gpt', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/grcbit_gpt/grcbit_gpt/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('grcbit_gpt.listing', {
#             'root': '/grcbit_gpt/grcbit_gpt',
#             'objects': http.request.env['grcbit_gpt.grcbit_gpt'].search([]),
#         })

#     @http.route('/grcbit_gpt/grcbit_gpt/objects/<model("grcbit_gpt.grcbit_gpt"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('grcbit_gpt.object', {
#             'object': obj
#         })
