# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _
_logger = logging.getLogger(__name__)
class SetGroupsUser(models.TransientModel):
    _name = 'set.groups.user'

    user_id = fields.Many2one('res.users', string="User")
    grc_admin_check = fields.Boolean(string="GRC Admin", default= lambda x: x.get_current_groups('GRC Admin'))
    grc_consultant_check = fields.Boolean(string="GRC Consultant", default= lambda x: x.get_current_groups('GRC Consultant'))
    asset_management_check = fields.Boolean(string="Asset Management", default= lambda x: x.get_current_groups('Asset Management'))
    risk_management_check = fields.Boolean(string="Risk Management", default= lambda x: x.get_current_groups('Risk Management'))
    control_check = fields.Boolean(string="Control", default= lambda x: x.get_current_groups('Control'))
    isms_check = fields.Boolean(string="ISMS", default= lambda x: x.get_current_groups('ISMS'))
    compliance_check = fields.Boolean(string="Compliance", default= lambda x: x.get_current_groups('Compliance'))
    guest_check = fields.Boolean(string="Guest", default= lambda x: x.get_current_groups('Guest'))

    def get_current_groups(self, name):
        user = self.env.context.get('active_id')
        user_id = self.sudo().env['res.users'].search([('id','=', user)])
        category_id = self.sudo().env['ir.module.category'].search([('name','=','GRC')])
        groups = self.sudo().env['res.groups'].search([('name','=', name),('category_id','=',category_id.id)])
        if user_id.id in [n.id for n in groups.users]:
            return True
        else:
            return False

    def base_values(self,name):
        user = self.env.context.get('active_id')
        user_id = self.sudo().env['res.users'].search([('id','=', user)])
        category_id = self.sudo().env['ir.module.category'].search([('name','=','GRC')])
        groups = self.sudo().env['res.groups'].search([('name','=', name),('category_id','=',category_id.id)])
        return groups

    def assign_groups(self):
        data={
            'grc_admin_check':None,
            'grc_consultant_check':None,
            'asset_management_check':None,
            'risk_management_check':None,
            'control_check':None,
            'isms_check':None,
            'compliance_check':None,
            'guest_check':None,
        }
        for rec in self:
            data.update({
                'grc_admin_check'        : rec.grc_admin_check,
                'grc_consultant_check'   : rec.grc_consultant_check,
                'asset_management_check' : rec.asset_management_check,
                'risk_management_check'  : rec.risk_management_check,
                'control_check'          : rec.control_check,
                'isms_check'             : rec.isms_check,
                'compliance_check'       : rec.compliance_check,
                'guest_check'            : rec.guest_check,
            })
            if data['grc_admin_check'] == True:
                group_custom = self.base_values('GRC Admin')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values('GRC Admin')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]
            
            if data['grc_consultant_check'] == True:
                group_custom = self.base_values('GRC Consultant')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values('GRC Consultant')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

            if data['asset_management_check'] == True:
                group_custom = self.base_values('Asset Management')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values('Asset Management')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

            if data['risk_management_check'] == True:
                group_custom = self.base_values('Risk Management')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values('Risk Management')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

            if data['control_check'] == True:
                group_custom = self.base_values('Control')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values('Control')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

            if data['isms_check'] == True:
                group_custom = self.base_values('ISMS')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values('ISMS')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

            if data['compliance_check'] == True:
                group_custom = self.base_values('Compliance')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values('Compliance')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]

            if data['guest_check'] == True:
                group_custom = self.base_values('Guest')
                user = self.env.context.get('active_id')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
            else:
                group_custom = self.base_values('Guest')
                user = self.env.context.get('active_id')
                group_custom.users = [(3, user)]