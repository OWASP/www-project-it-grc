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
    sod_privilege_ids = fields.Many2many('sod.privilege', string="SoD Privilege")
    state = fields.Selection([
        ('draft','Draft'),
        ('approve','Approve'),
    ], string="State", default="draft")

    def action_approve(self):
        for rec in self:
            rec.state = 'approve'


class GRCSodPrivilege(models.Model):
    _name = 'sod.privilege'

    name = fields.Char(string="Name")
    active = fields.Boolean(default=True)
    description = fields.Text(string="Description")