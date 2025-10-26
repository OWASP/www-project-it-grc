# -*- coding: utf-8 -*-
from odoo import models
from odoo.exceptions import ValidationError

class ResUsersInh(models.Model):
    _inherit = 'res.users'

    def write(self, vals):
        for rec in self:
            current_user = rec.env['res.users'].sudo().browse(
                rec._context.get('uid', rec.env.user.id)
            )
            admin_user = rec.env.ref('base.user_admin')

            if rec.id == admin_user.id and current_user.id != admin_user.id:
                raise ValidationError("You cannot modify this user")

            if current_user.id == rec.id:
                continue

            if not current_user.has_group('grcbit_base.group_grc_admin'):
                raise ValidationError("You cannot modify this user")

        return super().write(vals)

    def unlink(self):
        admin_user = self.env.ref('base.user_admin')
        if admin_user in self:
            raise ValidationError("You cannot modify this user")
        return super().unlink()

    def copy(self, default=None):
        admin_user = self.env.ref('base.user_admin')
        if self.id == admin_user.id:
            raise ValidationError("You cannot modify this user")
        return super().copy(default)
