# -*- coding: utf-8 -*-
from odoo import models, fields, _, api

class RegistroPatronal(models.Model):
    _name = 'registro.patronal'
    _description = 'RegistroPatronal'
    _rec_name = "registro_patronal"


    registro_patronal = fields.Char(string="Registro Patronal")
    descripcion = fields.Char(string="Descripción")
    prima_riesgo = fields.Char(string="Prima riesgo")
    no_guia = fields.Char(string="No. guía")
    ciudad = fields.Char(string="Ciudad")
    isn = fields.Char(string="ISN")
   
    clase_riesgo = fields.Selection(
        selection=[('01', 'Clase I'), 
                   ('02', 'Clase II'), 
                   ('03', 'Clase III'),
                   ('04', 'Clase IV'), 
                   ('05', 'Clase V'),
                   ('06', 'No aplica'),],
        string=_('Clase riesgo'),)
