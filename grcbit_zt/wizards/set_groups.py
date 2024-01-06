# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SetGroupsZt(models.TransientModel):
    _inherit = 'set.groups.user'

    zt_admin_check = fields.Boolean(string="Admin", default=lambda x:x.get_current_groups_zt('Admin' if x.user_id.tz == 'en_US' else 'Administrador'))
    zt_user_check = fields.Boolean(string="User", default=lambda x:x.get_current_groups_zt('User' if x.user_id.tz == 'en_US' else 'Usuario'))
    zt_guest_check = fields.Boolean(string="Guest", default=lambda x:x.get_current_groups_zt('Guest' if x.user_id.tz == 'en_US' else 'Invitado'))

    def get_current_groups_zt(self, name):
        user = self.env.context.get('active_id')
        user_id = self.sudo().env['res.users'].search([('id','=', user)])
        category_id = self.sudo().env['ir.module.category'].search([('name','=','ZT'),('parent_id','!=',None)])
        groups = self.sudo().env['res.groups'].search([('name','=', name),('category_id','=',category_id.id)])
        if user_id.id in [n.id for n in groups.users]:
            return True
        else:
            return False

    def base_values_zt(self,name):
        user = self.env.context.get('active_id')
        user_id = self.sudo().env['res.users'].search([('id','=', user)])
        category_id = self.sudo().env['ir.module.category'].search([('name','=','ZT'),('parent_id','!=',None)])
        groups = self.sudo().env['res.groups'].search([('name','=', name),('category_id','=',category_id.id)])
        return groups

    def assign_groups(self):
        res = super(SetGroupsZt, self).assign_groups()

        for rec in self:
            data = {
                'zt_admin_check': None,
                'zt_user_check': None,
                'zt_guest_check': None,
            }
            data.update({
                'zt_admin_check': rec.zt_admin_check,
                'zt_user_check': rec.zt_user_check,
                'zt_guest_check': rec.zt_guest_check,
            })
            if data['zt_admin_check'] == True:
                group_custom = self.base_values_zt('Admin' if self.user_id.tz == 'en_US' else 'Administrador')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values_zt('Admin' if self.user_id.tz == 'en_US' else 'Administrador')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

            if data['zt_user_check'] == True:
                group_custom = self.base_values_zt('User' if self.user_id.tz == 'en_US' else 'Usuario')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values_zt('User' if self.user_id.tz == 'en_US' else 'Usuario')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

            if data['zt_guest_check'] == True:
                group_custom = self.base_values_zt('Guest' if self.user_id.tz == 'en_US' else 'Invitado')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values_zt('Guest' if self.user_id.tz == 'en_US' else 'Invitado')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

        return res