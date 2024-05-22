# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
# from odoo.exceptions import UserError
# import requests
# import json
# import base64

class AccountAccount(models.Model):
    _inherit = 'account.account'

#    centralized = fields.Boolean('Centralized')

    cuenta_sat = fields.Char(string='Código agrupador SAT')
    cuenta_tipo = fields.Selection(
        selection=[('A', 'Acreedora'), 
                   ('D', 'Deudora'),],
        string='Tipo Cuenta',
    )
   # activo = fields.Boolean('Usar en contabilidad electrónica', default=True)

