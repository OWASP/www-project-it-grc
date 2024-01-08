# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class ResUsersInh(models.Model):
    _inherit = 'res.users'

    def write(self, vals):
        res = super(ResUsersInh, self).write(vals)
        user_id = self.env.user
        if user_id.name != 'support' or user_id.login != 'support@grcbit.com':
            if self.name == 'support'  or self.login == 'support@grcbit.com':
                raise ValidationError("This users can't be update for you")
        return res