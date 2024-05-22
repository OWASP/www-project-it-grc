# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import xlwt
from xlwt import easyxf
import io
from docutils.nodes import line
from odoo.exceptions import UserError, Warning

class Payslip(models.Model):
    _inherit = 'hr.payslip'

    def get_amount_from_rule_code(self, rule_code):
        for slip in self:
            for line in slip.line_ids:
                if line.code == rule_code:
                   return round(line.total,2)
            return 0.0

    def get_total_work_days(self):
        total = 0
        for line in self.worked_days_line_ids:
            if line.code == 'WORK100' or line.code == 'FJC' or line.code == 'SEPT':
               total += line.number_of_days
        return total
    
    def get_total_code_value(self,special_code):
        line_ids = self.line_ids.filtered(lambda l: l.salary_rule_id.forma_pago == special_code)
        total = 0.0
        for line in line_ids:
            if line.salary_rule_id.category_id.code == 'ALW' or line.salary_rule_id.category_id.code == 'ALW3' or line.salary_rule_id.category_id.code == 'BASIC':
               total += line.total or 0.0
            elif line.salary_rule_id.category_id.code == 'DED':
               total -= line.total or 0.0
        line2_ids = self.line_ids.filtered(lambda l: l.salary_rule_id.category_id.code == 'AUX')
        for line2 in line2_ids:
             if line2.salary_rule_id.fondo_ahorro_aux and special_code == '001':
               total -= line2.total or 0.0
#             if line2.salary_rule_id.fondo_ahorro_aux and special_code == '002':
#               total += line2.total or 0.0
        return total
    
class PayslipBatches(models.Model):
    _inherit = 'hr.payslip.run'

    file_data = fields.Binary('File')

    
    def get_department(self):
        result = {}
        department = self.env['hr.department'].search([])
        for dept in department:
            result[dept.id] = dept.name
        return result

    
    def get_dept_total(self, dept_id):
        result = {}
        for rule in self.env['hr.salary.rule'].search([]):
            result[rule.code] = 0
        for payslip in self.slip_ids:
            if payslip.employee_id.department_id.id == dept_id and payslip.state != "cancel":
                for line in payslip.line_ids:
                    if line.code in result.keys():
                        result[line.code] = round(line.total + result.get(line.code), 2)
                    else:
                        result[line.code] = round(line.total, 2)
        return result

    
    def get_grand_total(self):
        result = {}
        for rule in self.env['hr.salary.rule'].search([]):
            result[rule.code] = 0
        for payslip in self.slip_ids:
            if payslip.state != "cancel":
                for line in payslip.line_ids:
                   if line.code in result.keys():
                       result[line.code] = round(line.total + result.get(line.code), 2)
                   else:
                       result[line.code] = round(line.total, 2)
        return result
    
    def get_payslip_group_by_department(self):
        result = {}
        start_range = self._context.get('start_range')
        end_range = self._context.get('end_range')
        if start_range and end_range:
            slips = self.env['hr.payslip'].browse()
            for slip in self.slip_ids:
                try:
                    if slip.employee_id.no_empleado:
                        emp_no = eval(slip.employee_id.no_empleado)
                except Exception as e:
                    continue
                if type(emp_no) not in (float,int):
                    continue
                if emp_no >= start_range and emp_no <= end_range:
                    slips += slip
            
        else:
            slips = self.slip_ids
        for line in slips:
            if line.employee_id.department_id.id in result.keys():
                result[line.employee_id.department_id.id].append(line)
            else:
                result[line.employee_id.department_id.id] = [line]
        return result

   
    def get_all_columns(self):
        result = {}
        all_col_list_seq = []
        start_range = self._context.get('start_range')
        end_range = self._context.get('end_range')
        if self.slip_ids:
            if start_range and end_range:
                slips = self.env['hr.payslip'].browse()
                for slip in self.slip_ids:
                    try:
                        if slip.employee_id.no_empleado:
                            emp_no = eval(slip.employee_id.no_empleado)
                    except Exception as e:
                        continue
                    if type(emp_no) not in (float,int):
                        continue
                    if emp_no >= start_range and emp_no <= end_range:
                        slips += slip
            else:
                slips = self.slip_ids
            for line in slips.mapped('line_ids').sorted(lambda x:x.sequence):
                if line.code not in all_col_list_seq:
                    all_col_list_seq.append(line.code)
                if line.code not in result.keys():
                    result[line.code] = line.name
