# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SetGroupsPolicy(models.TransientModel):
    _inherit = 'set.groups.user'

    approval_check = fields.Boolean(string="Approval", default=lambda x:x.get_current_group_policy())

    def get_current_group_policy(self):
        user = self.env.context.get('active_id')
        user_id = self.sudo().env['res.users'].search([('id','=', user)])
        if user_id.has_group('document_page_approval.group_document_approver_user'):
            return True
        else:
            return False

    def assign_groups(self):
        res = super(SetGroupsPolicy, self).assign_groups()

        for rec in self:
            data = {'approval_check': None}
            data.update({
                'approval_check': rec.approval_check
            })
            if data['approval_check'] == True:
                group_custom = self.env['set.groups.user'].base_values('approval_check')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.env['set.groups.user'].base_values('approval_check')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

        return res