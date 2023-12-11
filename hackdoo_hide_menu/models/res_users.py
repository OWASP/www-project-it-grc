# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class ResUsersHide(models.Model):
    _inherit = 'res.users'

    user_menuitems_ids = fields.Many2many('ir.ui.menu', string="Menuitems")