
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class ManaDashboardConfigBase(models.Model):
    '''
    Config Base
    '''
    _name = 'mana_dashboard.config_base'
    _description = 'Mana Dashboard Config Base'
    _rec_name = 'config_name'

    # use dashboard.config.sequence to gen the default name
    def _default_name(self):
        """
        default name
        """
        raise exceptions.NotImplementedError(
            'The _default_name method must be implemented!')

    any_config_id = fields.Many2one(
        string='Any Config',
        comodel_name='mana_dashboard.any_config',
        ondelete='cascade')

    dashboard_id = fields.Many2one(
        comodel_name='mana_dashboard.dashboard', 
        string='Dashboard', 
        ondelete='cascade')

    config_name = fields.Char(
        string='Config Name', 
        required=True)

    multi_data_source = fields.Boolean(
        string='Multi Datas Source', 
        default=False)

    data_source_ids = fields.One2many(
        string='Data Sources', 
        comodel_name='mana_dashboard.data_source', 
        inverse_name='config_id')

    drill_down_config = fields.Many2one(
        string='Drill Down Config',
        comodel_name='mana_dashboard.any_config',
        ondelete='set null')

    drill_up_config = fields.Many2one(
        string='Drill Up Config',
        comodel_name='mana_dashboard.any_config',
        ondelete='cascade')
    
    last_search_info = fields.Text(
        string='Last Search Info')

    # config_name and dashboard_id must be unique
    _sql_constraints = [
        ('config_name_dashboard_id_unique', 'unique (config_name, dashboard_id)', 'The config name must be unique!'),
    ]

    def get_config(self, options = {}):
        """
        get config
        """
        self.ensure_one()

        try:
            result = self.read()[0]
        except Exception as e:
            return {'error': str(e)}
            
        result['result_type'] = result['result_type_name']

        # template res id
        if self.template_id:
            result['template_external_id'] = self.template_id.get_external_id().get(self.template_id.id)

        if options.get('fetch_data'):
            data_sources = []
            if self.multi_data_source:
                for data_source in self.data_source_ids:
                    data_sources.append(data_source.get_data_source(options))
            else:
                # inherit from mana_data_source
                data_sources.append(self.get_data_source(options))
                # check get previous data
                if options.get('get_previous_data'):
                    # get previous data
                    data_sources.append(self.get_previous_datas(options))
                    
            result['data_sources'] = data_sources
        else:
            result['data_sources'] = []

        return result

    @api.model
    def create_config(self, dashboard_id, options = {}):
        """
        create custom config
        """
        raise exceptions.NotImplementedError('The create_config method must be implemented!')
