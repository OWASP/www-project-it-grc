
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ManaDashboardThemeColor(models.Model):
    '''
    Mana Dashboard Theme Color
    '''
    _name = 'mana_dashboard.theme_color'
    _description = 'theme color'

    color = fields.Char(string='color')
    theme_id = fields.Many2one(
        string='theme_id', 
        comodel_name='mana_dashboard.theme')
