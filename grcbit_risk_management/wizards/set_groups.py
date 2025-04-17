# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SetGroupsZt(models.TransientModel):
    _inherit = 'set.groups.user'

    control_draft  = fields.Boolean(string="Draft", default=lambda x:x.get_current_groups_control('grcbit_risk_management.group_control_draft'))
    control_design  = fields.Boolean(string="Design", default=lambda x:x.get_current_groups_control('grcbit_risk_management.group_control_design'))
    control_implementation  = fields.Boolean(string="Assess", default=lambda x:x.get_current_groups_control('grcbit_risk_management.group_control_implementation'))
    control_approval   = fields.Boolean(string="Implement", default=lambda x:x.get_current_groups_control('grcbit_risk_management.group_control_approval'))
    control_reject   = fields.Boolean(string="Reject", default=lambda x:x.get_current_groups_control('grcbit_risk_management.group_control_reject'))
    control_design_evaluation = fields.Boolean(string="Design Assessment", default=lambda x:x.get_current_groups_control('grcbit_risk_management.group_control_design_evaluation') )
    control_effectiveness_evaluation = fields.Boolean(string="Effectiveness Assessment", default=lambda x:x.get_current_groups_control('grcbit_risk_management.group_control_effectiveness_evaluation') )
    control_setdraft = fields.Boolean(string="Set to draft", default=lambda x:x.get_current_groups_control('grcbit_risk_management.group_control_setdraft') )
   
    def get_current_groups_control(self, xml_id):
        user = self.env.context.get('active_id')
        user_id = self.sudo().env['res.users'].search([('id','=', user)])
        groups = self.env.ref(xml_id).sudo()
        if user_id.id in [n.id for n in groups.users]:
            return True
        else:
            return False

    def base_values_control(self,xml_id):
        user = self.env.context.get('active_id')
        user_id = self.sudo().env['res.users'].search([('id','=', user)])
        groups = self.env.ref(xml_id).sudo()
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
                'control_setdraft': None,
            }
            data.update({
                'control_draft' : rec.control_draft,
                'control_design' : rec.control_design,
                'control_implementation' : rec.control_implementation,
                'control_approval' : rec.control_approval,
                'control_reject' : rec.control_reject,
                'control_design_evaluation' : rec.control_design_evaluation,
                'control_effectiveness_evaluation' : rec.control_effectiveness_evaluation,
                'control_setdraft': rec.control_setdraft,
            })
            if data['control_draft'] == True:
                group_custom = self.base_values_control('grcbit_risk_management.group_control_draft')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values_control('grcbit_risk_management.group_control_draft')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

            if data['control_design'] == True:
                group_custom = self.base_values_control('grcbit_risk_management.group_control_design')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values_control('grcbit_risk_management.group_control_design')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

            if data['control_implementation'] == True:
                group_custom = self.base_values_control('grcbit_risk_management.group_control_implementation')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values_control('grcbit_risk_management.group_control_implementation')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

            if data['control_approval'] == True:
                group_custom = self.base_values_control('grcbit_risk_management.group_control_approval')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values_control('grcbit_risk_management.group_control_approval')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

            if data['control_reject'] == True:
                group_custom = self.base_values_control('grcbit_risk_management.group_control_reject')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values_control('grcbit_risk_management.group_control_reject')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

            if data['control_design_evaluation'] == True:
                group_custom = self.base_values_control('grcbit_risk_management.group_control_design_evaluation')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values_control('grcbit_risk_management.group_control_design_evaluation')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

            if data['control_effectiveness_evaluation'] == True:
                group_custom = self.base_values_control('grcbit_risk_management.group_control_effectiveness_evaluation')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values_control('grcbit_risk_management.group_control_effectiveness_evaluation')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

            if data['control_setdraft'] == True:
                group_custom = self.base_values_control('grcbit_risk_management.group_control_setdraft')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values_control('grcbit_risk_management.group_control_setdraft')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

        return res