#         for payslip in self.slip_ids:
#             for line in payslip.line_ids:
#                 if line.code not in result.keys():
#                     result[line.code] = line.name
        return [result, all_col_list_seq]

    def export_report_xlsx_button(self):
        view = self.env.ref('nomina_cfdi_extras.listado_de_monin_wizard')
        ctx = self.env.context.copy()
        ctx .update({'default_payslip_batch_id':self.id})
        return {
            'name': 'Listado De Nomina',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'listado.de.monina',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': ctx,
        }
       
    def export_report_xlsx(self):
        import base64
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Listado de nomina')
        header_style = easyxf('font:height 200; align: horiz center; font:bold True;' "borders: top thin,left thin,right thin,bottom thin")
        text_bold_left = easyxf('font:height 200; font:bold True; align: horiz left;' "borders: top thin,bottom thin")
        text_left = easyxf('font:height 200; align: horiz left;' "borders: top thin,bottom thin")
        text_right = easyxf('font:height 200; align: horiz right;' "borders: top thin,bottom thin")
        text_bold_right = easyxf('font:height 200;font:bold True; align: horiz right;' "borders: top thin,bottom thin")
        worksheet.write(0, 0, 'Cod', header_style)
        worksheet.write(0, 1, 'Empleado', header_style)
        worksheet.write(0, 2, 'Dias Pag', header_style)
        col_nm = 3

        noms = self.slip_ids
        for nom in noms:
            if not nom.employee_id.department_id:
                raise UserError(_('%s no tiene departamento configurado') % (nom.employee_id.name))

        all_column = self.get_all_columns()
        all_col_dict = all_column[0]
        all_col_list = all_column[1]
        for col in all_col_list:
            worksheet.write(0, col_nm, all_col_dict[col], header_style)
            col_nm += 1
        for t in ['Total Efectivo', 'Total Especie']:
            worksheet.write(0, col_nm, t, header_style)
            col_nm += 1

        payslip_group_by_department = self.get_payslip_group_by_department()
        row = 1
        grand_total = {}
        for dept in self.env['hr.department'].browse(payslip_group_by_department.keys()).sorted(lambda x:x.name):
            row += 1
            worksheet.write_merge(row, row, 0, 2, dept.name, text_bold_left)
            total = {}
            row += 1
            slip_sorted_by_employee={}
            hr_payslips=[]
            value = 1
            for slip in payslip_group_by_department[dept.id]:
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
            for slip in hr_payslips:
                if slip.state == "cancel":
                    continue
                if slip.employee_id.no_empleado:
                    worksheet.write(row, 0, slip.employee_id.no_empleado, text_left)
                worksheet.write(row, 1, slip.employee_id.name, text_left)
                work_day = slip.get_total_work_days()
                worksheet.write(row, 2, work_day, text_right)
                code_col = 3
                for code in all_col_list:
                    amt = 0
                    if code in total.keys():
                        for line in slip.details_by_salary_rule_category:
                           if line.code == code:
                               amt = round(line.total,2)
#                        amt = slip.get_amount_from_rule_code(code)
#                        if amt:
                               grand_total[code] = grand_total.get(code) + amt
                               total[code] = total.get(code) + amt
                    else:
                        #amt = slip.get_amount_from_rule_code(code)
                        for line in slip.details_by_salary_rule_category:
                           if line.code == code:
                               amt = round(line.total,2)
                               total[code] = amt or 0
                        if code in grand_total.keys():
                            grand_total[code] = amt + grand_total.get(code) or 0.0
                        else:
                            grand_total[code] = amt or 0
                    worksheet.write(row, code_col, amt, text_right)
                    code_col += 1
                worksheet.write(row, code_col, slip.get_total_code_value('001'), text_right)
                code_col += 1
                worksheet.write(row, code_col, slip.get_total_code_value('002'), text_right)
                row += 1
            worksheet.write_merge(row, row, 0, 2, 'Total Departamento', text_bold_left)
            code_col = 3
            for code in all_col_list:
                worksheet.write(row, code_col, total.get(code), text_bold_right)
                code_col += 1
        row += 1
        worksheet.write_merge(row, row, 0, 2, 'Gran Total', text_bold_left)
        code_col = 3
        for code in all_col_list:
            worksheet.write(row, code_col, grand_total.get(code), text_bold_right)
            code_col += 1

        fp = io.BytesIO()
        workbook.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        self.write({'file_data': base64.b64encode(data)})
        action = {
            'name': 'Journal Entries',
            'type': 'ir.actions.act_url',
            'url': "/web/content/?model=hr.payslip.run&id=" + str(self.id) + "&field=file_data&download=true&filename=Listado_de_nomina.xls",
            'target': 'self',
            }
        return action
