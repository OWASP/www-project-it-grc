# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class ResUsersInh(models.Model):
    _inherit = 'res.users'

    is_support = fields.Boolean(string="Is Support", default=False)

    def write(self, vals):
        res = super(ResUsersInh, self).write(vals)
        user_id = self.env.user
        if user_id.is_support != True:
            raise ValidationError("This users can't be update for you")
        return res