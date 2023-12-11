
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ManaDashboardBlockSettings(models.Model):
    '''
    Mana Dashboard Block Settings
    '''
    _name = 'mana_dashboard.block_settings'
    _description = 'mana dashboard block settings'

    config_id = fields.Many2one(
        string= 'Config',
        comodel_name='mana_dashboard.any_config', 
        ondelete='cascade')

    dashboard_id = fields.Many2one(
        string='Dashboard',
        comodel_name='mana_dashboard.dashboard',
        related='config_id.dashboard_id')
    
    content = fields.Text(
        string='content', help="This is a json string")
