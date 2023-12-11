
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ManaDashboardFileContent(models.Model):
    '''
    File Content Model
    '''
    _name = 'mana_dashboard.file_content'
    _description = 'Mana Dashboard File Content'

    content = fields.Text(string='content')
