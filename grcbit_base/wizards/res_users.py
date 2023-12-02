# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class ResUsersInh(models.Model):
    _inherit = 'res.users'

    def open_set_groups(self):
        return {
            'name': _('Set Groups'),
            'view_type': 'form',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'res_model' : 'set.groups.user',
            'target': 'new',
            'context': {'default_user_id': self.id},

        }