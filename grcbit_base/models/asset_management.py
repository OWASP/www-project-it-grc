# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
from datetime import date
from statistics import mode

_logger = logging.getLogger(__name__)

class DataClassification(models.Model):
    _name = 'data.classification'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Data Classification'
    

    name = fields.Char(string=_('Data Classification'), required=True, help="Categorizing data based on its sensitivity, importance, and predefined criteria.")
    description = fields.Text(string=_('Description'), required=True, help="Categorizing data based on its sensitivity, importance, and predefined criteria.")
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

    name = fields.Char(string=_('System Name'), required=True)
    description = fields.Text(string=_('Description'), required=True)
    ip = fields.Char(string=_('IP'), required=True)
    url = fields.Char(string=_('URL'))
    environment = fields.Selection([
        ('prod', 'Production'), 
        ('dev', 'Development'), 
        ('stg','Staging')
        ], string=_('Enviroment'), required=True)
    is_cloud = fields.Boolean(string=_('Cloud Hosted?'), required=True)
    is_internet_exposed = fields.Boolean(string=_('Internet Exposed?'), required=True)
    users_qty = fields.Integer(string=_('User Quantity'), required=True)
    os_version = fields.Char(string=_('OS Version'))
    db_version = fields.Char(string=_('DB Version'))
    it_components = fields.Many2many('it.components','name', string=_('IT Components'))
    attachment = fields.Many2many('ir.attachment', string=_("Attachment"))
    data_inventory_count = fields.Integer(string=_("Data Asset Count"))
    # tcp_port = fields.Many2many('tcp.ports', 'it_inventory_tcp_ports_rel', 'it_inventory_id', 'tcp_ports_id', string="TCP Port")
    nmap_ids = fields.Many2many('nmap.system', string="nmap" )
    # business_justification = fields.Text(string="Bussiness justification", track_visibility='onchange')
    # is_open = fields.Boolean(string="Is open", default=True)
    active = fields.Boolean(default=True)
    tcp_inventory_ids = fields.One2many('it_inventory.tcp_ports.grc', 'it_inventory_id', string="TCP Port", auto_join=True)
    _sql_constraints = [('name_uniq', 'unique(name)', _("The IT system name already exists."))]

    @api.model
    def web_read_group(self, domain, fields, groupby, limit=None, offset=0, orderby=False,lazy=True, expand=False, expand_limit=None, expand_orderby=False):
        res = super().web_read_group(domain, fields, groupby, limit, offset, orderby, lazy, expand, expand_limit, expand_orderby)
        for i in self.env['it.inventory'].search([]):
            data_assets = self.env['data.inventory'].search([('it_inventory_id', 'in', [i.id] )])
            self.env['it.inventory'].sudo().search([('id','=',i.id)]).sudo().write({'data_inventory_count':len(data_assets)})
        return res
    
class DataInventory(models.Model):
    _name = 'data.inventory'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Data Inventory'

    name = fields.Char(string=_('Asset Name'), required=True)
    description = fields.Text(string=_('Description'), required=True)
    data_classification_id = fields.Many2one('data.classification', help="Categorizing data based on its sensitivity, importance, and predefined criteria.", string=_('Data Classification'), required=True)
    business_process_id = fields.Many2many('business.process', string="Business Process", help="Process where the data is used")
    it_inventory_id = fields.Many2many('it.inventory',string=_('IT System'), required=True, help="Computer system where data is stored, processed or transmitted")
    third_party_id = fields.Many2many('third.party',string=_('Supplier'), help="Organizations that do not directly interact with customers or business data consumers.")
    security_requirement = fields.Text(string=_('Security Requirement'), required=True, help="Requirements levied on an information system that are derived from applicable laws, Executive Orders, directives, policies, standards, instructions, regulations, or procedures, or organizational mission/business case needs to ensure the confidentiality, integrity, and availability of the information being processed, stored, or transmitted.")
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
        ], required=True, help="Amount of time an organization keeps certain types of data before deleting or archiving it.")
    attachment = fields.Many2many('ir.attachment', string=_("Attachment"), required=True)
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

    name = fields.Char(string=_('Third Party Vendor'), required=True, help="Organizations that do not directly interact with customers or business data consumers.")
    description = fields.Text(string=_('Description'), required=True, help="Organizations that do not directly interact with customers or business data consumers.")
    attachment = fields.Many2many('ir.attachment', string=_("Attachment"))
    data_inventory_count = fields.Integer(string=_("Data Asset Count"))
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', _("The third party name already exists."))]

    @api.model
    def web_read_group(self, domain, fields, groupby, limit=None, offset=0, orderby=False,lazy=True, expand=False, expand_limit=None, expand_orderby=False):
        res = super().web_read_group(domain, fields, groupby, limit, offset, orderby, lazy, expand, expand_limit, expand_orderby)
        for i in self.env['third.party'].search([]):
            _logger.info('grcbitdebug:' + str(i))
            data_assets = self.env['data.inventory'].search([('third_party_id', 'in', [i.id] )])
            self.env['third.party'].sudo().search([('id','=',i.id)]).sudo().write({'data_inventory_count':len(data_assets)})
        return res

class BusinessProcess(models.Model):
    _name = 'business.process'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = 'process_name'

    process_name = fields.Char(string="Process Name")
    process_owner = fields.Many2one('hr.employee', string="Process Owner")
    description = fields.Html(string="Description")
    data_inventory_count = fields.Integer(string=_("Data Asset Count"))

    @api.model
    def web_read_group(self, domain, fields, groupby, limit=None, offset=0, orderby=False,lazy=True, expand=False, expand_limit=None, expand_orderby=False):
        res = super().web_read_group(domain, fields, groupby, limit, offset, orderby, lazy, expand, expand_limit, expand_orderby)
        for i in self.env['business.process'].search([]):
            data_assets = self.env['data.inventory'].search([('business_process_id', 'in', [i.id] )])
            self.env['business.process'].sudo().search([('id','=',i.id)]).sudo().write({'data_inventory_count':len(data_assets)})
        return res