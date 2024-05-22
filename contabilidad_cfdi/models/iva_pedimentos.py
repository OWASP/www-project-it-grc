# -*- coding: utf-8 -*-

from odoo import models, fields, api

class IvaPedimentos(models.Model):
    _name = "iva.pedimentos"

    partner_id = fields.Many2one('res.partner', string="Cliente", required=True)
    monto_iva = fields.Float(string='Monto IVA', required = True)
    fecha = fields.Date(string='Fecha', required = True)