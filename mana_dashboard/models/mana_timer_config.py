
# -*- coding: utf-8 -*-

from odoo import models, fields


class ManaDashboardTimerConfig(models.Model):
    '''
    Mana Dashboard Timer Config
    '''
    _name = 'mana_dashboard.timer_config'
    _description = 'Mana Dashboard Timer Config'

    def _default_name(self):
        """
        Default name use dashboard.sequence.timer
        """
        return self.env['ir.sequence'].next_by_code('dashboard.sequence.timer')

    name = fields.Char(
        string='Name',
        default=_default_name, 
        required=True)

    config_id = fields.Many2one(
        string= 'Config',
        comodel_name='mana_dashboard.any_config', 
        ondelete='cascade')

    dashboard_id = fields.Many2one(
        string='Dashboard',
        comodel_name='mana_dashboard.dashboard',
        related='config_id.dashboard_id')

    interval = fields.Integer(string='Interval', default=1000)

    targets = fields.Many2many(
        string='Targets',
        comodel_name='mana_dashboard.any_config', 
        relation='mana_dashboard_timer_config_target_rel',
        column1='timer_config_id',
        column2='config_id',
        ondelete='cascade',
        help='if not set, all targets will be notified')

    message = fields.Char(
        string='Message', 
        default='mana_dashboard.timer.reload_config', 
        required=True)

    repeat = fields.Integer(
        string='Repeat', 
        default=-1)

    remark = fields.Text(string='Remark')

    _sql_constraints = [
        ('name_dashboard_id_unique', 'unique(name, dashboard_id)', 'name and dashboard_id must be unique')
    ]

    def export_timer_config(self):
        """
        export timer config
        """
        self.ensure_one()
        return {
            'name': self.name,
            'interval': self.interval,
            'targets': [(6, 0, self.targets.ids)],
            'message': self.message,
            'repeat': self.repeat,
            'remark': self.remark,
            'config_id': self.config_id.id,
        }
    
    def import_timer_config(self, config):
        """
        import timer config, need to replace the old target ids and config id
        """
        self.create({
            'name': config.get('name'),
            'interval': config.get('interval'),
            'targets': [(6, 0, config.get('targets'))],
            'message': config.get('message'),
            'repeat': config.get('repeat'),
            'remark': config.get('remark'),
            'config_id': config.get('config_id'),
        })
        
