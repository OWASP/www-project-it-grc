# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SetGroupsZt(models.TransientModel):
    _inherit = 'set.groups.user'

    xdr_admin_check = fields.Boolean(string="Admin", default=lambda x:x.get_current_groups_xdr('Admin' if x.user_id.tz == 'en_US' else 'Administrador'))
    xdr_user_check = fields.Boolean(string="User", default=lambda x:x.get_current_groups_xdr('User' if x.user_id.tz == 'en_US' else 'Usuario'))
    xdr_guest_check = fields.Boolean(string="Guest", default=lambda x:x.get_current_groups_xdr('Guest' if x.user_id.tz == 'en_US' else 'Invitado'))

    def get_current_groups_xdr(self, name):
        user = self.env.context.get('active_id')
        user_id = self.sudo().env['res.users'].search([('id','=', user)])
        category_id = self.sudo().env['ir.module.category'].search([('name','=','XDR'),('parent_id','!=',None)])
        groups = self.sudo().env['res.groups'].search([('name','=', name),('category_id','=',category_id.id)])
        if user_id.id in [n.id for n in groups.users]:
            return True
        else:
            return False

    def base_values_xdr(self,name):
        user = self.env.context.get('active_id')
        user_id = self.sudo().env['res.users'].search([('id','=', user)])
        category_id = self.sudo().env['ir.module.category'].search([('name','=','XDR'),('parent_id','!=',None)])
        groups = self.sudo().env['res.groups'].search([('name','=', name),('category_id','=',category_id.id)])
        return groups

    def assign_groups(self):
        res = super(SetGroupsZt, self).assign_groups()

        for rec in self:
            data = {
                'xdr_admin_check': None,
                'xdr_user_check': None,
                'xdr_guest_check': None,
            }
            data.update({
                'xdr_admin_check': rec.xdr_admin_check,
                'xdr_user_check': rec.xdr_user_check,
                'xdr_guest_check': rec.xdr_guest_check,
            })
            if data['xdr_admin_check'] == True:
                group_custom = self.base_values_xdr('Admin' if self.user_id.tz == 'en_US' else 'Administrador')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values_xdr('Admin' if self.user_id.tz == 'en_US' else 'Administrador')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

            if data['xdr_user_check'] == True:
                group_custom = self.base_values_xdr('User' if self.user_id.tz == 'en_US' else 'Usuario')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values_xdr('User' if self.user_id.tz == 'en_US' else 'Usuario')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

            if data['xdr_guest_check'] == True:
                group_custom = self.base_values_xdr('Guest' if self.user_id.tz == 'en_US' else 'Invitado')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values_xdr('Guest' if self.user_id.tz == 'en_US' else 'Invitado')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

        return res