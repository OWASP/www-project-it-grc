
# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api
import pendulum

# date time range base
class ManaDashboardDatetimeRangeBase(models.Model):
    '''
    Mana Date Time Range Base
    '''
    _name = 'mana_dashboard.datetime_range_base'
    _description = 'Mana Date Time Range Base'

    range_type = fields.Char(string='Range Type', default='Custom Range')
    could_relative = fields.Boolean(string='Could Relative', default=False)

    start_time = fields.Datetime(string='Start Time', compute='_compute_start_time')
    end_time = fields.Datetime(string='End Time', compute='_compute_end_time')

    previous_start_time = fields.Datetime(string='Previous Start Time', compute='_compute_previous_start_time')
    previous_end_time = fields.Datetime(string='Previous End Time', compute='_compute_previous_end_time')

    @api.depends('range_type')
    def _compute_start_time(self):
        for record in self:
            range_type = record.range_type.lower()
            if range_type == 'today':
                record.start_time = pendulum.now().start_of('day').to_datetime_string()
                record.end_time = pendulum.now().end_of('day').to_datetime_string()
                record.previous_start_time = pendulum.now().subtract(days=1).start_of('day').to_datetime_string()
                record.previous_end_time = pendulum.now().subtract(days=1).end_of('day').to_datetime_string()
            elif range_type == 'yesterday':
                record.start_time = pendulum.now().subtract(days=1).start_of('day').to_datetime_string()
                record.end_time = pendulum.now().subtract(days=1).end_of('day').to_datetime_string()
                record.previous_start_time = pendulum.now().subtract(days=2).start_of('day').to_datetime_string()
                record.previous_end_time = pendulum.now().subtract(days=2).end_of('day').to_datetime_string()
            elif range_type == 'last week':
                record.start_time = pendulum.now().subtract(weeks=1).start_of('week').to_datetime_string()
                record.end_time = pendulum.now().subtract(weeks=1).end_of('week').to_datetime_string()
                record.previous_start_time = pendulum.now().subtract(weeks=2).start_of('week').to_datetime_string()
                record.previous_end_time = pendulum.now().subtract(weeks=2).end_of('week').to_datetime_string()
            elif range_type == 'last month':
                record.start_time = pendulum.now().subtract(months=1).start_of('month').to_datetime_string()
                record.end_time = pendulum.now().subtract(months=1).end_of('month').to_datetime_string()
                record.previous_start_time = pendulum.now().subtract(months=2).start_of('month').to_datetime_string()
                record.previous_end_time = pendulum.now().subtract(months=2).end_of('month').to_datetime_string()
            elif range_type == 'last quarter':
                record.start_time = pendulum.now().subtract(months=3).start_of('quarter').to_datetime_string()
                record.end_time = pendulum.now().subtract(months=3).end_of('quarter').to_datetime_string()
                record.previous_start_time = pendulum.now().subtract(months=6).start_of('quarter').to_datetime_string()
                record.previous_end_time = pendulum.now().subtract(months=6).end_of('quarter').to_datetime_string()
            elif range_type == 'last year':
                record.start_time = pendulum.now().subtract(years=1).start_of('year').to_datetime_string()
                record.end_time = pendulum.now().subtract(years=1).end_of('year').to_datetime_string()
                record.previous_start_time = pendulum.now().subtract(years=2).start_of('year').to_datetime_string()
                record.previous_end_time = pendulum.now().subtract(years=2).end_of('year').to_datetime_string()
            elif range_type == 'this week':
                record.start_time = pendulum.now().start_of('week').to_datetime_string()
                record.end_time = pendulum.now().end_of('week').to_datetime_string()
                record.previous_start_time = pendulum.now().subtract(weeks=1).start_of('week').to_datetime_string()
                record.previous_end_time = pendulum.now().subtract(weeks=1).end_of('week').to_datetime_string()
            elif range_type == 'this month':
                record.start_time = pendulum.now().start_of('month').to_datetime_string()
                record.end_time = pendulum.now().end_of('month').to_datetime_string()
                record.previous_start_time = pendulum.now().subtract(months=1).start_of('month').to_datetime_string()
                record.previous_end_time = pendulum.now().subtract(months=1).end_of('month').to_datetime_string()
            elif range_type == 'this quarter':
                record.start_time = pendulum.now().start_of('quarter').to_datetime_string()
                record.end_time = pendulum.now().end_of('quarter').to_datetime_string()
                record.previous_start_time = pendulum.now().subtract(months=3).start_of('quarter').to_datetime_string()
                record.previous_end_time = pendulum.now().subtract(months=3).end_of('quarter').to_datetime_string()
            elif range_type == 'this year':
                record.start_time = pendulum.now().start_of('year').to_datetime_string()
                record.end_time = pendulum.now().end_of('year').to_datetime_string()
                record.previous_start_time = pendulum.now().subtract(years=1).start_of('year').to_datetime_string()
                record.previous_end_time = pendulum.now().subtract(years=1).end_of('year').to_datetime_string()
            elif range_type == 'last 7 days':
                record.start_time = pendulum.now().subtract(days=7).start_of('day').to_datetime_string()
                record.end_time = pendulum.now().end_of('day').to_datetime_string()
                record.previous_start_time = pendulum.now().subtract(days=14).start_of('day').to_datetime_string()
                record.previous_end_time = pendulum.now().subtract(days=7).end_of('day').to_datetime_string()
            elif range_type == 'last 30 days':
                record.start_time = pendulum.now().start_of('day').subtract(days=30).to_datetime_string()
                record.end_time = pendulum.now().start_of('day').to_datetime_string()
                record.previous_start_time = pendulum.now().start_of('day').subtract(days=60).to_datetime_string()
                record.previous_end_time = pendulum.now().start_of('day').subtract(days=30).to_datetime_string()
            elif range_type == 'last 90 days':
                record.start_time = pendulum.now().start_of('day').subtract(days=90).to_datetime_string()
                record.end_time = pendulum.now().start_of('day').to_datetime_string()
                record.previous_start_time = pendulum.now().start_of('day').subtract(days=180).to_datetime_string()
                record.previous_end_time = pendulum.now().start_of('day').subtract(days=90).to_datetime_string()
            elif range_type == 'last 365 days':
                record.start_time = pendulum.now().start_of('day').subtract(days=365).to_datetime_string()
                record.end_time = pendulum.now().start_of('day').to_datetime_string()
                record.previous_start_time = pendulum.now().start_of('day').subtract(days=730).to_datetime_string()
                record.previous_end_time = pendulum.now().start_of('day').subtract(days=365).to_datetime_string()
            elif range_type == 'this 7 days':
                record.start_time = pendulum.now().start_of('day').to_datetime_string()
                record.end_time = pendulum.now().add(days=7).end_of('day').to_datetime_string()
                record.previous_start_time = pendulum.now().subtract(days=7).start_of('day').to_datetime_string()
                record.previous_end_time = pendulum.now().start_of('day').to_datetime_string()
            elif range_type == 'this 30 days':
                record.start_time = pendulum.now().start_of('day').to_datetime_string()
                record.end_time = pendulum.now().add(days=30).end_of('day').to_datetime_string()
                record.previous_start_time = pendulum.now().start_of('day').subtract(days=30).to_datetime_string()
                record.previous_end_time = pendulum.now().start_of('day').to_datetime_string()
            elif range_type == 'this 90 days':
                record.start_time = pendulum.now().start_of('day').to_datetime_string()
                record.end_time = pendulum.now().add(days=90).end_of('day').to_datetime_string()
                record.previous_start_time = pendulum.now().start_of('day').subtract(days=90).to_datetime_string()
                record.previous_end_time = pendulum.now().start_of('day').to_datetime_string()
            elif range_type == 'this 365 days':
                record.start_time = pendulum.now().start_of('day').to_datetime_string()
                record.end_time = pendulum.now().add(days=365).end_of('day').to_datetime_string()
                record.previous_start_time = pendulum.now().end_of('day').subtract(days=365).to_datetime_string()
                record.previous_end_time = pendulum.now().end_of('day').to_datetime_string()
            elif range_type == 'next week':
                record.start_time = pendulum.now().add(weeks=1).start_of('week').to_datetime_string()
                record.end_time = pendulum.now().add(weeks=1).end_of('week').to_datetime_string()
                record.previous_start_time = pendulum.now().start_of('week').to_datetime_string()
                record.previous_end_time = pendulum.now().end_of('week').to_datetime_string()
            elif range_type == 'next month':
                record.start_time = pendulum.now().add(months=1).start_of('month').to_datetime_string()
                record.end_time = pendulum.now().add(months=1).end_of('month').to_datetime_string()
                record.previous_start_time = pendulum.now().start_of('month').to_datetime_string()
                record.previous_end_time = pendulum.now().end_of('month').to_datetime_string()
            elif range_type == 'next quarter':
                record.start_time = pendulum.now().add(months=3).start_of('quarter').to_datetime_string()
                record.end_time = pendulum.now().add(months=3).end_of('quarter').to_datetime_string()
                record.previous_start_time = pendulum.now().start_of('quarter').to_datetime_string()
                record.previous_end_time = pendulum.now().end_of('quarter').to_datetime_string()
            elif range_type == 'next year':
                record.start_time = pendulum.now().add(years=1).start_of('year').to_datetime_string()
                record.end_time = pendulum.now().add(years=1).end_of('year').to_datetime_string()
                record.previous_start_time = pendulum.now().start_of('year').to_datetime_string()
                record.previous_end_time = pendulum.now().end_of('year').to_datetime_string()
            elif range_type == 'next 7 days':
                record.start_time = pendulum.now().end_of('day').to_datetime_string()
                record.end_time = pendulum.now().end_of('day').add(days=7).to_datetime_string()
                record.previous_start_time = pendulum.now().end_of('day').subtract(days=7).to_datetime_string()
                record.previous_end_time = pendulum.now().end_of('day').to_datetime_string()
            elif range_type == 'next 30 days':
                record.start_time = pendulum.now().end_of('day').to_datetime_string()
                record.end_time = pendulum.now().end_of('day').add(days=30).to_datetime_string()
                record.previous_start_time = pendulum.now().end_of('day').subtract(days=30).to_datetime_string()
                record.previous_end_time = pendulum.now().end_of('day').to_datetime_string()
            elif range_type == 'next 90 days':
                record.start_time = pendulum.now().end_of('day').to_datetime_string()
                record.end_time = pendulum.now().end_of('day').add(days=90).to_datetime_string()
                record.previous_start_time = pendulum.now().end_of('day').subtract(days=90).to_datetime_string()
                record.previous_end_time = pendulum.now().end_of('day').to_datetime_string()
            elif range_type == 'next 365 days':
                record.start_time = pendulum.now().end_of('day').to_datetime_string()
                record.end_time = pendulum.now().end_of('day').add(days=365).to_datetime_string()
                record.previous_start_time = pendulum.now().end_of('day').subtract(days=365).to_datetime_string()
                record.previous_end_time = pendulum.now().end_of('day').to_datetime_string()
            elif range_type == 'custom range':
                record.start_time = record.custom_start_time
                record.end_time = record.custom_end_time
                record.previous_start_time = False
                record.previous_end_time = False


class ManaDashboardDatetimeRange(models.Model):
    '''
    Mana Date Time Range
    '''
    _name = 'mana_dashboard.datetime_range'
    _description = 'Mana Date Time Range'
    _inherit = 'mana_dashboard.datetime_range_base'
    _rec_name = 'range_type'

    config_id = fields.Many2one(
        'mana_dashboard.config', string='Config', required=True, ondelete='cascade')

    uid = fields.Many2one(
        'res.users', string='User', default=lambda self: self.env.user)

    # for custom range
    custom_start_time = fields.Datetime(string='Custom Start')
    custom_end_time = fields.Datetime(string='Custom End')

   
class ManaDashboardFieldDatetimeRange(models.Model):
    '''
    Mana Field Date Time Range, just to use to create a new model type
    '''
    _name = 'mana_dashboard.field_datetime_range'
    _inherit = 'mana_dashboard.datetime_range_base'
    _description = 'Mana Field Date Time Range'
    _rec_name = 'range_type'

    pass
