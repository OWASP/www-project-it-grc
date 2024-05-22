# -*- coding: utf-8 -*-
from odoo import models, fields

class ContractHistorialSalario(models.Model):
    _name = 'contract.historial.salario'
    _description = 'ContractHistorialSalario'

    fecha_sueldo = fields.Date('Fecha')
    sueldo_mensual = fields.Float('Sueldo mensual')
    sueldo_diario = fields.Float('Sueldo diario')
    sueldo_por_hora = fields.Float('Sueldo por hora')
    sueldo_diario_integrado = fields.Float('Sueldo diario integrado')
    sueldo_base_cotizacion = fields.Float('Sueldo base cotización')
    contract_id = fields.Many2one('hr.contract', 'Contract')
    