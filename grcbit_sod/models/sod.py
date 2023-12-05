# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _
_logger = logging.getLogger(__name__)

class GRCSodRole(models.Model):
    _name = 'sod.role'

    name = fields.Char(string="Name")
    active = fields.Boolean(default=True)
    description = fields.Text(string="Description")
    it_inventory_id = fields.Many2one('it.inventory' , string="IT System")
    sod_privilege_ids = fields.One2many('sod.privilege', 'sod_role_id', string="SoD Privilege")
    user_id = fields.Many2one('res.users', string="Responsible")
    state = fields.Selection([
        ('draft','Draft'),
        ('approve','Approve'),
    ], string="State", default="draft")

    def action_approve(self):
        for rec in self:
            rec.state = 'approve'
    
    def action_draft(self):
        for rec in self:
            rec.state = 'draft'


class GRCSodPrivilege(models.Model):
    _name = 'sod.privilege'

    name = fields.Char(string="Name")
    active = fields.Boolean(default=True)
    description = fields.Text(string="Description")
    sod_role_id = fields.Many2one('sod.role', string="SoD Role")
    is_grc_admin = fields.Boolean(string="is admin", compute="_get_group")

    @api.onchange('name')
    def _onchange_is_admin_new(self):
        for rec in self:
            flag = self.env.user.has_group('grcbit_base.group_grc_admin')
            rec.is_grc_admin = flag

    def _get_group(self):
        for rec in self:
            flag = self.env.user.has_group('grcbit_base.group_grc_admin')
            rec.is_grc_admin = flag