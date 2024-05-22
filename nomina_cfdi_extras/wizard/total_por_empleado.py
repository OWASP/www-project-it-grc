# -*- coding: utf-8 -*-

from odoo import models, fields, api
import xlwt
from xlwt import easyxf
import io
from docutils.nodes import line
import base64
import string

class TotalPorEmpleado(models.TransientModel):
    _name = 'total.por.empleado'
    _description = 'Total por empleado'

    hr_payslip_run_ids = fields.Many2many('hr.payslip.run',string="Procesamientos de nómina")
    file_data = fields.Binary()
    payslip_batch_id = fields.Many2one('hr.payslip.run','Payslip Run')
    def print_total_por_empleado_report(self):
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Total por empleado')
        header_style = easyxf('font:height 200; align: horiz center; font:bold True;' "borders: top thin,left thin,right thin,bottom thin")
        text_bold_left = easyxf('font:height 200; font:bold True; align: horiz left;' "borders: top thin,bottom thin")
        text_left = easyxf('font:height 200; align: horiz left;' "borders: top thin,bottom thin")
        text_right = easyxf('font:height 200; align: horiz right;' "borders: top thin,bottom thin")
        text_bold_right = easyxf('font:height 200;font:bold True; align: horiz right;' "borders: top thin,bottom thin")
        worksheet.write(0, 0, 'Cod', header_style)
        worksheet.write(0, 1, 'Empleado', header_style)
        worksheet.write(0, 2, 'Puesto', header_style)
        worksheet.write(0, 3, 'Departamento', header_style)
        col_nm = 4
        if self.hr_payslip_run_ids:
            result = {}
            all_col_list_seq = []
            employee={} 
            rule = {}
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
            row = 1
            hr_payslips = self.hr_payslip_run_ids.slip_ids
            hr_payslips=sorted(hr_payslips, key=lambda x: int(x.employee_id.no_empleado), reverse=False)
            for slip in hr_payslips:
                row+=1
                if slip.state == "cancel":
                    continue
#                if slip.employee_id.no_empleado:
#                    print(slip.employee_id.no_empleado)
                work_day = slip.get_total_work_days()
                rule = {}
                for code in all_col_list_seq:
                    if slip.employee_id.no_empleado:
                        rule.update({code:0.0,'puesto':slip.employee_id.job_title,'no_empleado':slip.employee_id.no_empleado,'employee_name':slip.employee_id.name,'depto':slip.employee_id.department_id.name,})
                    else:
                        rule.update({code:0.0,'puesto':slip.employee_id.job_title,'no_empleado':slip.employee_id.no_empleado,'employee_name':'','depto':slip.employee_id.department_id.name,})
                if not slip.details_by_salary_rule_category:
                    if not slip.employee_id.id in employee:
                        employee.update({slip.employee_id.id:{}})
                        employee[slip.employee_id.id] = dict(rule)
                for line in slip.details_by_salary_rule_category:
                    if not slip.employee_id.id in employee:
                        employee.update({slip.employee_id.id:{}})
                        employee[slip.employee_id.id] = dict(rule)
                    if line.code not in employee[slip.employee_id.id]:
                        employee[slip.employee_id.id][line.code] = line.amount
                    else:
                        employee[slip.employee_id.id][line.code] += line.amount
            row=2
            col=0
            for employee_wise,datas in employee.items():
                worksheet.write(row, col, datas.get('no_empleado'), text_left)
                col+=1
                worksheet.write(row, col, datas.get('employee_name'), text_left)
                col+=1
                worksheet.write(row, col, datas.get('puesto'), text_right)
                col+=1
                worksheet.write(row, col, datas.get('depto'), text_right)
                col+=1
                for rule_name in all_col_list_seq:
                    worksheet.write(row, col, datas.get(rule_name), text_right)
                    col+= 1 
                worksheet.write(row,col, slip.get_total_code_value('001'), text_right)
                col += 1
                worksheet.write(row,col, slip.get_total_code_value('002'), text_right)
                row+=1
                col = 0
        code_col = 4
        count=2
        count_alpha=4
        flag = False
        j=1
        i=1
        for code in all_col_list_seq:
            if count_alpha==26:
                flag=True
            if flag==True:
                if j==27:
                    i+=1
                    j=1 
                for col_name_start in range(0,i):
                    alpha_str = string.ascii_uppercase[col_name_start]
                for col_name in range(0,j):
                    alpha_to_str = string.ascii_uppercase[col_name]
                new_col = alpha_str+alpha_to_str
                sum = "SUM("+new_col+str(count)+":" +new_col+ "%d)"
                j+=1
            if flag == False :
                row_aplha=string.ascii_uppercase[count_alpha]
                sum = "SUM("+row_aplha+str(count)+":" +row_aplha+ "%d)"
            worksheet.write(row, code_col ,xlwt.Formula(sum %(row)), text_bold_right)
            code_col+=1
            count_alpha+=1
        fp = io.BytesIO()
        workbook.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        self.write({'file_data': base64.b64encode(data)})
        action = {
            'name': 'Total por empleado',
            'type': 'ir.actions.act_url',
            'url': "/web/content/?model=total.por.empleado&id=" + str(self.id) + "&field=file_data&download=true&filename=total_por_empleado.xls",
            'target': 'self',
            }
        return action
