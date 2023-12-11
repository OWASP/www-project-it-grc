# -*- coding: utf-8 -*-

from odoo import models, fields, api
import xw_utils


class ManaDashboardConfig(models.Model):
    '''
    Dashboard Config
    '''
    _name = 'mana_dashboard.config'
    _inherit = [
        'mana_dashboard.config_base', 
        'mana_dashboard.template_base',
        'mana_dashboard.data_source',
        'mana_dashboard.theme_base',
    ]
    _description = 'Mana Dashboard Config'
    _rec_name = 'config_name'

    # as related and compute from mixin not work, so we override it here
    template_id = fields.Many2one(
        string='Template',
        comodel_name='mana_dashboard.template')

    supported_data_source_types = fields.Many2many(
        comodel_name='mana_dashboard.data_source_type',
        related='template_id.supported_data_source_types')

    data_source_type_domain_ids = fields.One2many(
        string='Data Source Type Domain',
        compute='_compute_data_source_type_domain_ids',
        comodel_name='mana_dashboard.data_source_type')

    supported_result_types = fields.Many2many(
        string='Supported Result Types',
        comodel_name='mana_dashboard.result_type',
        related='template_id.supported_result_types')

    result_type_domain_ids = fields.One2many(
        string='Result Type Domain',
        comodel_name='mana_dashboard.result_type',
        compute='_compute_result_type_domain_ids')

    @api.model
    def get_next_name(self):
        """
        get next name
        """
        name = self.env['ir.sequence'].next_by_code('dashboard.config.sequence')
        while self.search([('config_name', '=', name)]):
            name = self.env['ir.sequence'].next_by_code('dashboard.config.sequence')
        return name

    @api.model
    def create_config(self, dashboard_id, options = {}):
        """
        create custom config
        """
        record = xw_utils.create_config(self, dashboard_id, options)
        return record

    @api.depends('template_category', 'template_type')
    def _compute_template_domain_ids(self):
        """
        if has a drill up category, it is a drill down config
        """
        for record in self:
            if record.template_category and not record.drill_up_config:
                domain = [('category', '=', record.template_category)]
                if record.template_type:
                    domain.append(('type', '=', record.template_type))
                record.template_domain_ids = self.env['mana_dashboard.template'].search(domain).ids or False
            else:
                record.template_domain_ids = self.env['mana_dashboard.template'].search([]).ids or False

    @api.depends('supported_data_source_types')
    def _compute_data_source_type_domain_ids(self):
        """
        override this method to set the domain of data source type
        """
        for record in self:
            if record.supported_data_source_types:
                record.data_source_type_domain_ids = record.supported_data_source_types.ids
            else:
                record.data_source_type_domain_ids = self._get_data_source_types()

    @api.depends('supported_result_types')
    def _compute_result_type_domain_ids(self):
        for record in self:
            record.result_type_domain_ids = self._get_result_types()

    def export_config(self):
        """
        export config
        """
        return xw_utils.export_config(self)

    @api.model
    def import_config(self, config_info):
        """
        import config
        """
        return xw_utils.import_config(self, config_info)
    
    def save_theme_info(self, theme_info):
        """
        save theme info
        """
        self.ensure_one()
        self.theme_info = theme_info
        return True
