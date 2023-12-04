# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SetGroupsSeller(models.TransientModel):
    _inherit = 'set.groups.user'

    seller_admin_check = fields.Boolean(string="Admin", default=lambda x:x.get_current_groups_seller('Admin'))
    seller_user_check = fields.Boolean(string="User", default=lambda x:x.get_current_groups_seller('User'))

    def get_current_groups_seller(self, name):
        user = self.env.context.get('active_id')
        user_id = self.sudo().env['res.users'].search([('id','=', user)])
        category_id = self.sudo().env['ir.module.category'].search([('name','=','GRC Seller')])
        groups = self.sudo().env['res.groups'].search([('name','=', name),('category_id','=',category_id.id)])
        if user_id.id in [n.id for n in groups.users]:
            return True
        else:
            return False

    def base_values_seller(self,name):
        user = self.env.context.get('active_id')
        user_id = self.sudo().env['res.users'].search([('id','=', user)])
        category_id = self.sudo().env['ir.module.category'].search([('name','=','GRC Seller')])
        groups = self.sudo().env['res.groups'].search([('name','=', name),('category_id','=',category_id.id)])
        return groups

    def assign_groups(self):
        res = super(SetGroupsSeller, self).assign_groups()

        for rec in self:
            data = {
                'seller_admin_check': None,
                'seller_user_check': None,
            }
            data.update({
                'seller_admin_check': rec.seller_admin_check,
                'seller_user_check': rec.seller_user_check,
            })
            if data['seller_admin_check'] == True:
                group_custom = self.base_values_seller('Admin')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values_seller('Admin')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

            if data['seller_user_check'] == True:
                group_custom = self.base_values_seller('User')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values_seller('User')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

        return res