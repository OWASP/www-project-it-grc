# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
import random as r
from datetime import date
from statistics import mode
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class ItComponents(models.Model):
    _name ='it.components'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name")
    description = fields.Html(string="Description")
    color = fields.Integer(string="Color", default=lambda x: x.default_color())

    _sql_constraints = [
        ('unique_name','unique(name)','IT Component name already exist.!')]

    def default_color(self):
        x = r.randrange(11)
        if x <= 11 or x > 0:
            return x
        
    @api.model
    def create(self, vals):
        res = super(ItComponents, self).create(vals)
        components = self.env['it.components'].search([('id','!=', res.id)])
        if components:
            if vals['name'] in [x.name for x in components]:
                raise ValidationError("IT Component name already exist.!")
        return res

class TCPPorts(models.Model):
    _name = 'tcp.ports'

    name = fields.Char(string="Name")
    # it_inventory_id = fields.Many2one('it.inventory', string="IT Components")
    color = fields.Integer(string="Color", default=lambda x: x.default_color())

    _sql_constraints = [
        ('unique_name','unique(name)','TCP Port name already exist.!')]

    def default_color(self):
        x = r.randrange(11)
        if x <= 11 or x > 0:
            return x
        
    @api.model
    def create(self, vals):
        res = super(TCPPorts, self).create(vals)
        tcp_port = self.env['tcp.ports'].search([('id','!=', res.id)])
        if tcp_port:
            if vals['name'] in [x.name for x in tcp_port]:
                raise ValidationError("TCP Port name already exist.!")
        return res
    