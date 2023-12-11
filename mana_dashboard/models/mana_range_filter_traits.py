
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ManaDashboardRangeFilterTraits(models.Model):
    '''
    range filter traits
    '''
    _name = 'mana_dashboard.range_filter_traits'  
    _description = 'Mana Range Filter Traits'

    config_id = fields.Many2one(
        string='config_id', comodel_name='mana_dashboard.any_config', ondelete='cascade')
    type = fields.Selection(
        string='type', selection=[("specified", "specified"), ("global", "global")], default="global")
    targets = fields.Many2many(
        string='targets', comodel_name='mana_dashboard.any_config', relation='mana_dashboard_range_filter_traits_target_rel')
    
    def export_range_filter(self):
        """
        export range filter
        """
        self.ensure_one()
        return {
            'type': self.type,
            'targets': self.targets.ids,
        }
