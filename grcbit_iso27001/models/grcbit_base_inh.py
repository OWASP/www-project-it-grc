# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
from datetime import date
from statistics import mode

_logger = logging.getLogger(__name__)

class ResPartnerIsoInh(models.Model):
    _inherit = 'hr.employee'

    isms_roles_ids = fields.Many2many('isms.role', string=_("ISMS Role"))

class ItInventoryInh(models.Model):
    _inherit = 'it.inventory'

    responsible = fields.Many2one('hr.employee', string="IT Admin")

class DataInventoryInh(models.Model):
    _inherit = 'data.inventory'

    owner = fields.Many2one('hr.employee', string="Asset Owner")

class ResUsersIsoInh(models.Model):
    _inherit = 'res.users'

    @api.onchange('is_support')
    def onchange_is_support(self):
        for rec in self:
            data = {'is_support': None}
            data.update({
                'is_support': rec.is_support
            })
            if data['is_support'] == True:
                group_custom = self.env['res.groups'].sudo().search([('name','=','Support')])
                user = self.env.context.get('uid')
                user_id = self.sudo().env['res.users'].search([('id','=', user)])
                group_custom.users = [(4, user)]
                rec.is_support = True
            else:
                group_custom = self.env['res.groups'].sudo().search([('name','=','Support')])
                user = self.env.context.get('uid')
                group_custom.users = [(3, user)]
                rec.is_support = False