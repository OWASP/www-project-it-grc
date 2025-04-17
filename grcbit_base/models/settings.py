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

    name = fields.Char(string="Name", track_visibility='onchange')
    description = fields.Text(string="Description", track_visibility='onchange')
    it_inventory_count = fields.Integer(string="IT Inventory Count")
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('unique_name','unique(name)','IT Component name already exist.!')]

    #@api.model
    #def create(self, vals):
    #    res = super(ItComponents, self).create(vals)
    #    components = self.env['it.components'].search([('id','!=', res.id)])
    #    if components:
    #        if vals['name'] in [x.name for x in components]:
    #            raise ValidationError("IT Component name already exist.!")
    #    return res
    
    @api.model
    def web_read_group(self, domain, fields, groupby, limit=None, offset=0, orderby=False,lazy=True, expand=False, expand_limit=None, expand_orderby=False):
        res = super().web_read_group(domain, fields, groupby, limit, offset, orderby, lazy, expand, expand_limit, expand_orderby)
        for i in self.env['it.components'].search([]):
            data_assets = self.env['it.inventory.it.component'].search([('it_component_id', 'in', [i.id] )])
            self.env['it.components'].sudo().search([('id','=',i.id)]).sudo().write({'it_inventory_count':len(data_assets)})
        return res

class TCPPorts(models.Model):
    _name = 'tcp.ports'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name", track_visibility='onchange')
    #it_inventory_ids = fields.Many2many('it.inventory', 'it_inventory_tcp_ports_rel', 'tcp_ports_id', 'it_inventory_id', string="It system")
    description = fields.Text(string="Description", track_visibility='onchange')
    it_inventory_count = fields.Integer(string="IT Inventory Count")
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('unique_name','unique(name)','TCP Port name already exist.!')]

    #@api.model
    #def create(self, vals):
    #    res = super(TCPPorts, self).create(vals)
    #    tcp_port = self.env['tcp.ports'].search([('id','!=', res.id)])
    #    if tcp_port:
    #        if vals['name'] in [x.name for x in tcp_port]:
    #            raise ValidationError("TCP Port name already exist.!")
    #    return res
    
    @api.model
    def web_read_group(self, domain, fields, groupby, limit=None, offset=0, orderby=False,lazy=True, expand=False, expand_limit=None, expand_orderby=False):
        res = super().web_read_group(domain, fields, groupby, limit, offset, orderby, lazy, expand, expand_limit, expand_orderby)
        for i in self.env['tcp.ports'].search([]):
            data_assets = self.env['it_inventory.tcp_ports.grc'].search([('tcp_ports_id', 'in', [i.id] )])
            self.env['tcp.ports'].sudo().search([('id','=',i.id)]).sudo().write({'it_inventory_count':len(data_assets)})
        return res
'''
# Pending
class NmapSystem(models.Model):
    _name = 'nmap.system'
    nmap_file = fields.Binary(string="nmap File")
    nmap_name = fields.Char(string="nmap name")
    nmap_output = fields.Html(string="nmap output")
'''

class TCPJustification(models.Model):
    _name = 'it_inventory.tcp_ports.grc'
    _rec_name = 'tcp_ports_id'
    tcp_ports_id = fields.Many2one('tcp.ports', string="TCP Port")
    it_inventory_id = fields.Many2one('it.inventory', string="IT System")
    business_justification = fields.Text(string="Bussiness justification")
    is_open = fields.Boolean(string="Is open", default=True)
    color = fields.Integer(string="Color", default=lambda x: x.default_color())

    def default_color(self):
        x = r.randrange(11)
        if x <= 11 or x > 0:
            return x
