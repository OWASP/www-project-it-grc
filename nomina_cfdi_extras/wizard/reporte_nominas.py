# -*- coding: utf-8 -*-

from odoo import models, fields, api
#import time
#from datetime import datetime
#from dateutil import relativedelta
from collections import defaultdict
import io
from odoo.tools.misc import xlwt
import base64

class WizardReporteNominas(models.TransientModel):
    _name = 'wizard.reporte.nomina'
    _description = 'WizardReporteNominas'

    name = fields.Char("Name")
    employee_id = fields.Many2one('hr.employee', string='Empleado')
    date_from = fields.Date(string='Fecha inicio')
    date_to = fields.Date(string='Fecha fin')
    department_id = fields.Many2one('hr.department', 'Departamento')
    file_data = fields.Binary("File Data")

    def print_reporte_nominas_report(self):
        #domain=[('state','=', 'done')]
        domain=[]
        if self.date_from:
            domain.append(('date_from','>=',self.date_from))
            
        if self.date_to:
            domain.append(('date_from','<=',self.date_to))
        if self.employee_id:
            domain.append(('employee_id','=',self.employee_id.id))
        if not self.employee_id and self.department_id:
            employees = self.env['hr.employee'].search([('department_id', '=', self.department_id.id)])
            domain.append(('employee_id','in',employees.ids))

        payslips = self.env['hr.payslip'].search(domain)

        workbook = xlwt.Workbook()
        bold = xlwt.easyxf("font: bold on;")
        worksheet = workbook.add_sheet('Nomina')
        from_to_date = 'De  %s A %s'%(self.date_from or '', self.date_to or '')
        worksheet.write_merge(1, 1, 0, 4, 'Reporte de nominas', bold)
        worksheet.write_merge(2, 2, 0, 4, from_to_date, bold)

        worksheet.write(4, 0, 'Procesamiento', bold)
        worksheet.write(4, 1, 'Periodo', bold)
        worksheet.write(4, 2, 'Fecha nomina', bold)
        worksheet.write(4, 3, 'Folio', bold)
        worksheet.write(4, 4, 'RFC', bold)
        worksheet.write(4, 5, 'Empleado', bold)
        worksheet.write(4, 6, 'Estado timbrado', bold)
        worksheet.write(4, 7, 'Total timbrado', bold)
        worksheet.write(4, 8, 'UUID', bold)
        worksheet.write(4, 9, 'Fecha de timbrado', bold)
        worksheet.write(4, 10, 'Fecha Certificación SAT', bold)
        worksheet.write(4, 11, 'Estado de nómina', bold)
        worksheet.write(4, 12, 'Cantidad retenida por ISR salarios', bold)
        worksheet.write(4, 13, 'Salario', bold)
        worksheet.write(4, 14, 'Septimo dia', bold)
        worksheet.write(4, 15, 'Subsidio al empleo aplicado', bold)
        worksheet.write(4, 16, 'Subsidio para el empleo', bold)
        worksheet.write(4, 17, 'ISR antes de SUBEM', bold)
        worksheet.write(4, 18, 'ISR a retener por subsidio entregado que no correspondia', bold)

        col = 4
        row = 5
        for payslip in payslips:
            worksheet.write(row, 0, payslip.payslip_run_id.name)
            #worksheet.write(row, 1, payslip.no_periodo)
            worksheet.write(row, 2, '%s A %s'%(payslip.date_from or '', payslip.date_to or ''))
            worksheet.write(row, 3, payslip.number)
            worksheet.write(row, 4, payslip.employee_id.rfc)
            worksheet.write(row, 5, payslip.employee_id.name)
            worksheet.write(row, 6, payslip.estado_factura)
            worksheet.write(row, 7, payslip.total_nomina)
            worksheet.write(row, 8, payslip.folio_fiscal)
            worksheet.write(row, 9, payslip.fecha_factura)
            worksheet.write(row, 10, payslip.fecha_certificacion)
            worksheet.write(row, 11, payslip.state)

            acum_isr = 0
            acum_dev_isr = 0
            acum_salario = 0
            acum_sept = 0
            acum_sub_aplicado = 0
            acum_sub_empleo = 0
            acum_isr_antes = 0
            acum_isr_retener = 0
            for line in payslip.line_ids:
                if line.code == 'ISR2' or line.code == 'D060':
                    acum_isr += line.total
                if line.code == 'O007':
                    acum_dev_isr += line.total
                if line.code == 'P001':
                    acum_salario += line.total
                if line.code == 'P005':
                    acum_sept += line.total
                if line.code == 'SUB':
                    acum_sub_aplicado += line.total
                if line.code == 'O001':
                    acum_sub_empleo += line.total
                if line.code == 'ISR':
                    acum_isr_antes += line.total
                if line.code == 'O005':
                    acum_isr_retener += line.total

            worksheet.write(row, 12, round(acum_isr - acum_dev_isr,2))
            worksheet.write(row, 13, round(acum_salario,2))
            worksheet.write(row, 14, round(acum_sept,2))
            worksheet.write(row, 15, round(acum_sub_aplicado,2))
            worksheet.write(row, 16, round(acum_sub_empleo,2))
            worksheet.write(row, 17, round(acum_isr_antes,2))
            worksheet.write(row, 18, round(acum_isr_retener,2))

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
            'url': "/web/content/?model="+self._name+"&id=" + str(self.id) + "&field=file_data&download=true&filename=Reporte_nominas.xls",
            'target': 'self',
            }
        return action
