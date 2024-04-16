# -*- coding: utf-8 -*-
# from odoo import http


# class ChatgptBlog(http.Controller):
#     @http.route('/chatgpt_blog/chatgpt_blog', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/chatgpt_blog/chatgpt_blog/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('chatgpt_blog.listing', {
#             'root': '/chatgpt_blog/chatgpt_blog',
#             'objects': http.request.env['chatgpt_blog.chatgpt_blog'].search([]),
#         })

#     @http.route('/chatgpt_blog/chatgpt_blog/objects/<model("chatgpt_blog.chatgpt_blog"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('chatgpt_blog.object', {
#             'object': obj
#         })
