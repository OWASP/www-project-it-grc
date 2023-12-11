
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import json
import json5
import xw_utils


class ManaDashboardSearchInfo(models.Model):
    '''
    Search Info
    '''
    _name = 'mana_dashboard.search_info'
    _description = 'Mana Dashboard Search Info'

    name = fields.Char(string='name', required=True)
    dashboard_id = fields.Many2one(
        string='dashboard_id', comodel_name='mana_dashboard.dashboard')
    uid = fields.Many2one(string='uid', comodel_name='res.users')
    search_infos = fields.Text(string='search infos')
    
    # dashboard and name must be unique
    _sql_constraints = [
        ('dashboard_id_name_unique', 'unique(dashboard_id, name)', _('Dashboard and name must be unique!'))
    ]
        
    def reset_search_infos(self, dashboard_id):
        """
        reset search info
        """
        records = self.env['mana_dashboard.search_info'].search([
            ('dashboard_id', '=', dashboard_id),
            ('uid', '=', self.env.uid)
        ])
        records.unlink()
        self.clear_caches()

    def update_search_infos(self, dashboard_id, search_infos):
        """
        update search info
        """
        xw_utils.update_search_infos(self, dashboard_id, search_infos)
    
    def get_search_info(self, dashboard_id, name):
        """
        get search info
        """
        records = self.env['mana_dashboard.search_info'].search([
            ('dashboard_id', '=', dashboard_id),
            ('uid', '=', self.env.uid),
            ('name', '=', name)
        ], limit=1)
        if not records:
            return {}
        
        result = {}
        for record in records:
            result[record.name] = json.loads(record.search_infos)
        
        return result

    def get_search_infos(self, dashboard_id):
        """
        get search infos
        """
        records = self.env['mana_dashboard.search_info'].search([
            ('dashboard_id', '=', dashboard_id),
            ('uid', '=', self.env.uid)
        ])
        if not records:
            return {}
        
        result = {}
        for record in records:
            result[record.name] = json5.loads(record.search_infos)
        
        return result