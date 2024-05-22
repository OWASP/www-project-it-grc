# -*- coding: utf-8 -*-

from odoo import models, fields, api
from collections import defaultdict
import io
from odoo.tools.misc import xlwt
import base64
import logging
_logger = logging.getLogger(__name__)

class WizardISN(models.TransientModel):
    _name = 'wizard.isn'
    _description = 'WizardISN'

    name = fields.Char("Name")
    employee_id = fields.Many2one('hr.employee', string='Empleado')
    date_from = fields.Date(string='Fecha inicio', required=True)
    date_to = fields.Date(string='Fecha fin', required=True)
    department_id = fields.Many2one('hr.department', 'Departamento')
    file_data = fields.Binary("File Data")

    def print_reglas_salariales_report(self):
        domain=[('state','=', 'done')]
        domain_employee=[]
        if self.date_from:
            domain.append(('date_from','>=',self.date_from))
        if self.date_to:
            domain.append(('date_to','<=',self.date_to))
        if self.employee_id:
            domain.append(('employee_id','=',self.employee_id.id))
            domain_employee.append(('id','=',self.employee_id.id))
        if not self.employee_id and self.department_id:
            employees = self.env['hr.employee'].search([('department_id', '=', self.department_id.id)])
            domain.append(('employee_id','in',employees.ids))
            domain_employee.append(('id','in',employees.ids))

        _logger.info('domain_employee %s', domain_employee)
        employee_ids = self.env['hr.employee'].search(domain_employee)
        _logger.info('empleados %s', employee_ids)

        workbook = xlwt.Workbook()
        bold = xlwt.easyxf("font: bold on;")
        
        worksheet = workbook.add_sheet('Impuesto sobre nomina')
        
        from_to_date = 'De  %s A %s'%(self.date_from or '', self.date_to or '')
        
        worksheet.write_merge(1, 1, 0, 4, 'Reporte de impuesto sobre nomina', bold)
        worksheet.write_merge(2, 2, 0, 4, from_to_date, bold)

        worksheet.write(4, 0, 'Departamento', bold)
        worksheet.write(4, 1, 'No. Empleado', bold)
        worksheet.write(4, 2, 'Empleado', bold)
        worksheet.write(4, 3, 'Nomina', bold)
        worksheet.write(4, 4, 'Fecha', bold)
        worksheet.write(4, 5, 'Monto', bold)
        col = 4
        row = 5
        for empleado in employee_ids:
             total = 0
             if empleado.contract_ids:
                rule = self.env['hr.salary.rule'].search([('code', '=', 'TPER')], limit=1)
                payslips = self.env['hr.payslip'].search([('employee_id', '=', empleado.id), ('state','=', 'done'), ('date_from','>=',self.date_from), ('date_to','<=',self.date_to)])
                payslip_lines = payslips.mapped('line_ids').filtered(lambda x: x.salary_rule_id.id == rule.id)
                worksheet.write(row, 0, empleado.department_id.name)
                worksheet.write(row, 1, empleado.no_empleado)
                worksheet.write(row, 2, empleado.name)
                for line in payslip_lines:
                   worksheet.write(row, 3, line.slip_id.name)
                   worksheet.write(row, 4, line.slip_id.date_from)
                   worksheet.write(row, 5, line.total * empleado.contract_id.tablas_cfdi_id.isn/100)
                   total += line.total * empleado.contract_id.tablas_cfdi_id.isn/100
                   row +=1
             worksheet.write(row, 4, 'Total')
             worksheet.write(row, 5, total)
             row +=2

        fp = io.BytesIO()
        workbook.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        
        self.write({'file_data':base64.b64encode(data)})
        action = {
            'name': 'Payslips',
            'type': 'ir.actions.act_url',
            'url': "/web/content/?model="+self._name+"&id=" + str(self.id) + "&field=file_data&download=true&filename=ISN.xls",
            'target': 'self',
            }
        return action
