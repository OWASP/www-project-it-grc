
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ManaDashboardHistoryData(models.Model):
    '''
    Mana Dashboard History Data
    '''
    _name = 'mana_dashboard.history_data'
    _description = 'History Data'

    title = fields.Char(string='Title')
    data = fields.Text(string='Data')
    remark = fields.Char(string='Remark')
