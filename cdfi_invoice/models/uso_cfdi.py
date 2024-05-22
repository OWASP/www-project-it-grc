# -*- coding: utf-8 -*-

from odoo import models, fields, api

class UsoCfdi(models.Model):
    _name = 'catalogo.uso.cfdi'
    _rec_name = "description"

    code = fields.Char(string='Clave')
    description = fields.Char(string='Descripción')
