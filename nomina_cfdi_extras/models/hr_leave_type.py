# -*- coding: utf-8 -*-

from odoo import api, fields, models

class HolidaysType(models.Model):
    _inherit = "hr.leave.type"

    code = fields.Char('Código')