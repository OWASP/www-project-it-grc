# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
from datetime import date
from statistics import mode

_logger = logging.getLogger(__name__)

class DataClassification(models.Model):
    _name = 'data.classification'
    _description = 'Data Classification'

    name = fields.Char(string=_('Data Classification'), required=True)
    description = fields.Text(string=_('Description'), required=True)
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
    _description = 'IT Inventory'

    name = fields.Char(string=_('System Name'), required=True)
    description = fields.Text(string=_('Description'), required=True)
    ip = fields.Char(string=_('IP'), required=True)
    url = fields.Char(string=_('URL'))
    business_process_id = fields.Many2many('business.process', string="Business Process")
    # responsible = fields.Many2one('res.users', string=_('IT Admin'), required=True)
    environment = fields.Selection([
        ('prod', 'Production'), 
        ('dev', 'Development'), 
        ('stg','Staging')
        ], string=_('Enviroment'), required=True)
    is_cloud = fields.Boolean(string=_('Cloud Hosted?'), required=True)
    # cloud_provider = fields.Many2many('third.party',string=_('Third Party'))
    is_internet_exposed = fields.Boolean(string=_('Internet Exposed?'), required=True)
    users_qty = fields.Integer(string=_('User Quantity'), required=True)
    os_version = fields.Char(string=_('OS Version'))
    db_version = fields.Char(string=_('DB Version'))
    it_components = fields.Many2many('it.components','name', string=_('IT Components'))
    attachment = fields.Many2many('ir.attachment', string=_("Attachment"))
    data_inventory_count = fields.Integer(string=_("Data Asset Count"))
    active = fields.Boolean(default=True)
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
    _description = 'Data Inventory'

    name = fields.Char(string=_('Asset Name'), required=True)
    description = fields.Text(string=_('Description'), required=True)
    data_classification_id = fields.Many2one('data.classification', string=_('Data Classification'), required=True)
    # location = fields.Char(string=_('Location'), required=True)
    # owner = fields.Many2one('res.users', string=_('Asset Owner'), required=True)
    business_process_id = fields.Many2many('business.process', string="Business Process")
    it_inventory_id = fields.Many2many('it.inventory',string=_('IT System'), required=True)
    third_party_id = fields.Many2many('third.party',string=_('Third Party'))
    security_requirement = fields.Text(string=_('Security Requirement'), required=True)
    retention_period = fields.Selection([
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
        ], required=True)
    attachment = fields.Many2many('ir.attachment', string=_("Attachment"), required=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', _("The data inventory name already exists."))]

    @api.model
    def get_data(self):
        """Returns data to the tiles of dashboard"""
        it_system = self.env['it.inventory'].search([])
        third_party = self.env['third.party'].search([])
        _logger.info("THIRDPATY"+str(len(third_party)))
    #    storable = self.env['product.template'].search([('detailed_type', '=', 'product')])
    #    consumable = self.env['product.template'].search([('detailed_type', '=', 'consu')])
        return {
            'it_system': len(it_system),
            'third_party': len(third_party),
            # 'storable': len(storable),
            # 'consumable': len(consumable),
        }

class ThirdParty(models.Model):
    _name = 'third.party'
    _decription = 'Third-Party'

    name = fields.Char(string=_('Third Party Vendor'), required=True)
    description = fields.Text(string=_('Description'), required=True)
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