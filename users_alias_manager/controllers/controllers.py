# -*- coding: utf-8 -*-
from odoo import http

# class UsersAliasManager(http.Controller):
#     @http.route('/users_alias_manager/users_alias_manager/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/users_alias_manager/users_alias_manager/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('users_alias_manager.listing', {
#             'root': '/users_alias_manager/users_alias_manager',
#             'objects': http.request.env['users_alias_manager.users_alias_manager'].search([]),
#         })

#     @http.route('/users_alias_manager/users_alias_manager/objects/<model("users_alias_manager.users_alias_manager"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('users_alias_manager.object', {
#             'object': obj
#         })