
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class ManaDashboardThemeBase(models.Model):
    '''
    Mana Dashboard Theme Base
    '''
    _name = 'mana_dashboard.theme_base'
    _description = 'Mana Dashboard Theme Base'

    theme_info = fields.Text(string='Theme Info')

    @api.model
    def save_theme_info(self, theme_info):
        """
        save theme info
        :param theme_info:
        :return:
        """
        self.ensure_one()
        self.theme_info = theme_info
