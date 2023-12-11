
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ManaDashboardContentEditor(models.TransientModel):
    '''
    Editor for the content like svg etc.
    '''
    _name = 'mana_dashboard.content_editor'
    _description = 'Content Editor'

    content = fields.Text(string='Content')
