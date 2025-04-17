# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
from datetime import date
from statistics import mode
import random as r

_logger = logging.getLogger(__name__)

class DataClassification(models.Model):
    _name = 'data.classification'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Data Classification'
    

    name = fields.Char(string=_('Data Classification'), required=True, help="Categorizing data based on its sensitivity, importance, and predefined criteria.", track_visibility='onchange')
    description = fields.Text(string=_('Description'), required=True, help="Categorizing data based on its sensitivity, importance, and predefined criteria.", track_visibility='onchange')
    data_inventory_count = fields.Integer(string=_("Data Asset Count"))
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', _("The data classification name already exists."))]

    @api.model
    def web_read_group(self, domain, fields, groupby, limit=None, offset=0, orderby=False,lazy=True, expand=False, expand_limit=None, expand_orderby=False):
        res = super().web_read_group(domain, fields, groupby, limit, offset, orderby, lazy, expand, expand_limit, expand_orderby)
        for i in self.env['data.classification'].search([]):
            data_assets = self.env['data.inventory'].search([('data_classification_id', 'in', [i.id] )])
            self.env['data.classification'].sudo().search([('id','=',i.id)]).sudo().write({'data_inventory_count':len(data_assets)})
        return res

class ItInventory(models.Model):
    _name = 'it.inventory'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'IT Inventory'

    name = fields.Char(string=_('System Name'), required=True, track_visibility='onchange')
    description = fields.Text(string=_('Description'), required=True, track_visibility='onchange')
    #ip = fields.Char(string=_('IP'), required=True, track_visibility='onchange')
    #url = fields.Char(string=_('URL'), track_visibility='onchange')
    environment = fields.Selection([
        ('prod', 'Production'), 
        ('dev', 'Development'), 
        ('stg','Staging')
        ], string=_('Enviroment'), required=True, track_visibility='onchange')
    #is_cloud = fields.Boolean(string=_('Cloud Hosted?'), required=True, track_visibility='onchange')
    users_qty = fields.Integer(string=_('User Quantity'), track_visibility='onchange')
    attachment = fields.Many2many('ir.attachment', string=_("Attachment"), track_visibility='onchange')
    data_inventory_count = fields.Integer(string=_("Data Asset Count"))
    #xdr_agent = fields.Char(string="XDR Agent ID", track_visibility='onchange')
    active = fields.Boolean(default=True)
    tcp_inventory_ids = fields.One2many('it_inventory.tcp_ports.grc', 'it_inventory_id', string="TCP Port", auto_join=True)
    it_component_ids = fields.One2many('it.inventory.it.component','it_inventory_id',string='IT Component', auto_join=True)

    _sql_constraints = [('name_uniq', 'unique(name)', _("The IT system name already exists."))]

    @api.model
    def web_read_group(self, domain, fields, groupby, limit=None, offset=0, orderby=False,lazy=True, expand=False, expand_limit=None, expand_orderby=False):
        res = super().web_read_group(domain, fields, groupby, limit, offset, orderby, lazy, expand, expand_limit, expand_orderby)
        for i in self.env['it.inventory'].search([]):
            data_assets = self.env['data.inventory.it.inventory'].search([('it_inventory_id', 'in', [i.id] )])
            self.env['it.inventory'].sudo().search([('id','=',i.id)]).sudo().write({'data_inventory_count':len(data_assets)})
        return res
    
class DataInventory(models.Model):
    _name = 'data.inventory'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Data Inventory'

    name = fields.Char(string=_('Asset Name'), required=True, track_visibility='onchange')
    owner = fields.Many2one('hr.employee', string="Data Asset Owner", track_visibility='onchange')
    description = fields.Text(string=_('Description'), required=True, track_visibility='onchange')
    data_classification_id = fields.Many2one('data.classification', help="Categorizing data based on its sensitivity, importance, and predefined criteria.", string=_('Data Classification'), required=True, track_visibility='onchange')
    data_inventory_business_process_ids = fields.One2many('data.inventory.business.process', 'data_inventory_id', string='Business Process', auto_join=True, track_visibility='onchange')
    data_inventory_third_party_ids = fields.One2many('data.inventory.third.party', 'data_inventory_id', string='Supplier', auto_join=True, track_visibility='onchange')
    data_inventory_security_requirement_ids = fields.One2many('data.inventory.security.requirement','data_inventory_id', string='Security Requirement', auto_join=True, track_visibility='onchange')
    data_inventory_it_inventory_ids = fields.One2many('data.inventory.it.inventory','data_inventory_id', string='IT Inventory', auto_join=True, track_visibility='onchange')
    retention_period = fields.Selection([
        ('na','N/A (Not applicable)'),
        ('1m','1 month'),
        ('2m','2 months'),
        ('3m','3 months'),
        ('4m','4 months'),
        ('5m','5 months'),
        ('6m','6 months'),
        ('7m','7 months'),
        ('8m','8 months'),
        ('9m','9 months'),
        ('10m','10 months'),
        ('11m','11 months'),
        ('1y','1 year'),
        ('2y','2 years'),
        ('3y','3 years'),
        ('4y','4 years'),
        ('5y','5 years'),
        ], required=True, help="Amount of time an organization keeps certain types of data before deleting or archiving it.", track_visibility='onchange')
    attachment = fields.Many2many('ir.attachment', string=_("Attachment"), required=True, track_visibility='onchange')
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', _("The data inventory name already exists."))]

    @api.model
    def get_data(self):
        """Returns data to the tiles of dashboard"""
        it_system = self.env['it.inventory'].search([])
        third_party = self.env['third.party'].search([])
        _logger.info("THIRDPATY"+str(len(third_party)))
        return {
            'it_system': len(it_system),
            'third_party': len(third_party),
        }

