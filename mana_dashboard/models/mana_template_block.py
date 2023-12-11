
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ManaDashboardTemplateBlock(models.Model):
    '''
    Template Block
    '''
    _name = 'mana_dashboard.template_block'
    _description = 'Dashboard Template Block'

    name = fields.Char(string='name')

    dashboard_template_id = fields.Many2one(
        string='dashboard_template',
        comodel_name='mana_dashboard.dashboard_template')

    # default template
    default_template_id = fields.Many2one(
        string='default_template',
        comodel_name='mana_dashboard.template')
        
    template = fields.Text(string='template')
    demo_template = fields.Text(string='Demo Template')

    scripts = fields.Text(string='Scripts')
    default_scripts = fields.Text(string='Default Scripts')
