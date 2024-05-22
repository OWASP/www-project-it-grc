# -*- coding: utf-8 -*-

from odoo import models,fields

class EntregaFondoCaja(models.TransientModel):
    _name = 'entrega.fondo.caja'
    _description = 'Entrega fondo caja'

    fecha_solicitud = fields.Date('Fecha solicitud')
    fecha_aplicacion = fields.Date('Fecha aplicación')
    descripcion = fields.Char("Descripción")
    clave = fields.Char("Código")
    
    
    def create_caja_de_ahorro(self):
        employee_ids = self.env['hr.employee'].search([])
        if len(employee_ids) >= 1:
            for employee in employee_ids:
                if len(employee.contract_ids) > 0:
                   new_caja_nomina_id = self.env['caja.nomina'].create({
                      'employee_id' : employee.id,
                      'fecha_solicitud': self.fecha_solicitud,
                      'fecha_aplicacion': self.fecha_aplicacion,
                      'descripcion': self.descripcion,
                      'clave': self.clave,
                   })
                   new_caja_nomina_id._compute_saldo()
                   new_caja_nomina_id.write({'importe': new_caja_nomina_id.saldo})
