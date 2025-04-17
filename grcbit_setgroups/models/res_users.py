# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class ResUsersInh(models.Model):
    _inherit = 'res.users'

    is_support = fields.Boolean(string="Is Support", default=False)

    '''
    def _check_admin_restriction(self):
        user = self.env.user
        is_admin_user = (
            user.has_group('base.group_system') and
            user.id == self.env.ref('base.user_admin').id
        )
        if not is_admin_user:
            #raise exceptions.AccessError("Solo el usuario administrador del sistema puede realizar esta acción.")
            raise ValidationError("This users can't be update for you")         
    '''

    def write(self, vals):
        '''
        user = self.env.user
        if not user.has_group('grcbit_base.group_grc_admin'):
            raise ValidationError("This users can't be update for you")
        if user.has_group('grcbit_base.group_grc_admin') and self.is_support == True:
            if not user.has_group('base.group_system') or not self.env.ref('base.user_admin'):
                raise ValidationError("This users can't be update for you")
        if 'is_support' in vals:
            if not user.has_group('base.group_system') or not self.env.ref('base.user_admin'):
                raise ValidationError("This users can't be update for you")
                #self._check_admin_restriction()
        '''
        for rec in self:
            user = rec.env.user
            if not user.has_group('grcbit_base.group_grc_admin'):
                raise ValidationError("This users can't be update for you")
            if user.has_group('grcbit_base.group_grc_admin') and rec.is_support == True:
                if not user.has_group('base.group_system') or not rec.env.ref('base.user_admin'):
                    raise ValidationError("This users can't be update for you")
            if 'is_support' in vals:
                if not user.has_group('base.group_system') or not rec.env.ref('base.user_admin'):
                    raise ValidationError("This users can't be update for you")

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

