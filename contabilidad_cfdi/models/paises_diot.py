# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ClavePaisesDiot(models.Model):
    _name = 'catalogos.pais_diot'
    _rec_name = "descripcion"
    _description = 'claves_paises_diot'

    c_pais = fields.Char(string='Clave Pais')
    descripcion = fields.Char(string='Pais')
    nacionalidad = fields.Char(string='Nacionalidad')