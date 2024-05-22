# -*- coding: utf-8 -*-

from odoo import models


class PartnerXlsx(models.AbstractModel):
    _name = 'report.nomina_cfdi_extras.report_imss_payslip_batch'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'partner_xlsx'

    def generate_xlsx_report(self, workbook, data, payslip_batches):
        for batche in payslip_batches:
            report_name = batche.name
            sheet = workbook.add_worksheet(report_name)
            bold = workbook.add_format({'bold': True})
            sheet.write(0, 0, 'Employee number', bold)
            sheet.write(0, 1, 'Employee name', bold)
            sheet.write(0, 2, 'Exedente 3 SMGDF', bold)
            sheet.write(0, 3, 'Prest. en dinero', bold)
            sheet.write(0, 4, 'Gastos médicos', bold)
            sheet.write(0, 5, 'Invalidez y Vida', bold)
            sheet.write(0, 6, 'Cesantia y vejez', bold)
            sheet.write(0, 7, 'IMSS trabajador', bold)
            sheet.write(0, 8, '', bold)
            sheet.write(0, 9, 'Cuota fija patronal', bold)
            sheet.write(0, 10, 'Exedente 3 SMGDF', bold)
            sheet.write(0, 11, 'Prest. en dinero', bold)
            sheet.write(0, 12, 'Gastos médicos', bold)
            sheet.write(0, 13, 'Riegso de trabajo', bold)
            sheet.write(0, 14, 'Invalidez y Vida', bold)
            sheet.write(0, 15, 'Guarderias y PS', bold)
            sheet.write(0, 16, 'Retiro', bold)
            sheet.write(0, 17, 'Cesantia y vejez', bold)
            sheet.write(0, 18, 'INFONAVIT', bold)
            sheet.write(0, 19, 'IMSS patron', bold)
           
            row_index = 1
            col_index=0
            slip_lines = batche.slip_ids
            for slip_line in slip_lines:
                if slip_line.state == 'cancel':
                    continue
                slip_line = slip_line.sudo()
                sheet.write(row_index, col_index, slip_line.employee_id.no_empleado)
                col_index+=1
                sheet.write(row_index, col_index, slip_line.employee_id.name)
                col_index+=1
                sheet.write(row_index, col_index, slip_line.emp_exedente_smg)
                col_index+=1
                sheet.write(row_index, col_index, slip_line.emp_prest_dinero)
                col_index+=1
                sheet.write(row_index, col_index, slip_line.emp_esp_pens)
                col_index+=1
                sheet.write(row_index, col_index, slip_line.emp_invalidez_vida)    
                col_index+=1
                sheet.write(row_index, col_index, slip_line.emp_cesantia_vejez)    
                col_index+=1
                sheet.write(row_index, col_index, slip_line.emp_total)    
                col_index=col_index+2
                sheet.write(row_index, col_index, slip_line.pat_cuota_fija_pat)    
                col_index+=1
                sheet.write(row_index, col_index, slip_line.pat_exedente_smg)    
                col_index+=1
                sheet.write(row_index, col_index, slip_line.pat_prest_dinero)    
                col_index+=1
                sheet.write(row_index, col_index, slip_line.pat_esp_pens)    
                col_index+=1
                sheet.write(row_index, col_index, slip_line.pat_riesgo_trabajo)    
                col_index+=1
                sheet.write(row_index, col_index, slip_line.pat_invalidez_vida)    
                col_index+=1
                sheet.write(row_index, col_index, slip_line.pat_guarderias)    
                col_index+=1
                sheet.write(row_index, col_index, slip_line.pat_retiro)    
                col_index+=1
                sheet.write(row_index, col_index, slip_line.pat_cesantia_vejez)    
                col_index+=1
                sheet.write(row_index, col_index, slip_line.pat_infonavit)    
                col_index+=1
                sheet.write(row_index, col_index, slip_line.pat_total)    
                row_index+=1
                col_index=0
                
