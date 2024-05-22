# -*- coding: utf-8 -*-

from odoo import models, fields, api
import xlwt
from xlwt import easyxf
import io
from docutils.nodes import line
import base64
class TotalPorDepartamento(models.TransientModel):
    _name = 'total.por.departamento'
    _description = 'Total por departamento'

    hr_payslip_run_ids = fields.Many2many('hr.payslip.run',string="Procesamientos de nómina")
    file_data = fields.Binary()
    payslip_batch_id = fields.Many2one('hr.payslip.run','Payslip Run')

    def print_total_por_departamento_report(self):
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Total por empleado')
        header_style = easyxf('font:height 200; align: horiz center; font:bold True;' "borders: top thin,left thin,right thin,bottom thin")
        text_bold_left = easyxf('font:height 200; font:bold True; align: horiz left;' "borders: top thin,bottom thin")
        text_left = easyxf('font:height 200; align: horiz left;' "borders: top thin,bottom thin")
        text_right = easyxf('font:height 200; align: horiz right;' "borders: top thin,bottom thin")
        text_bold_right = easyxf('font:height 200;font:bold True; align: horiz right;' "borders: top thin,bottom thin")
        worksheet.write(0, 0, 'Cod', header_style)
        worksheet.write(0, 1, 'Empleado', header_style)
        worksheet.write(0, 2, 'Dias Pag', header_style)
        col_nm = 3
        if self.hr_payslip_run_ids:
            #hr_payslip_line_ids=self.hr_payslip_run_ids.slip_ids.details_by_salary_rule_category
            result = {}
            all_col_list_seq = []
            for line in self.hr_payslip_run_ids.slip_ids.mapped('line_ids').sorted(lambda x:x.sequence):
                if line.code not in all_col_list_seq:
                    all_col_list_seq.append(line.code)
                if line.code not in result.keys():
                    result[line.code] = line.name
            for col in all_col_list_seq:
                worksheet.write(0, col_nm, result[col], header_style)
                col_nm += 1
            for t in ['Total Efectivo', 'Total Especie']:
                worksheet.write(0, col_nm, t, header_style)
                col_nm += 1    
            result_department={}        
            for line in self.hr_payslip_run_ids.slip_ids:
                if line.employee_id.department_id.id in result_department.keys():
                    result_department[line.employee_id.department_id.id].append(line)
                else:
                    result_department[line.employee_id.department_id.id] = [line]
            row = 1
            grand_total = {}
            for dept in self.env['hr.department'].browse(result_department.keys()).sorted(lambda x:x.name):
                #row += 1
                #worksheet.write_merge(row, row, 0, 2, dept.name, text_bold_left)
                total = {}
                row += 1
                slip_sorted_by_employee={}
                hr_payslips=[]
                value = 1
                for slip in result_department[dept.id]:
                    if slip.employee_id and not slip.employee_id.no_empleado in slip_sorted_by_employee.values():
                        slip_sorted_by_employee[slip.id]=slip.employee_id.no_empleado or '0'
                    else:
                        slip_sorted_by_employee[slip.id]=slip.employee_id.no_empleado + str(value) or '0' + str(value)
                        value += 1
                for values in sorted(slip_sorted_by_employee.values()):
                    val_list = list(slip_sorted_by_employee.values())
                    key_list = list(slip_sorted_by_employee.keys())
                    slip = key_list[val_list.index(values)]
                    hr_payslips.append(self.env['hr.payslip'].browse(slip))
                hr_payslips=sorted(hr_payslips, key=lambda x: int(x.employee_id.no_empleado), reverse=False)
                for slip in hr_payslips:
                    if slip.state == "cancel":
                        continue
#                     if slip.employee_id.no_empleado:
#                         print(slip.employee_id.no_empleado)
#                         worksheet.write(row, 0, slip.employee_id.no_empleado, text_left)
                    #worksheet.write(row, 1, slip.employee_id.name, text_left)
                    work_day = slip.get_total_work_days()
                    #worksheet.write(row, 2, work_day, text_right)
                    code_col = 3
                    for code in all_col_list_seq:
                        amt = 0  
                        if code in total.keys():
                            for line in slip.details_by_salary_rule_category:
                                if line.code == code:
                                    amt = line.total
    #                        amt = slip.get_amount_from_rule_code(code)
    #                        if amt:
                                    grand_total[code] = grand_total.get(code) + amt
                                    total[code] = total.get(code) + amt
                        else:
                            #amt = slip.get_amount_from_rule_code(code)
                            for line in slip.details_by_salary_rule_category:
                                if line.code == code:
                                    amt = line.total
                                    total[code] = amt or 0
                            if code in grand_total.keys():
                                grand_total[code] = amt + grand_total.get(code) or 0.0
                            else:
                                grand_total[code] = amt or 0
                        #worksheet.write(row, code_col, amt, text_right)
                        #code_col += 1  
                    #worksheet.write(row, code_col, slip.get_total_code_value('001'), text_right)
                    #code_col += 1
                    #worksheet.write(row, code_col, slip.get_total_code_value('002'), text_right)
                    #row += 1
                worksheet.write_merge(row, row, 0, 2, dept.name, text_left)
                code_col = 3
                for code in all_col_list_seq:
                    worksheet.write(row, code_col, total.get(code), text_right)
                    code_col += 1 
        row += 1
        worksheet.write_merge(row, row, 0, 2, 'Gran Total', text_bold_left)
        code_col = 3
        for code in all_col_list_seq:
            worksheet.write(row, code_col, grand_total.get(code), text_bold_right)
            code_col += 1
                           
        fp = io.BytesIO()
        workbook.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        self.write({'file_data': base64.b64encode(data)})
        action = {
            'name': 'Total por departamento',
            'type': 'ir.actions.act_url',
            'url': "/web/content/?model=total.por.departamento&id=" + str(self.id) + "&field=file_data&download=true&filename=total_por_departamento.xls",
            'target': 'self',
            }
        return action
