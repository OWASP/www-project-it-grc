# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _
_logger = logging.getLogger(__name__)
class SetGroupsUser(models.TransientModel):
    _name = 'set.groups.user'

    user_id = fields.Many2one('res.users', string="User")
    
    def assign_groups(self):
        data = {}