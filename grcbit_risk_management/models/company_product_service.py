from odoo import models, fields, api

class CompanyProductService(models.Model):
    _name = 'company.product.service'
    _description = 'Company Product Service'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    type_product_service = fields.Selection([
        ('product', 'Product'),
        ('service', 'Service')
    ], string="Type", required=True, tracking=True)
    active = fields.Boolean(default=True) 