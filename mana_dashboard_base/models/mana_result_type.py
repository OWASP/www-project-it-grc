
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ManaDashboardResultType(models.Model):
    '''
    Result Type
    '''
    _name = 'mana_dashboard.result_type'
    _description = 'Result Type'

    name = fields.Char(string='name', required=True)

    # name need to be unique
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'name need to be unique')
    ]
