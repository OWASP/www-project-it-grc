# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class ResCurrency(models.Model):
    _inherit = 'res.currency'

    no_decimales = fields.Integer('Decimales moneda', default=2, help='Número de decimales máximo para la moneda segun el SAT')
    no_decimales_tc = fields.Integer('Decimales tipo cambio', default=2, help='Número de decimales para el tipo de cambio')
