# -*- coding: utf-8 -*-

from odoo import models, fields, api

#-------------------------------------
# Asset Management
#-------------------------------------

class DataClassification(models.Model):
    _name = 'data.classification'
    _description = 'Data Classification'

    name = fields.Char(string='Data Classification', required=True)
    description = fields.Text(string='Description')
    
    _sql_constraints = [
        ('name_uniq', 'unique(name)', "The data classification name already exists."),
    ]

class ItInventory(models.Model):
    _name = 'it.inventory'
    _description = 'IT Inventory'

    name = fields.Char(string='System Name', required=True)
    description = fields.Text(string='Description', required=True)
    ip = fields.Char(string='IP', required=True)
    url = fields.Char(string='URL', required=True)
    responsible = fields.Many2one('res.users', string='IT Admin', required=True)
    environment = fields.Selection([('prod', 'Production'), ('dev', 'Development'), ('stg','Staging')], string='Enviroment', required=True)
    is_cloud = fields.Boolean(string='Cloud Hosting', required=True)
    cloud_provider = fields.Char(string='Cloud Provider', required=True)
    is_internet_exposed = fields.Boolean(string='Internet Exposed', required=True)
    users_qty = fields.Integer(string='User Quantity', required=True)
    os_version = fields.Char(string='OS Version', required=True)
    db_version = fields.Char(string='DB Version', required=True)
    #ii_id = fields.Many2one('data.inventory')

    _sql_constraints = [
        ('name_uniq', 'unique(name)', "The IT system name already exists."),
    ]

class DataInventory(models.Model):
    _name = 'data.inventory'
    _description = 'Data Inventory'

    name = fields.Char(string='Asset Name', required=True)
    description = fields.Text(string='Description', required=True)
    data_classification_id = fields.Many2one('data.classification', string='Data Classification', required=True)
    location = fields.Char(string='Location', required=True)
    owner = fields.Many2one('res.users', string='Asset Owner', required=True)
    #ii_id   = fields.One2many('it.inventory','ii_id', string='IT System')
    it_inventory_id = fields.Many2many('it.inventory',string='IT System', required=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', "The data inventory name already exists."),
    ]

#--------------------------------
# ISO 27001:2022
#--------------------------------

class ControlType(models.Model):
    name = fields.Char(string='Control Type', required=True)
    description = fields.Text(string='Description', required=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The control type name already exists.")]

class ControlType(models.Model):
    name = fields.Char(string='Control Type', required=True)
    description = fields.Text(string='Description', required=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The control type name already exists.")]




# class grcbit(models.Model):
#     _name = 'grcbit.grcbit'
#     _description = 'grcbit.grcbit'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
