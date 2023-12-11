
# -*- coding: utf-8 -*-

from odoo import models, fields


class ManaDashboardDataSourceType(models.Model):
    '''
    Mana Data Source Type
    '''
    _name = 'mana_dashboard.data_source_type'
    _description = 'Mana Data Source Type'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence', default=10)

    # name need to be unique
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'name need to be unique')
    ]
