# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class ResUsersInh(models.Model):
    _inherit = 'res.users'

    def open_set_groups(self):
        user = self.env.user
        admin_user = self.env.ref('base.user_admin')

        if self.id == admin_user.id and user.id != admin_user.id:
            raise ValidationError(_("You cannot modify the administrator user."))

        if not user.has_group('grcbit_base.group_grc_admin'):
            raise ValidationError(_("You do not have permission to update this user."))

        return {
            'name': _('Set Groups'),
            'view_type': 'form',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'res_model' : 'set.groups.user',
            'target': 'new',
            'context': {'default_user_id': self.id},
        }
