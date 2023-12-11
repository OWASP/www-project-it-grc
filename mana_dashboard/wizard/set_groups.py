# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SetGroupsSod(models.TransientModel):
    _inherit = 'set.groups.user'

    dash_admin_check = fields.Boolean(string="Dasboard Admin", default=lambda x:x.get_current_groups_dash('dashboard manager'))

    def base_values_dash(self,name):
        user = self.env.context.get('active_id')
        user_id = self.sudo().env['res.users'].search([('id','=', user)])
        category_id = self.sudo().env['ir.module.category'].search([('name','=','mana dashboard')])
        groups = self.sudo().env['res.groups'].search([('name','=', name),('category_id','=',category_id.id)])
        return groups

    def get_current_groups_dash(self, name):
        user = self.env.context.get('active_id')
        user_id = self.sudo().env['res.users'].search([('id','=', user)])
        category_id = self.sudo().env['ir.module.category'].search([('name','=','mana dashboard')])
        groups = self.sudo().env['res.groups'].search([('name','=', name),('category_id','=',category_id.id)])
        if user_id.id in [n.id for n in groups.users]:
            return True
        else:
            return False

    def assign_groups(self):
        res = super(SetGroupsSod, self).assign_groups()

        for rec in self:
            data = {'dash_admin_check': None}
            data.update({
                'dash_admin_check': rec.dash_admin_check
            })
            if data['dash_admin_check'] == True:
                group_custom = self.env['set.groups.user'].base_values_dash('dashboard manager')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.env['set.groups.user'].base_values_dash('dashboard manager')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

        return res