# -*- coding: utf-8 -*-

from odoo import models, fields, api

class UnidadMedida(models.Model):
    _name = 'catalogo.unidad.medida'
    _rec_name = "descripcion"

    clave = fields.Char(string='Clave')
    descripcion = fields.Char(string='Descripción')
