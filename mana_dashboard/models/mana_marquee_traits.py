
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ManaDashboardMarqueeTraits(models.Model):
    '''
    Mana Marquee Traits
    '''
    _name = 'mana_dashboard.marquee_traits'
    _description = 'Mana Dashboard Marquee Trait'

    config_id = fields.Many2one(
        string='config id',
        comodel_name='mana_dashboard.any_config',
        ondelete='cascade')
    circular = fields.Boolean(string='circular', default=True)
    loop = fields.Integer(string='loop', default=-1)
    direction = fields.Selection(
        string='direction', 
        selection=[("down", "down"), ("up", "up"), ("right", "right"), ("left", "left")],
        default="left")
    scrolldelay = fields.Integer(string='scrolldelay', default=0)
    scrollamount = fields.Integer(string='scrollamount', default=50)
    runshort = fields.Boolean(string='runshort', default=True)
    hoverstop = fields.Boolean(string='hoverstop', default=True)
    inverthover = fields.Boolean(string='inverthover', default=False)

