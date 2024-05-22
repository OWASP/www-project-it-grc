# -*- coding: utf-8 -*-

from odoo import models, fields, api

class WizardDarBaja(models.TransientModel):
    _name = 'wizard.dar.baja'
    _description = 'WizardDarBaja'
    
    fecha = fields.Date(string="Fecha")
    tipo_de_baja = fields.Selection([('1','Término de contrato'),
                                      ('2','Separación voluntaria'),
                                      ('3','Abandono de empleo'),
                                      ('4','Defunción'),
                                      ('5','Clausura'),
                                      ('6','Otras'),
                                      ('7','Ausentismo'),
                                      ('8','Rescisión de contrato'),
                                      ('9','Jubilación'),
                                      ('A', 'Pensión')], string='Tipo de baja')

    #FUNCTION TO CREATE DAR ALTA
    def action_dar_baja(self):
        nomina_id = self.env['hr.payslip.run'].browse(self._context.get('active_id'))
        for rec in nomina_id.slip_ids:
            if rec.nom_liquidacion == True:
                vals = {
                    'tipo_de_incidencia': 'Baja',
                    'employee_id': rec.employee_id.id,
                    'fecha': self.fecha,
                    'tipo_de_baja': self.tipo_de_baja,
                    'contract_id': rec.employee_id.contract_id.id,
                }
                record = self.env['incidencias.nomina'].create(vals)
                record.action_validar()


    """ THIS WORKS BUT ONLY WITH ONE LINE IN SLIP_IDS

    #FUNCTION TO CREATE INCIDENTIA DAR ALTA
    def action_dar_baja(self):
        nomina_id = self.env['hr.payslip.run'].browse(self._context.get('active_id'))
        for rec in nomina_id:
            if rec.slip_ids.nom_liquidacion == True:
                vals = {
                    'tipo_de_incidencia': 'Baja',
                    'employee_id': rec.slip_ids.employee_id.id,
                    'fecha': self.fecha,
                    'tipo_de_baja': self.tipo_de_baja
                }
        self.env['incidencias.nomina'].create(vals)"""
