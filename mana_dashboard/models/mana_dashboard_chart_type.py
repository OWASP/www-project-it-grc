
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ManaDashboardChartType(models.Model):
    '''
    Mana Dashboard Chart Type
    '''
    _name = 'mana_dashboard.chart_type'
    _description = 'false'

    name = fields.Char(string='name', required=True)

    # name must be unique
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'name must be unique')
    ]
