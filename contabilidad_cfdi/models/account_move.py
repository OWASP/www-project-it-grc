# -*- coding: utf-8 -*-

from odoo import fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    contabilidad_electronica = fields.Boolean('CE', default=True)
    cierre_anual = fields.Boolean('Mes 13', default=False)
