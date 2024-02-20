# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class ResUsersInh(models.Model):
    _inherit = 'res.users'

    is_support = fields.Boolean(string="Is Support", default=False)

        
    def write(self, vals):
        res = super(ResUsersInh, self).write(vals)
        user_id = self.env.user
        context = self.env.context
        for rec in self:
            if 'install_mode' in context:
                break
            elif 'params' in context:
                if user_id.is_support != True and rec.is_support== True:
                    raise ValidationError("This users can't be update for you")         
            
        return res