# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class DocumentPageInh(models.Model):
    _inherit = 'document.page'

    approver_gid = fields.Many2one(default=lambda x: x.get_approver_group())

    def get_approver_group(self):
        user = self.env.context.get('active_id')
        category_id = self.sudo().env['ir.module.category'].search([('name','=','GRC')])
        groups = self.sudo().env['res.groups'].search([('name','=', 'Policy Approver'),('category_id','=',category_id.id)])
        return groups.id