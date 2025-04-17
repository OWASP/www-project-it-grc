# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class ResUsersInh(models.Model):
    _inherit = 'res.users'

    def open_set_groups(self):
        user = self.env.user
        if not user.has_group('grcbit_base.group_grc_admin'):
            raise ValidationError("This users can't be update for you")
        if user.has_group('grcbit_base.group_grc_admin') and self.is_support == True:
            raise ValidationError("This users can't be update for you")
        return {
            'name': _('Set Groups'),
            'view_type': 'form',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'res_model' : 'set.groups.user',
            'target': 'new',
            'context': {'default_user_id': self.id},
        }
