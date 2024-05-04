# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SetGroupsPolicy(models.TransientModel):
    _inherit = 'set.groups.user'

    permissions = fields.Selection([
        ('knowledge','Knowledge'),
        ('editor','Editor'),
        ('approver','Approver'),
        ('responsible','Responsible')
        ],string="Permissions", default=lambda x:x.get_current_group_policy())
    
    check_approver = fields.Boolean(string="Approver")

    def get_current_group_policy(self):
        user = self.env.context.get('active_id')
        user_id = self.sudo().env['res.users'].search([('id','=', user)])
        flag = 0
        if user_id.has_group('document_knowledge.group_document_user'):
            flag = 1 
            if user_id.has_group('document_page.group_document_editor'):
                flag = 2
                if user_id.has_group('document_page_approval.group_document_approver_user'):
                    flag = 3
                    if user_id.has_group('document_page.group_document_manager'):
                        flag = 4
        if flag == 0:
            return ''
        elif flag == 1:
            return 'knowledge'
        elif flag == 2:
            return 'editor'
        elif flag == 3:
            return 'approver'
        elif flag == 4:
            return 'responsible'
            

    def assign_groups(self):
        res = super(SetGroupsPolicy, self).assign_groups()

        for rec in self:
            user = self.env.context.get('active_id')
            group_custom = self.env['res.groups'].search([('category_id.name','=','Documentos' if self.env.user.lang == 'es_MX' else 'Documents Knowledge')])
            data = {'permissions': ''}
            data.update({
                'permissions': rec.permissions
            })
            if data['permissions'] == 'responsible':
                for l in group_custom:
                    l.users = [(4, user)]

            elif data['permissions'] == 'approver':
                for s in group_custom.filtered(lambda s: s.name == 'Aprobador' if self.env.user.lang == 'es_MX' else 'Approver'):
                    s.users = [(4, user)]
                for l in group_custom.filtered(lambda s: s.name == 'Responsable' if self.env.user.lang == 'es_MX' else 'Manager'):
                    l.users = [(3, user)]
                
            elif data['permissions'] == 'editor':
                for s in group_custom.filtered(lambda s: s.name == 'Editor' if self.env.user.lang == 'es_MX' else 'Editor'):
                    s.users = [(4, user)]
                for l in group_custom.filtered(lambda s: s.name == 'Aprobador' if self.env.user.lang == 'es_MX' else 'Approver'):
                    l.users = [(3, user)]
                for l in group_custom.filtered(lambda s: s.name == 'Responsable' if self.env.user.lang == 'es_MX' else 'Manager'):
                    l.users = [(3, user)]

            elif data['permissions'] == 'knowledge':
                for s in group_custom.filtered(lambda s: s.name == 'Conocimiento' if self.env.user.lang == 'es_MX' else 'Document Knowledge user'):
                    s.users = [(4, user)]
                for l in group_custom.filtered(lambda s: s.name == 'Editor' if self.env.user.lang == 'es_MX' else 'Editor'):
                    l.users = [(3, user)]
                for l in group_custom.filtered(lambda s: s.name == 'Aprobador' if self.env.user.lang == 'es_MX' else 'Approver'):
                    l.users = [(3, user)]
                for l in group_custom.filtered(lambda s: s.name == 'Responsable' if self.env.user.lang == 'es_MX' else 'Manager'):
                    l.users = [(3, user)]

            elif data['permissions'] == False:
                for l in group_custom:
                    l.users = [(3, user)]
        return res