# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class ResUsersInh(models.Model):
    _inherit = 'res.users'

    is_support = fields.Boolean(string="Is Support", default=False)


    def write(self, vals):
        for rec in self:
            user = rec.env.user
            # Allow users to update themselves
            if user.id == rec.id:
                return super().write(vals)
                
            if not user.has_group('grcbit_base.group_grc_admin'):
                raise ValidationError("1. This users can't be update for you")
            if user.has_group('grcbit_base.group_grc_admin') and rec.is_support == True:
                if not user.has_group('base.group_system') or not rec.env.ref('base.user_admin'):
                    raise ValidationError("2. This users can't be update for you")
            if 'is_support' in vals:
                if not user.has_group('base.group_system') or not rec.env.ref('base.user_admin'):
                    raise ValidationError("3. This users can't be update for you")

        return super().write(vals)

    def unlink(self):
        #self._check_admin_restriction()
        user = self.env.user
        if not user.has_group('grcbit_base.group_grc_admin'):
            raise ValidationError("This users can't be update for you")
        if user.has_group('grcbit_base.group_grc_admin') and self.is_support == True:
            raise ValidationError("This users can't be update for you")

        return super().unlink()

    def copy(self, default=None):
        #self._check_admin_restriction()
        user = self.env.user
        if not user.has_group('grcbit_base.group_grc_admin'):
            raise ValidationError("This users can't be update for you")
        if user.has_group('grcbit_base.group_grc_admin') and self.is_support == True:
            raise ValidationError("This users can't be update for you")

        return super().copy(default)