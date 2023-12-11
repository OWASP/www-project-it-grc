# -*- coding: utf-8 -*-

from odoo import models, fields, api
import xw_utils


class ManaDashboardTemplate(models.Model):
    '''
    Mana Template
    '''
    _name = 'mana_dashboard.template'
    _description = 'Mana Template'

    supported_data_source_types = fields.Many2many(
        comodel_name='mana_dashboard.data_source_type',
        relation='mana_dashboard_template_data_source_type_rel',
        column1='template_id',
        column2='data_source_type_id',
        string='Supported Data Source Types', 
        help='Supported Data Source Types, if empty, all types are supported')

    supported_result_types = fields.Many2many(
        comodel_name='mana_dashboard.result_type',
        relation='mana_dashboard_template_data_result_type_rel',
        column1='template_id',
        column2='data_result_type_id',
        string='Supported Data Result Types', 
        help='Supported Data Result Types, if empty, all types are supported')
    
    supported_series_types = fields.Many2many(
        comodel_name='mana_dashboard.series_type',
        relation='mana_dashboard_template_data_series_type_rel',
        column1='template_id',
        column2='data_series_type_id',
        string='Supported Series Types',
        help='Supported Series Types')

    def get_image_url(self):
        """
        get image url
        """
        self.ensure_one()
        return '/web/image/mana_dashboard.template/%s/preview' % self.id
    
    @api.model
    def _add_inherited_fields(self):
        """ Determine inherited fields. """

        # add inherited fields
        super()._add_inherited_fields()

        # check fields
        xw_utils.ensure_template_fields(self, fields)
