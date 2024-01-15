# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SetGroupsZt(models.TransientModel):
    _inherit = 'set.groups.user'

    control_draft  = fields.Boolean(string="Draft", default=lambda x:x.get_current_groups_control('Draft' if x.env.user.lang == 'en_US' else 'Borrador'))
    control_design  = fields.Boolean(string="Design", default=lambda x:x.get_current_groups_control('Design' if x.env.user.lang == 'en_US' else 'Diseño'))
    control_implementation  = fields.Boolean(string="Implementation", default=lambda x:x.get_current_groups_control('Implementation' if x.env.user.lang == 'en_US' else 'Implementación'))
    control_approval   = fields.Boolean(string="Approval", default=lambda x:x.get_current_groups_control('Approval' if x.env.user.lang == 'en_US' else 'Aprobación'))
    control_reject   = fields.Boolean(string="Reject", default=lambda x:x.get_current_groups_control('Reject' if x.env.user.lang == 'en_US' else 'Rechazar'))
    control_design_evaluation = fields.Boolean(string="Design Evaluation", default=lambda x:x.get_current_groups_control('Design Evaluation' if x.env.user.lang == 'en_US' else 'Evaluación de diseño') )
    control_effectiveness_evaluation = fields.Boolean(string="Effectiveness Evaluation", default=lambda x:x.get_current_groups_control('Effectiveness Evaluation' if x.env.user.lang == 'en_US' else 'Evaluación de eficacia') )
    

    def get_current_groups_control(self, name):
        user = self.env.context.get('active_id')
        user_id = self.sudo().env['res.users'].search([('id','=', user)])
        category_id = self.sudo().env['ir.module.category'].search([('name','=','Control')])
        groups = self.sudo().env['res.groups'].search([('name','=', name),('category_id','=',category_id.id)])
        if user_id.id in [n.id for n in groups.users]:
            return True
        else:
            return False

    def base_values_control(self,name):
        user = self.env.context.get('active_id')
        user_id = self.sudo().env['res.users'].search([('id','=', user)])
        category_id = self.sudo().env['ir.module.category'].search([('name','=','Control')])
        groups = self.sudo().env['res.groups'].search([('name','=', name),('category_id','=',category_id.id)])
        return groups

    def assign_groups(self):
        res = super(SetGroupsZt, self).assign_groups()

        for rec in self:
            data = {
                'control_draft' : None,
                'control_design' : None,
                'control_implementation' : None,
                'control_approval' : None,
                'control_reject' : None,
                'control_design_evaluation': None,
                'control_effectiveness_evaluation': None,
            }
            data.update({
                'control_draft' : rec.control_draft,
                'control_design' : rec.control_design,
                'control_implementation' : rec.control_implementation,
                'control_approval' : rec.control_approval,
                'control_reject' : rec.control_reject,
                'control_design_evaluation' : rec.control_design_evaluation,
                'control_effectiveness_evaluation' : rec.control_effectiveness_evaluation,
            })
            if data['control_draft'] == True:
                group_custom = self.base_values_control('Draft' if self.env.user.lang == 'en_US' else 'Borrador')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values_control('Draft' if self.env.user.lang == 'en_US' else 'Borrador')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

            if data['control_design'] == True:
                group_custom = self.base_values_control('Design' if self.env.user.lang == 'en_US' else 'Diseño')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values_control('Design' if self.env.user.lang == 'en_US' else 'Diseño')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

            if data['control_implementation'] == True:
                group_custom = self.base_values_control('Implementation' if self.env.user.lang == 'en_US' else 'Implementación')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values_control('Implementation' if self.env.user.lang == 'en_US' else 'Implementación')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

            if data['control_approval'] == True:
                group_custom = self.base_values_control('Approval' if self.env.user.lang == 'en_US' else 'Aprobación')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values_control('Approval' if self.env.user.lang == 'en_US' else 'Aprobación')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

            if data['control_reject'] == True:
                group_custom = self.base_values_control('Reject' if self.env.user.lang == 'en_US' else 'Rechazar')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values_control('Reject' if self.env.user.lang == 'en_US' else 'Rechazar')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

            if data['control_design_evaluation'] == True:
                group_custom = self.base_values_control('Design Evaluation' if self.env.user.lang == 'en_US' else 'Evaluación de diseño')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values_control('Design Evaluation' if self.env.user.lang == 'en_US' else 'Evaluación de diseño')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

            if data['control_effectiveness_evaluation'] == True:
                group_custom = self.base_values_control('Effectiveness Evaluation' if self.env.user.lang == 'en_US' else 'Evaluación de eficacia')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values_control('Effectiveness Evaluation' if self.env.user.lang == 'en_US' else 'Evaluación de eficacia')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

        return res