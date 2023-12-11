
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ManaDashboardSeriesType(models.Model):
    '''
    Mana Dashboard Series Type
    '''
    _name = 'mana_dashboard.series_type'
    _description = 'false'

    name = fields.Char(string='name')


