
# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools

help_html = '''<div class="alert alert-info" role="alert">
    <p>If it is global, it will be applied to all the targets.</p>
    <p>If it is specified, it will be applied to the targets you selected.</p>
    <ul>
'''

class ManaDashboardSearchGroupTraits(models.Model):
    '''
    Mana Dashboard Search Container Traits
    '''
    _name = 'mana_dashboard.search_group_traits'
    _description = 'Search Group Trait'

    name = fields.Char(
        string='Name', 
        required=True, 
        default=lambda self: self.env['ir.sequence'].next_by_code(
            'dashboard.search_group.sequence'))

    targets = fields.Many2many(
        string='Targets',
        comodel_name='mana_dashboard.any_config',
        relation='mana_search_group_traits_targets_rel')
    
    type = fields.Selection(
        string='Type',
        selection=[("specified", "specified"), ("global", "global")], 
        default="global")
    
    any_config_id = fields.Many2one(
        string='Config Id', 
        comodel_name='mana_dashboard.any_config')
    
    dashboard_id = fields.Many2one(
        string='Dashboard Id', 
        comodel_name='mana_dashboard.dashboard',
        related='any_config_id.dashboard_id', 
        store=True)
    
    search_immidiate = fields.Boolean(
        string='Immidiate', default=True)
    
    load_last_search = fields.Boolean(
        string='Load Last Search', default=True)

    help = fields.Html(string='Help', default=help_html)

    def export_search_groups(self):
        """
        export search groups
        """
        self.ensure_one()
        return {
            'targets': [(6, 0, self.targets.ids)],
            'type': self.type,
            'search_immidiate': self.search_immidiate,
        }
