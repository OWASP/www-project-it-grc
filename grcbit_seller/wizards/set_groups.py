# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SetGroupsSeller(models.TransientModel):
    _inherit = 'set.groups.user'

    seller_admin_check = fields.Boolean(string="grc4ciso Admin", default=lambda x:x.get_current_groups_seller('grcbit_seller.group_admin_seller'))
    seller_consultor_check = fields.Boolean(string="grc4ciso Consultor", default=lambda x:x.get_current_groups_seller('grcbit_seller.group_consultor_seller'))
    seller_user_check = fields.Boolean(string="grc4ciso User", default=lambda x:x.get_current_groups_seller('grcbit_seller.group_user_seller'))

    def get_current_groups_seller(self, name):
        user = self.env.context.get('active_id')
        user_id = self.sudo().env['res.users'].search([('id','=', user)])
        if user_id.has_group(name):
            return True
        else:
            return False

    def base_values_seller(self,name):
        user = self.env.context.get('active_id')
        user_id = self.sudo().env['res.users'].search([('id','=', user)])
        if self.env.user.lang == 'en_US':
            lang = 'GRC Seller'
        else: 
            lang = 'Vendedor GRC'
        category_id = self.sudo().env['ir.module.category'].search([('name','=', lang)])
        groups = self.sudo().env['res.groups'].search([('name','=', name),('category_id','=',category_id.id)])
        return groups

    def assign_groups(self):
        res = super(SetGroupsSeller, self).assign_groups()

        for rec in self:
            user = self.env.context.get('active_id')
            user_id = self.sudo().env['res.users'].search([('id','=', user)])
            data = {
                'seller_admin_check': None,
                'seller_consultor_check': None,
                'seller_user_check': None,
            }
            data.update({
                'seller_admin_check': rec.seller_admin_check,
                'seller_consultor_check': rec.seller_consultor_check,
                'seller_user_check': rec.seller_user_check,
            })
            if data['seller_admin_check'] == True:
                if not user_id.has_group('grcbit_seller.group_admin_seller'):
                    group_custom = self.base_values_seller('grc4ciso Admin' if self.env.user.lang == 'en_US' else 'Administrador grc4ciso')
                    group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values_seller('grc4ciso Admin' if self.env.user.lang == 'en_US' else 'Administrador grc4ciso')
                group_custom.users = [(3, user)]

            if data['seller_consultor_check'] == True:
                if not user_id.has_group('grcbit_seller.group_consultor_seller'):
                    group_custom = self.base_values_seller('grc4ciso Consultor' if self.env.user.lang == 'en_US' else 'Consultor grc4ciso')
                    group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values_seller('grc4ciso Consultor' if self.env.user.lang == 'en_US' else 'Consultor grc4ciso')
                group_custom.users = [(3, user)]

            if data['seller_user_check'] == True:
                if not user_id.has_group('grcbit_seller.group_user_seller'):
                    group_custom = self.base_values_seller('grc4ciso User' if self.env.user.lang == 'en_US' else 'Usuario grc4ciso')
                    group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values_seller('grc4ciso User' if self.env.user.lang == 'en_US' else 'Usuario grc4ciso')
                group_custom.users = [(3, user)]



        return res