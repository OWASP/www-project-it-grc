# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SetGroupsPolicyOther(models.TransientModel):
    _inherit = 'set.groups.user'

    check_project = fields.Boolean(string="Project", default=lambda x: x.get_default_menuitem(1, 'project.group_project_manager'))
    check_mailing = fields.Boolean(string="Awareness Campaign", default=lambda x: x.get_default_menuitem(1, 'mass_mailing.group_mass_mailing_user'))
    check_employee = fields.Boolean(string="Employees", default=lambda x: x.get_default_menuitem(1, 'hr.group_hr_manager'))
    check_knowledge = fields.Boolean(string="Policy", default=lambda x: x.get_default_menuitem(2, 'document_page.group_document_manager'))

    def base_values(self,name):
        user = self.env.context.get('active_id')
        category_id = self.sudo().env['ir.module.category'].search([('name','=','GRC')])
        groups = self.sudo().env['res.groups'].search([('name','=', name),('category_id','=',category_id.id)])
        return groups

    def get_default_menuitem(self, opt, group):
        user = self.env.context.get('active_id')
        user_obj = self.env['res.users'].search([('id','=',user)])
        if opt == 1:
            if user_obj.has_group(group):
                return True
            else:
                return False
        if opt == 2:
            if user_obj.has_group('document_page.group_document_manager') or \
                user_obj.has_group('document_page_approval.group_document_approver_user') or \
                user_obj.has_group('document_page.group_document_editor') or \
                user_obj.has_group('document_knowledge.group_document_user'):
                return True
            else:
                return False
            
    def assign_groups(self):
        res = super(SetGroupsPolicyOther, self).assign_groups()
        for rec in self:
            user = self.env.context.get('active_id')
            group_custom = self.sudo().env['res.groups'].search([('category_id.name','=','Documentos' if self.env.user.lang == 'es_MX' else 'Documents Knowledge')])
            data = {                
                'check_project': '',
                'check_mailing': '',
                'check_employee': '',
                # 'check_knowledge': '',
            }
            data.update({
                'check_project': rec.check_project,
                'check_mailing': rec.check_mailing,
                'check_employee': rec.check_employee,
                # 'check_knowledge': rec.check_knowledge,
            })
            if data['check_project'] == True:
                user = self.env.context.get('active_id')
                category_id = self.sudo().env['ir.module.category'].search([('name','=','Project' if self.env.user.lang == 'en_US' else 'Proyecto')])
                group_custom = self.sudo().env['res.groups'].search([('name','=', 'Administrator' if self.env.user.lang == 'en_US' else 'Administrador'),('category_id','=',category_id.id)])
                group_custom.sudo().users = [(4, user)]
            if data['check_mailing'] == True:
                user = self.env.context.get('active_id')
                category_id = self.sudo().env['ir.module.category'].search([('name','=','Email Marketing' if self.env.user.lang == 'en_US' else 'Marketing por correo electrónico')])
                group_custom = self.sudo().env['res.groups'].search([('name','=', 'User' if self.env.user.lang == 'en_US' else 'Usuario'),('category_id','=',category_id.id)])
                group_custom.sudo().users = [(4, user)]
            if data['check_employee'] == True:
                user = self.env.context.get('active_id')
                category_id = self.sudo().env['ir.module.category'].search([('name','=','Employees' if self.env.user.lang == 'en_US' else 'Empleados')])
                group_custom = self.sudo().env['res.groups'].search([('name','=', 'Administrator' if self.env.user.lang == 'en_US' else 'Administrador'),('category_id','=',category_id.id)])
                group_custom.sudo().users = [(4, user)]
        return res