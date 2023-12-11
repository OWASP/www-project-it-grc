# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ManaDashboardTemplate(models.Model):
    '''
    Mana Dashboard Template, This is different from mana_dashboard_template
    '''
    _name = 'mana_dashboard.dashboard_template'
    _description = 'Mana Dashboard Template'

    name = fields.Char(string='name', required=True)
    
    template = fields.Text(string='Template', required=True)
    
    # files
    style_files = fields.Many2many(
        'ir.attachment', 
        string='Style Files', 
        relation='mana_dashboard_template_style_files_rel')   
    js_files = fields.Many2many(
        'ir.attachment', 
        string='Js Files',
        relation='mana_dashboard_template_js_files_rel')
    image_files = fields.Many2many(
        'ir.attachment', 
        string='Image Files',
        relation='mana_dashboard_template_image_files_rel')

    file_urls = fields.Text(
        string='File Urls', compute='_compute_file_urls')

    description = fields.Html(string='Description')
    preview = fields.Binary(string='Preview')

    block_template_ids = fields.One2many(
        comodel_name='mana_dashboard.template',
        inverse_name='dashboard_template_id',
        string='Template Blocks')

    # name msut be unique
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The name of the template must be unique!')
    ]

    @api.depends('style_files', 'js_files', 'image_files')
    def _compute_file_urls(self):
        """
        compute file urls js_files
        """
        for record in self:
            urls = []
            for css_file in record.style_files:
                url = 'web/content/mana_dashboard.template/%s/style_files/%s' % (record.id, css_file.id)
                urls.append(url)
            for js_file in record.js_files:
                url = 'web/content/mana_dashboard.template/%s/js_files/%s' % (record.id, js_file.id)
                urls.append(url)
            for image_file in record.image_files:
                url = 'web/content/mana_dashboard.template/%s/image_files/%s' % (record.id, image_file.id)
                urls.append(url)
            record.file_urls = urls.join(',')
