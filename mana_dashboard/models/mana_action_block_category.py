# -*- coding: utf-8 -*-

from odoo import models, fields


class ManaDashBlockActionBlockCateGory(models.Model):
    '''
    This model is used to define the category of the action block.
    '''
    _name = 'mana_dashboard.action_block_category'
    _description = 'Mana Dashboard Block Category'
    _order = 'sequence asc, id desc'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence', default=10)

    # name msut be unique
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The name of the category must be unique!')
    ]
