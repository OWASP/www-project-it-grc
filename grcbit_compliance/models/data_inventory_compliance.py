from odoo import models, fields, api

class DataInventoryComplianceVersion(models.Model):
    _name = 'data.inventory.compliance.version'
    _rec_name = 'compliance_version_id'
    
    data_inventory_id = fields.Many2one('data.inventory', string='Data Inventory')
    compliance_version_id = fields.Many2one('compliance.version', string='Compliance Version')
    description = fields.Text(string='Description')

class DataInventory(models.Model):
    _inherit = 'data.inventory'
    
    data_inventory_compliance_version_ids = fields.One2many('data.inventory.compliance.version', 'data_inventory_id', string='Compliance Version', auto_join=True, track_visibility='onchange') 