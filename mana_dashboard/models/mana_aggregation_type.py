
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ManaDashboardAggregationType(models.Model):
    '''
    Aggregation Type
    '''
    _name = 'mana_dashboard.aggregation_type'
    _description = 'aggregation function types'

    name = fields.Char(string='name', required=True)

    # name must be unique
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'name must be unique'),
    ]

