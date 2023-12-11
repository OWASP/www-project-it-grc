# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ManaDashboardDataSource(models.Model):
    '''
    Mana Data Source
    '''
    _name = 'mana_dashboard.data_source'
    _inherit = 'mana_dashboard.data_source_base'
    _inherits = {'mana_dashboard.data_source_mixin': 'data_source_mixin_id'}
    _description = 'Mana data source'
    _order = 'sequence, id'

    sequence = fields.Integer(string='Sequence', default=10)

    data_source_mixin_id = fields.Many2one(
        comodel_name='mana_dashboard.data_source_mixin', 
        string='Data Source Mixin', 
        required=True,
        ondelete='cascade')

    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals_list):
        """
        overwrite to set linked configs
        """
        res = super(ManaDashboardDataSource, self).create(vals_list)
        res.update_linked_config()
        return res

    def write(self, vals):
        """ 
        write(vals)
        """
        res = super(ManaDashboardDataSource, self).write(vals)
        self.update_linked_config()
        return res

    def update_linked_config(self):
        """
        update linked config
        """
        for record in self:
            if record.link_to_config:
                config_id = record.link_to_config.id
                config = self.env['mana_dashboard.any_config'].browse(config_id)
                # for multi data source
                if record.config_id:
                    config.linked_config_ids = [(4, record.config_id.any_config_id.id)]
                else:
                    # link to self, for single data source
                    config.linked_config_ids = [(4, record.any_config_id.id)]

    @api.onchange('config_id')
    def _onchange_data_source_type(self):
        """
        onchange data source type
        """
        if self.config_id and self.config_id.template_id:
            # set the default data_source_type
            if self.config_id.template_id.default_data_source_type:
                self.data_source_type = self.config_id.template_id.default_data_source_type
            elif self.config_id.template_id.supported_data_source_types:
                self.data_source_type = self.config_id.template_id.supported_data_source_types[0]
            
            # set the default data_result type
            if self.config_id.template_id.default_result_type:
                self.result_type = self.config_id.template_id.default_result_type
            elif self.config_id.template_id.supported_result_types:
                self.result_type = self.config_id.template_id.supported_result_types[0]

    def export_data_source(self):
        """
        export data source
        """
        self.ensure_one()
        return {
            'sequence': self.sequence,
            'data_source_mixin_id': self.data_source_mixin_id.export_data_source_mixin(),
        }

    def import_data_source(self, data_source):
        """
        import data source
        """
        # create data source mixin
        data_source_mixin = self.env['mana_dashboard.data_source_mixin'].import_data_source_mixin(
            data_source['data_source_mixin_id'])
        data_source = self.create({
            'sequence': data_source['sequence'],
            'data_source_mixin_id': data_source_mixin.id
        })
        return data_source