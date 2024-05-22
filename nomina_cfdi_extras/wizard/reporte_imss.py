# -*- coding: utf-8 -*-

from odoo import models, fields, api
#import time
#from datetime import datetime
#from dateutil import relativedelta
from collections import defaultdict
import io
from odoo.tools.misc import xlwt
import base64

class WizardReporteImss(models.TransientModel):
    _name = 'wizard.imss.nomina'
    _description = 'WizardReporteImss'

    name = fields.Char("Name")
    employee_id = fields.Many2one('hr.employee', string='Empleado')
    date_from = fields.Date(string='Fecha inicio')
    date_to = fields.Date(string='Fecha fin')
    department_id = fields.Many2one('hr.department', 'Departamento')
    file_data = fields.Binary("File Data")

    def print_reporte_imss_report(self):
        #domain=[('state','=', 'done')]
        domain=[]
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

        workbook = xlwt.Workbook()
        bold = xlwt.easyxf("font: bold on;")
        worksheet = workbook.add_sheet('IMSS')
        from_to_date = 'De  %s A %s'%(self.date_from or '', self.date_to or '')
        worksheet.write_merge(1, 1, 0, 4, 'Reporte IMSS', bold)
        worksheet.write_merge(2, 2, 0, 4, from_to_date, bold)

        worksheet.write(4, 0, 'Employee number', bold)
        worksheet.write(4, 1, 'Employee name', bold)
        worksheet.write(4, 2, 'Exedente 3 SMGDF', bold)
        worksheet.write(4, 3, 'Prest. en dinero', bold)
        worksheet.write(4, 4, 'Gastos médicos', bold)
        worksheet.write(4, 5, 'Invalidez y Vida', bold)
        worksheet.write(4, 6, 'Cesantia y vejez', bold)
        worksheet.write(4, 7, 'IMSS trabajador', bold)
        worksheet.write(4, 8, '', bold)
        worksheet.write(4, 9, 'Cuota fija patronal', bold)
        worksheet.write(4, 10, 'Exedente 3 SMGDF', bold)
        worksheet.write(4, 11, 'Prest. en dinero', bold)
        worksheet.write(4, 12, 'Gastos médicos', bold)
        worksheet.write(4, 13, 'Riegso de trabajo', bold)
        worksheet.write(4, 14, 'Invalidez y Vida', bold)
        worksheet.write(4, 15, 'Guarderias y PS', bold)
        worksheet.write(4, 16, 'Retiro', bold)
        worksheet.write(4, 17, 'Cesantia y vejez', bold)
        worksheet.write(4, 18, 'INFONAVIT', bold)
        worksheet.write(4, 19, 'IMSS patron', bold)

        row_index = 5
        col_index=0
        
    
        group_by_employee_dict = {}
        
        for payslip in payslips:
            if payslip.state != 'done':
                    continue
            
            if payslip.employee_id.id not in group_by_employee_dict:
                group_by_employee_dict[payslip.employee_id.id] = {}
            
                group_by_employee_dict[payslip.employee_id.id]['emp_no'] = payslip.employee_id.no_empleado
                group_by_employee_dict[payslip.employee_id.id]['emp_name'] = payslip.employee_id.name
                
            group_by_employee_dict[payslip.employee_id.id]['emp_exedente_smg'] = group_by_employee_dict[payslip.employee_id.id].get('emp_exedente_smg',0.0) + payslip.emp_exedente_smg
            group_by_employee_dict[payslip.employee_id.id]['emp_prest_dinero'] = group_by_employee_dict[payslip.employee_id.id].get('emp_prest_dinero',0.0) + payslip.emp_prest_dinero
            group_by_employee_dict[payslip.employee_id.id]['emp_esp_pens'] = group_by_employee_dict[payslip.employee_id.id].get('emp_esp_pens',0.0) + payslip.emp_esp_pens
            group_by_employee_dict[payslip.employee_id.id]['emp_invalidez_vida'] = group_by_employee_dict[payslip.employee_id.id].get('emp_invalidez_vida',0.0) + payslip.emp_invalidez_vida
            group_by_employee_dict[payslip.employee_id.id]['emp_cesantia_vejez'] = group_by_employee_dict[payslip.employee_id.id].get('emp_cesantia_vejez',0.0) + payslip.emp_cesantia_vejez
            group_by_employee_dict[payslip.employee_id.id]['emp_total'] = group_by_employee_dict[payslip.employee_id.id].get('emp_total',0.0) + payslip.emp_total
            group_by_employee_dict[payslip.employee_id.id]['pat_cuota_fija_pat'] = group_by_employee_dict[payslip.employee_id.id].get('pat_cuota_fija_pat',0.0) + payslip.pat_cuota_fija_pat
            group_by_employee_dict[payslip.employee_id.id]['pat_exedente_smg'] = group_by_employee_dict[payslip.employee_id.id].get('pat_exedente_smg',0.0) + payslip.pat_exedente_smg
            group_by_employee_dict[payslip.employee_id.id]['pat_prest_dinero'] = group_by_employee_dict[payslip.employee_id.id].get('pat_prest_dinero',0.0) + payslip.pat_prest_dinero
            
            
            group_by_employee_dict[payslip.employee_id.id]['pat_esp_pens'] = group_by_employee_dict[payslip.employee_id.id].get('pat_esp_pens',0.0) + payslip.pat_esp_pens
            group_by_employee_dict[payslip.employee_id.id]['pat_riesgo_trabajo'] = group_by_employee_dict[payslip.employee_id.id].get('pat_riesgo_trabajo',0.0) + payslip.pat_riesgo_trabajo
            group_by_employee_dict[payslip.employee_id.id]['pat_invalidez_vida'] = group_by_employee_dict[payslip.employee_id.id].get('pat_invalidez_vida',0.0) + payslip.pat_invalidez_vida
            group_by_employee_dict[payslip.employee_id.id]['pat_guarderias'] = group_by_employee_dict[payslip.employee_id.id].get('pat_guarderias',0.0) + payslip.pat_guarderias
            group_by_employee_dict[payslip.employee_id.id]['pat_retiro'] = group_by_employee_dict[payslip.employee_id.id].get('pat_retiro',0.0) + payslip.pat_retiro
            group_by_employee_dict[payslip.employee_id.id]['pat_cesantia_vejez'] = group_by_employee_dict[payslip.employee_id.id].get('pat_cesantia_vejez',0.0) + payslip.pat_cesantia_vejez
            
            
            group_by_employee_dict[payslip.employee_id.id]['pat_infonavit'] = group_by_employee_dict[payslip.employee_id.id].get('pat_infonavit',0.0) + payslip.pat_infonavit
            group_by_employee_dict[payslip.employee_id.id]['pat_total'] = group_by_employee_dict[payslip.employee_id.id].get('pat_total',0.0) + payslip.pat_total
             
        for emp_id, info in group_by_employee_dict.items():        
            worksheet.write(row_index, col_index, info.get('emp_no'))
            col_index+=1
            worksheet.write(row_index, col_index, info.get('emp_name'))
            col_index+=1
            worksheet.write(row_index, col_index, info.get('emp_exedente_smg'))
            col_index+=1
            worksheet.write(row_index, col_index, info.get('emp_prest_dinero'))
            col_index+=1
            worksheet.write(row_index, col_index, info.get('emp_esp_pens'))
            col_index+=1
            worksheet.write(row_index, col_index, info.get('emp_invalidez_vida'))
            col_index+=1
            worksheet.write(row_index, col_index, info.get('emp_cesantia_vejez'))
            col_index+=1
            worksheet.write(row_index, col_index, info.get('emp_total'))
            col_index=col_index+2
            worksheet.write(row_index, col_index, info.get('pat_cuota_fija_pat'))
            col_index+=1
            worksheet.write(row_index, col_index, info.get('pat_exedente_smg'))
            col_index+=1
            worksheet.write(row_index, col_index, info.get('pat_prest_dinero'))
            col_index+=1
            worksheet.write(row_index, col_index, info.get('pat_esp_pens'))
            col_index+=1
            worksheet.write(row_index, col_index, info.get('pat_riesgo_trabajo'))
            col_index+=1
            worksheet.write(row_index, col_index, info.get('pat_invalidez_vida'))
            col_index+=1
            worksheet.write(row_index, col_index, info.get('pat_guarderias'))
            col_index+=1
            worksheet.write(row_index, col_index, info.get('pat_retiro'))
            col_index+=1
            worksheet.write(row_index, col_index, info.get('pat_cesantia_vejez'))
            col_index+=1
            worksheet.write(row_index, col_index, info.get('pat_infonavit'))
            col_index+=1
            worksheet.write(row_index, col_index, info.get('pat_total'))
            row_index+=1
            col_index=0


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