class ThirdParty(models.Model):
    _name = 'third.party'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _decription = 'Third-Party'

    name = fields.Char(string=_('Third Party Vendor'), required=True, help="Organizations that do not directly interact with customers or business data consumers.", track_visibility='onchange')
    description = fields.Text(string=_('Description'), required=True, help="Organizations that do not directly interact with customers or business data consumers.", track_visibility='onchange')
    attachment = fields.Many2many('ir.attachment', string=_("Attachment"), track_visibility='onchange')
    data_inventory_count = fields.Integer(string=_("Data Asset Count"))
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', _("The third party name already exists."))]

    @api.model
    def web_read_group(self, domain, fields, groupby, limit=None, offset=0, orderby=False,lazy=True, expand=False, expand_limit=None, expand_orderby=False):
        res = super().web_read_group(domain, fields, groupby, limit, offset, orderby, lazy, expand, expand_limit, expand_orderby)
        for i in self.env['third.party'].search([]):
            _logger.info('grcbitdebug:' + str(i))
            data_assets = self.env['data.inventory.third.party'].search([('third_party_id', 'in', [i.id] )])
            self.env['third.party'].sudo().search([('id','=',i.id)]).sudo().write({'data_inventory_count':len(data_assets)})
        return res

class BusinessProcess(models.Model):
    _name = 'business.process'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = 'process_name'

    process_name = fields.Char(string="Process Name", track_visibility='onchange')
    process_owner = fields.Many2one('hr.employee', string="Process Owner", track_visibility='onchange')
    description = fields.Text(string="Description", track_visibility='onchange')
    data_inventory_count = fields.Integer(string=_("Data Asset Count"))
    active = fields.Boolean(default=True)

    @api.model
    def web_read_group(self, domain, fields, groupby, limit=None, offset=0, orderby=False,lazy=True, expand=False, expand_limit=None, expand_orderby=False):
        res = super().web_read_group(domain, fields, groupby, limit, offset, orderby, lazy, expand, expand_limit, expand_orderby)
        for i in self.env['business.process'].search([]):
            data_assets = self.env['data.inventory.business.process'].search([('business_process_id', 'in', [i.id] )])
            self.env['business.process'].sudo().search([('id','=',i.id)]).sudo().write({'data_inventory_count':len(data_assets)})
        return res

class DataInventoryBusinessProcess(models.Model):
    _name = 'data.inventory.business.process'
    _rec_name = 'business_process_id'
    data_inventory_id = fields.Many2one('data.inventory', string='Data Inventory')
    business_process_id = fields.Many2one('business.process', string='Business Process')
    description = fields.Text(string='Description')

class DataInventoryThirdParty(models.Model):
    _name = 'data.inventory.third.party'
    _rec_name = 'third_party_id'
    data_inventory_id = fields.Many2one('data.inventory', string='Data Inventory')
    third_party_id = fields.Many2one('third.party', string='Supplier')
    description = fields.Text(string='Description')

class DataInventorySecurityRequirement(models.Model):
    _name = 'data.inventory.security.requirement'
    _rec_name = 'security_requirement'
    data_inventory_id = fields.Many2one('data.inventory', string='Data Inventory')
    security_requirement = fields.Char(string='Security Requirement')
    description = fields.Text(string='Description')

class DataInventoryItInventory(models.Model):
    _name = 'data.inventory.it.inventory'
    _rec_name = 'it_inventory_id'
    data_inventory_id = fields.Many2one('data.inventory', string='Data Inventory')
    it_inventory_id = fields.Many2one('it.inventory', string='IT Inventory')
    description = fields.Text(string='Description')

class ItInventoryItComponent(models.Model):
    _name = 'it.inventory.it.component'
    _rec_name = 'it_component_id'
    it_inventory_id = fields.Many2one('it.inventory', string='IT Asset', track_visibility='onchange')
    it_component_id = fields.Many2one('it.components', string='IT Component', track_visibility='onchange')
    ip = fields.Char(string=_('IP'), track_visibility='onchange')
    url = fields.Char(string=_('URL'), track_visibility='onchange')
    is_cloud = fields.Boolean(string=_('Cloud Hosted?'), required=True, track_visibility='onchange')
    description = fields.Text(string='Description', track_visibility='onchange')
    responsible = fields.Many2one('hr.employee', string="Responsible", track_visibility='onchange')
    xdr_agent = fields.Char(string=_('XDR Agent'), track_visibility='onchange')
    color = fields.Integer(string="Color", default=lambda x: x.default_color())

    def default_color(self):
        x = r.randrange(11)
        if x <= 11 or x > 0:
            return x
