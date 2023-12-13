
# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, exceptions


class ManaDashboardAnyConfig(models.Model):
    '''
    Dashboard any config
    '''
    _name = 'mana_dashboard.any_config'
    _description = 'Dashboard Any Config'
    _rec_name = 'config_name'

    @api.model
    @tools.ormcache()
    def get_model_selections(self):
        """
        get all the models
        :return:
        """
        return [('mana_dashboard.config', 'Dashboard Config')]

    dashboard_id = fields.Many2one(
        comodel_name='mana_dashboard.dashboard',
        string='Dashboard', 
        ondelete='cascade')
        
    custom_props = fields.Text(string='Custom Props')

    ref_config = fields.Reference(
        string='Config', 
        selection='get_model_selections')

    config_name = fields.Char(
        string='Config Name', 
        compute='_compute_config_name')

    linked_config_ids = fields.Many2many(
        string='Linked Configs',
        comodel_name='mana_dashboard.any_config',
        relation='mana_dashboard_linked_config_rel',
        column1='config_id',
        column2='linked_config_id')

    drill_down_config = fields.Many2one(
        string='Drill Down Config',
        comodel_name='mana_dashboard.any_config',
        ondelete='set null')

    drill_up_config = fields.Many2one(
        string='Drill Up Config',
        comodel_name='mana_dashboard.any_config',
        ondelete='cascade')

    @api.model
    def create_config(self, dashboard_id, config_model, options={}):
        """
        create config
        :param dashboard_id:
        :param config_model:
        :return:
        """
        ref_config = self.sudo().env[config_model].create_config(dashboard_id, options)
        any_config = self.create({
            'dashboard_id': dashboard_id,
            'ref_config': '{config_model},{ref_id}'.format(
                config_model=config_model,
                ref_id=ref_config.id
            )
        })
        # bind config
        ref_config.any_config_id = any_config.id
        return {
            'config_id': any_config.id,
            'ref_config_id': ref_config.id
        }

    def get_config(self, options={}):
        """
        get config
        :param options:
        :return:
        """
        self.ensure_one()
        # check exits
        if not self.exists():
            return False
        config = self.read()
        if len(config) == 0:
            return False
        config = config[0]
        config['ref_config'] = self.ref_config.get_config(options)
        # set linked config ids
        config['ref_config']['linked_config_ids'] = config['linked_config_ids']
        config['custom_props'] = self.custom_props or '{}'
        return config
    
    def get_data_source(self, options={}):
        """
        get datas 
        :param options:
        :return:
        """
        self.ensure_one()
        return self.ref_config.get_data_source(options)
    
    def get_datas(self, options={}):
        """
        get datas
        :param options:
        :return:
        """
        self.ensure_one()
        return self.ref_config.get_datas(options)

    def export_any_config(self):
        """
        export config
        :return:
        """
        return {
            'id': self.id,
            'model': self.ref_config._name,
            'custom_props': self.custom_props or '',
            'config_info': self.ref_config.export_config()
        }

    @api.model
    def import_any_config(self, any_config_info):
        """
        import config
        :param config:
        :return:
        """
        model_name = any_config_info['model']
        config_info = any_config_info['config_info']
        # user may change the config name
        config_info['config_name'] = any_config_info.get('config_name')
        config = self.env[model_name].import_config(config_info)
        return self.create({
            'custom_props': any_config_info.get('custom_props'),
            'ref_config': '{},{}'.format(model_name, config.id)
        })
        
    # clone config
    def clone_config(self, options={}):
        """
        clone config
        :param options:
        :return:
        """
        config_info = self.export_any_config()
        config_info['config_name'] = options.get('config_name')
        new_config = self.import_any_config(config_info)

        return new_config

    def get_drill_down_config(self, options = {}):
        """
        get drill down config
        """
        return xw_utils.get_drill_config(self, options)

    @api.depends('ref_config')
    def _compute_config_name(self):
        """
        compute config name
        :return:
        """
        for config in self:
            if config.ref_config:
                config.config_name = config.ref_config.config_name

    def save_theme_info(self, theme_info):
        """
        save theme info
        :param options:
        :return:
        """
        self.ensure_one()
        self.ref_config.save_theme_info(theme_info)
