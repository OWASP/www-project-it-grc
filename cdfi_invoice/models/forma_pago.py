# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FormaPago(models.Model):
    _name = 'catalogo.forma.pago'
    _rec_name = "description"

    code = fields.Char(string='Clave')
    description = fields.Char(string='Descripción')
