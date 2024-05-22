# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date
import base64
import logging
_logger = logging.getLogger(__name__)

class GenerarReciboNomina(models.TransientModel):
    _name='generar.recibo.nomina'
    _description = 'Generar recibo de nomina'

    department_id = fields.Many2one('hr.department',string="Departamento")
    

    #Function to print the report of recibo nomina by employee department
    def print_recibo_nomina(self):
        self.ensure_one()
        [data] = self.read()
        
        ctx = self._context.copy()
        if ctx.get('active_ids') and ctx.get('active_model','')=='hr.payslip.run':
            payslips = self.env['hr.payslip.run'].browse(ctx.get('active_id')).slip_ids.filtered(lambda x: x.employee_id.department_id.id == self.department_id.id)
            datas = {
                'ids': [],
                'model': 'hr.payslip',
                'form': data
            }
            return self.env.ref('nomina_cfdi.report_payslips').with_context(from_transient_model=True).report_action(payslips)

