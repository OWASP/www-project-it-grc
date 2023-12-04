# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SetGroupsSod(models.TransientModel):
    _inherit = 'set.groups.user'

    sod_check = fields.Boolean(string="SoD", default=lambda x:x.get_current_groups_sod('SoD'))

    def get_current_groups_sod(self, name):
        user = self.env.context.get('active_id')
        user_id = self.sudo().env['res.users'].search([('id','=', user)])
        category_id = self.sudo().env['ir.module.category'].search([('name','=','GRC')])
        groups = self.sudo().env['res.groups'].search([('name','=', name),('category_id','=',category_id.id)])
        if user_id.id in [n.id for n in groups.users]:
            return True
        else:
            return False

    def assign_groups(self):
        res = super(SetGroupsSod, self).assign_groups()

        for rec in self:
            data = {'sod_check': None}
            data.update({
                'sod_check': rec.sod_check
            })
            if data['sod_check'] == True:
                group_custom = self.env['set.groups.user'].base_values('SoD')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.env['set.groups.user'].base_values('SoD')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

        return res