# -*- coding: utf-8 -*-
from odoo import models, api, fields
from datetime import date

class HrContract(models.Model):
    _inherit = 'hr.contract'
    
    historial_salario_ids = fields.One2many('contract.historial.salario','contract_id', 'Historial Salario')

    def write(self, vals):
        res = super(HrContract, self).write(vals)
        if vals.get('state','')=='open':
            for contract in self:
                self.env['contract.historial.salario'].create({'fecha_sueldo': date.today(),
                                                'sueldo_mensual':contract.wage,
                                                'sueldo_diario' : contract.sueldo_diario,
                                                'sueldo_por_hora': contract.sueldo_hora,
                                                'sueldo_diario_integrado' : contract.sueldo_diario_integrado,
                                                'sueldo_base_cotizacion' : contract.sueldo_base_cotizacion,
                                                'contract_id' : contract.id, 
                                                })
        return res
