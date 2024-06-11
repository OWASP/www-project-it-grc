# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SetGroupsOther(models.TransientModel):
    _inherit = 'set.groups.user'

    check_project = fields.Boolean(string="Project", default=lambda x: x.get_default_menuitem('grcbit_setgroups.group_show_project'))
    check_mailing = fields.Boolean(string="Awareness Campaign", default=lambda x: x.get_default_menuitem('grcbit_setgroups.group_show_mailing'))
    check_employee = fields.Boolean(string="Employees", default=lambda x: x.get_default_menuitem('grcbit_setgroups.group_show_employee'))
    check_discuss = fields.Boolean(string="Discuss", default=lambda x: x.get_default_menuitem('grcbit_setgroups.group_show_discuss'))
    check_contacts = fields.Boolean(string="Contacts", default=lambda x: x.get_default_menuitem('grcbit_setgroups.group_show_contacts'))

    def get_default_menuitem(self, group):
        user = self.env.context.get('active_id')
        user_obj = self.env['res.users'].search([('id','=',user)])
        if user_obj.has_group(group):
            return True
        else:
            return False
            
    def assign_groups(self):
        res = super(SetGroupsOther, self).assign_groups()
        for rec in self:
            user = self.env.context.get('active_id')
            category_id = self.sudo().env['ir.module.category'].search([('name','=','Menuitems')])
            data = {                
                'check_project': '',
                'check_mailing': '',
                'check_employee': '',
                'check_discuss': '',
                'check_contacts': '',
            }
            data.update({
                'check_project': rec.check_project,
                'check_mailing': rec.check_mailing,
                'check_employee': rec.check_employee,
                'check_discuss': rec.check_discuss,
                'check_contacts': rec.check_contacts,
            })
            if data['check_project'] == True:
                group_custom = self.sudo().env['res.groups'].search([('name','=', 'Project' if self.env.user.lang == 'en_US' else 'Proyecto'),('category_id','=',category_id.id)])
                group_custom.sudo().users = [(4, user)]
            else: 
                group_custom = self.sudo().env['res.groups'].search([('name','=', 'Project' if self.env.user.lang == 'en_US' else 'Proyecto'),('category_id','=',category_id.id)])
                group_custom.sudo().users = [(3, user)]
            
            if data['check_mailing'] == True:
                group_custom = self.sudo().env['res.groups'].search([('name','=', 'Awareness Campaign' if self.env.user.lang == 'en_US' else 'Campaña Concientización'),('category_id','=',category_id.id)])
                group_custom.sudo().users = [(4, user)]
            else:
                group_custom = self.sudo().env['res.groups'].search([('name','=', 'Awareness Campaign' if self.env.user.lang == 'en_US' else 'Campaña Concientización'),('category_id','=',category_id.id)])
                group_custom.sudo().users = [(3, user)]

            if data['check_employee'] == True:
                group_custom = self.sudo().env['res.groups'].search([('name','=', 'Employee' if self.env.user.lang == 'en_US' else 'Empleados'),('category_id','=',category_id.id)])
                group_custom.sudo().users = [(4, user)]
            else:
                group_custom = self.sudo().env['res.groups'].search([('name','=', 'Employee' if self.env.user.lang == 'en_US' else 'Empleados'),('category_id','=',category_id.id)])
                group_custom.sudo().users = [(3, user)]

            if data['check_discuss'] == True:
                group_custom = self.sudo().env['res.groups'].search([('name','=', 'Discuss' if self.env.user.lang == 'en_US' else 'Conversaciones'),('category_id','=',category_id.id)])
                group_custom.sudo().users = [(4, user)]
            else:
                group_custom = self.sudo().env['res.groups'].search([('name','=', 'Discuss' if self.env.user.lang == 'en_US' else 'Conversaciones'),('category_id','=',category_id.id)])
                group_custom.sudo().users = [(3, user)]

            if data['check_contacts'] == True:
                group_custom = self.sudo().env['res.groups'].search([('name','=', 'Contacts' if self.env.user.lang == 'en_US' else 'Contactos'),('category_id','=',category_id.id)])
                group_custom.sudo().users = [(4, user)]
            else:
                group_custom = self.sudo().env['res.groups'].search([('name','=', 'Contacts' if self.env.user.lang == 'en_US' else 'Contactos'),('category_id','=',category_id.id)])
                group_custom.sudo().users = [(3, user)]

        return res