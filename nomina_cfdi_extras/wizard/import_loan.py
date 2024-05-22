# -*- coding: utf-8 -*-

from odoo import models,api, fields
import base64
import xlrd
from datetime import datetime


class import_loan(models.TransientModel):
    _name = "import.loan"
    _description = 'import_loan'
    
    file_type = fields.Selection([('excel','Excel'),('csv','CSV')],string='Tipo de archivo', default='csv')
    csv_file = fields.Binary(string='Archivo')
    
   
    def get_employee_id(self,name):
        emp_id = self.env['hr.employee'].search([('name','=',name)],limit=1)
        if emp_id:
            return emp_id
        else:
            return False
            
   
    def get_loan_type(self,name):
        type_id = self.env['employee.loan.type'].search([('name','=',name)],limit=1)
        if type_id:
            return type_id
        else:
            return False
    
    
   
    def add_in_remark(self,remark,coment):
        if remark:
            remark += ' , '+ coment
        else:
            remark = coment
        return remark
        
   
    def get_check_employee_loan(self,employee_id):
        now = datetime.now()
        year = now.year
        s_date = str(year)+'-01-01'
        e_date = str(year)+'-12-01'
        loan_ids = self.env['employee.loan'].search([('employee_id','=',employee_id.id),('date','<=',e_date),('date','>=',s_date)])
        return len(loan_ids)
        
        
    
   
    def import_loan(self):
        lines =[]
        if self.file_type == 'csv':
            file_data = base64.decodestring(self.csv_file)
            csv_data = str(file_data.decode("utf-8")) 
            csv_data = csv_data.split('\n')
            for csv_line in csv_data:
                if csv_line:
                    lines.append(csv_line.split(','))
            lines.pop(0)
        else:
            file_datas = base64.decodestring(self.csv_file) 
            workbook = xlrd.open_workbook(file_contents=file_datas)
            sheet = workbook.sheet_by_index(0)
            lines = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
            lines.pop(0)
            
        count = 1
        logs = ''
        for line in lines:
            count += 1
            remark =''
            employee_id = self.get_employee_id(line[0])
            if not employee_id:
                remark = self.add_in_remark(remark,'Employee')
            else:
                emp_loan = self.get_check_employee_loan(employee_id)
                if emp_loan >= employee_id.loan_request:
                    remark = self.add_in_remark(remark,'Employee Can not create more then '+ str(employee_id.loan_request))+' Loans'
                
            manager_id = self.get_employee_id(line[1])
            if not manager_id:
                remark = self.add_in_remark(remark,'Departnent Manager')
                
            loan_type_id = self.get_loan_type(line[3])
            if not loan_type_id:
                remark = self.add_in_remark(remark,'Loan type')
            if not remark:
                res ={
                    'employee_id':employee_id.id,
                    'manager_id':manager_id.id,
                    'job_id':employee_id.job_id and employee_id.job_id.id or False,
                    'department_id':employee_id.department_id and employee_id.department_id.id or False,
                    'payment_method':'by_payslip',
                    'loan_amount':line[2],
                    'loan_type_id':loan_type_id.id,
                    'start_date':line[4],
                    'term':loan_type_id.loan_term,
                    'interest_rate':loan_type_id.interest_rate,
                    'interest_type':loan_type_id.interest_type,
                    'notes':line[5],
                }
                self.env['employee.loan'].create(res)
            else:
                remark = 'Line No:'+str(count)+' '+remark+' Not Match \n'
                logs += remark
        
        
        if logs:
            log_id=self.env['import.logs'].create({'name':logs})
            return {
                'view_mode': 'form',
                'res_id': log_id.id,
                'res_model': 'import.logs',
                'view_type': 'form',
                'type': 'ir.actions.act_window',
                'target': 'new',
            }
                
                    
                
                
                
                
        

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
