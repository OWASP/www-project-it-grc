# -*- coding: utf-8 -*-

from odoo import models, fields, api
#import time
#from datetime import datetime
#from dateutil import relativedelta
from collections import defaultdict
import io
from odoo.tools.misc import xlwt
import base64

class WizardReglasSalariales(models.TransientModel):
    _name = 'wizard.regalas.salarieles'
    _description = 'WizardReglasSalariales'

    name = fields.Char("Name")
    employee_id = fields.Many2one('hr.employee', string='Empleado')
    date_from = fields.Date(string='Fecha inicio')
    date_to = fields.Date(string='Fecha fin')
    department_id = fields.Many2one('hr.department', 'Departamento')
    rule_ids = fields.Many2many('hr.salary.rule', 'hr_salary_rule_regalas_salarieles_rel','wizard_id','rule_id', string='Conceptos')
    file_data = fields.Binary("File Data")
    
   
    def print_reglas_salariales_report(self):
        domain=[('state','=', 'done')]
        if self.date_from:
            domain.append(('date_from','>=',self.date_from))
            
        if self.date_to:
            domain.append(('date_to','<=',self.date_to))
        if self.employee_id:
            domain.append(('employee_id','=',self.employee_id.id))
        if not self.employee_id and self.department_id:
            employees = self.env['hr.employee'].search([('department_id', '=', self.department_id.id)])
            domain.append(('employee_id','in',employees.ids))
                        
        payslips = self.env['hr.payslip'].search(domain)
        rules = self.rule_ids
        payslip_lines = payslips.mapped('line_ids').filtered(lambda x: x.salary_rule_id.id in rules.ids) #.sorted(key=lambda x: x.slip_id.employee_id)
        
        workbook = xlwt.Workbook()
        bold = xlwt.easyxf("font: bold on;")
        
        worksheet = workbook.add_sheet('Nomina')
        
        from_to_date = 'De  %s A %s'%(self.date_from or '', self.date_to or '')
        concepto = 'Concepto:  %s'%(self.date_from)
        
        worksheet.write_merge(1, 1, 0, 4, 'Reporte de acumulados de conceptos', bold)
        worksheet.write_merge(2, 2, 0, 4, from_to_date, bold)
        #worksheet.write_merge(3, 3, 0, 4, concepto, bold)
        
        worksheet.write(4, 0, 'No.Empleado', bold)
        worksheet.write(4, 1, 'Empleado', bold)
        col = 4
        rule_index = {}
        for rule in rules:
            worksheet.write(4, col, rule.name, bold)
            rule_index.update({rule.id:col})
            col +=1
        #employees = defaultdict(dict)
        #employee_payslip = defaultdict(set)
        employees = {}
        for line in payslip_lines:
            if line.slip_id.employee_id not in employees:
                employees[line.slip_id.employee_id] = {line.slip_id: []}
            if line.slip_id not in employees[line.slip_id.employee_id]:
                employees[line.slip_id.employee_id].update({line.slip_id: []})    
            employees[line.slip_id.employee_id][line.slip_id].append(line)
            
            #employees[line.slip_id.employee_id].add(line)
            
            #employee_payslip[line.slip_id.employee_id].add(line.slip_id)
            
        row = 5
        tipo_nomina = {'O':'Nómina ordinaria', 'E':'Nómina extraordinaria'}
        for employee, payslips in employees.items():
            worksheet.write(row, 0, employee.no_empleado)
            worksheet.write(row, 1, employee.name)
            row +=1
            worksheet.write(row, 2, 'Fecha de la nomina', bold)
            worksheet.write(row, 3, 'Tipo', bold)
            row +=1
            total_by_rule = defaultdict(lambda: 0.0)
            for payslip,lines in payslips.items():
            #for line in lines:
                worksheet.write(row, 2, payslip.date_from)
                worksheet.write(row, 3, tipo_nomina.get(payslip.tipo_nomina,''))
                for line in lines:
                    worksheet.write(row, rule_index.get(line.salary_rule_id.id), line.total)
                    total_by_rule[line.salary_rule_id.id] += line.total
                row +=1
            worksheet.write(row, 3, 'Total', bold)
            for rule_id, total in total_by_rule.items():
                worksheet.write(row, rule_index.get(rule_id), total)
            row +=1
                
        fp = io.BytesIO()
        workbook.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        
        self.write({'file_data':base64.b64encode(data)})
        action = {
            'name': 'Payslips',
            'type': 'ir.actions.act_url',
            'url': "/web/content/?model="+self._name+"&id=" + str(self.id) + "&field=file_data&download=true&filename=Reglas_salariales.xls",
            'target': 'self',
            }
        return action
        
    
    