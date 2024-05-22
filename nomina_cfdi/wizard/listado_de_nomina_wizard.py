# -*- coding: utf-8 -*-
from odoo import models, fields, api

class TimbradoDeNominaWizard(models.TransientModel):
    _name = "timbrado.de.nomina"
    _description = 'Timbrado de nomina'
    
    todos = fields.Boolean(string='Rango')
    rango_de_empleados1 = fields.Integer(string='Rango de empleados')
    rango_de_empleados2 = fields.Integer(string='a')
    payslip_batch_id = fields.Many2one('hr.payslip.run','Payslip Run')
    
    def timbrado_nomina(self):
        #if not self.todos and self.rango_de_empleados1 and self.rango_de_empleados2:
        start = self.rango_de_empleados1
        end = self.rango_de_empleados2 
        todos = self.todos
        if todos:
            return self.payslip_batch_id.with_context(start_range=start,end_range=end).timbrar_nomina_wizard()
        else:
            return self.payslip_batch_id.timbrar_nomina_wizard()


class ConfirmadoDeNominaWizard(models.TransientModel):
    _name = "confirmado.de.nomina"
    _description = 'Confirmación de nomina'
    
    todos = fields.Boolean(string='Rango')
    rango_de_empleados1 = fields.Integer(string='Rango de empleados')
    rango_de_empleados2 = fields.Integer(string='a')
    payslip_batch_id = fields.Many2one('hr.payslip.run','Payslip Run')
    
    def confirmado_nomina(self):
        # if not self.todos and self.rango_de_empleados1 and self.rango_de_empleados2:
        start = self.rango_de_empleados1
        end = self.rango_de_empleados2 
        todos = self.todos
        if todos:
            return self.payslip_batch_id.with_context(start_range=start,end_range=end).confirmar_nomina_wizard()
        else:
            return self.payslip_batch_id.confirmar_nomina_wizard()


class RecalcularDeNominaWizard(models.TransientModel):
    _name = "recalcular.de.nomina"
    _description = 'Recalcular de nomina'

    todos = fields.Boolean(string='Rango')
    rango_de_empleados1 = fields.Integer(string='Rango de empleados')
    rango_de_empleados2 = fields.Integer(string='a')
    payslip_batch_id = fields.Many2one('hr.payslip.run', 'Payslip Run')

    def recalcular_nomina(self):
        # if not self.todos and self.rango_de_empleados1 and self.rango_de_empleados2:
        start = self.rango_de_empleados1
        end = self.rango_de_empleados2
        todos = self.todos
        if todos:
            return self.payslip_batch_id.with_context(start_range=start, end_range=end).recalcular_nomina_wizard()
        else:
            return self.payslip_batch_id.recalcular_nomina_wizard()
