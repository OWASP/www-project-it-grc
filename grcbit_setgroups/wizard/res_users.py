# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class ResUsersInh(models.Model):
    _inherit = 'res.users'

    is_admin = fields.Boolean(string="is admin", compute="_get_group")

    @api.onchange('name')
    def _onchange_is_admin_new(self):
        for rec in self:
            flag = self.env.user.has_group('base.group_system')
            rec.is_admin = flag

    def _get_group(self):
        for rec in self:
            flag = self.env.user.has_group('base.group_system')
            rec.is_admin = flag

    def open_set_groups(self):
        user_id = self.env.user
        if user_id.is_support != True and self.is_support == True:
            raise ValidationError("This users can't be update for you")
        else:
            return {
                'name': _('Set Groups'),
                'view_type': 'form',
                'view_mode': 'form',
                'type': 'ir.actions.act_window',
                'res_model' : 'set.groups.user',
                'target': 'new',
                'context': {'default_user_id': self.id},
            }