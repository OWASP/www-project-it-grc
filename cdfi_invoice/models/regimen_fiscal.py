# -*- coding: utf-8 -*-

from odoo import models, fields, api

class RegimenFiscal(models.Model):
    _name = 'catalogo.regimen.fiscal'
    _rec_name = "description"

    code = fields.Char(string='Clave')
    description = fields.Char(string='Descripción')
