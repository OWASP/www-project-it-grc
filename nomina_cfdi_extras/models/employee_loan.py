# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta
from calendar import monthrange
import io
import xlwt
import itertools
from odoo.tools.misc import xlwt
import base64

class employee_loan(models.Model):
    _name = 'employee.loan'
    _inherit = 'mail.thread'
    _order = 'name desc'
    _description = 'employee_loan'
    
    file_data = fields.Binary("File Data")
    loan_state=[('draft','Borrador'),
               # ('request','Enviar petición'),
               # ('dep_approval','Aprobación del departamento'),
                ('hr_approval','Aprobado'),
                ('paid','Pagado'),
                ('done','Hecho'),
                ('close', 'Cerrar'),
                ('reject','Rechazar'),
                ('cancel','Cancelado')]
                
    @api.model
    def _get_employee(self):
        employee_id = self.env['hr.employee'].search([('user_id','=',self.env.user.id)],limit=1)
        return employee_id

    @api.model
    def _get_default_user(self):
        return self.env.user
    
    @api.model
    def nearest_date(self, items, pivot):
        return min(items, key=lambda x: abs(x - pivot))
    
    @api.model
    def get_quincenal_end_date(self,start_date, term):
        for i in range(0,term):
            if i!=0:
                date = start_date + relativedelta(days=i*15)
                month_last_day = monthrange(date.year,date.month)[1]
                items = [date+relativedelta(day=month_last_day), date+relativedelta(day=15)]
                previous_month_date = date+relativedelta(months=-1)
                previous_month_last_day = monthrange(previous_month_date.year,previous_month_date.month)[1]
                items.append(previous_month_date+relativedelta(day=previous_month_last_day),)
                if date.day>15:
                    items.append(date+relativedelta(months=1,day=15))
                end_date = self.nearest_date(items,date)
            else:
                end_date = start_date
        return end_date
    
    @api.depends('start_date','term')
    def _get_end_date(self):
        
        for loan in self:
            if loan.start_date and loan.loan_type_id:
                periodo_de_pago = loan.loan_type_id.periodo_de_pago or ''
                start_date =  loan.start_date #datetime.strptime(self.start_date, '%Y-%m-%d')
                
                if periodo_de_pago=='Semanal':
                    end_date = start_date+relativedelta(weeks=loan.term)
                elif periodo_de_pago=='Quincenal':
                    end_date = loan.get_quincenal_end_date(start_date, loan.term)
                else:
                    end_date = start_date+relativedelta(months=loan.term)
                loan.end_date = end_date.strftime("%Y-%m-%d")
            else:
               loan.end_date = datetime.today().strftime("%Y-%m-%d")

    name = fields.Char('Name',default='/',copy=False)
    state = fields.Selection(loan_state,string='Estado',default='draft', tracking=True)
    employee_id = fields.Many2one('hr.employee',string='Empleado',default=_get_employee, required="1")
    department_id = fields.Many2one('hr.department',string='Departamento')
#    hr_manager_id = fields.Many2one('hr.employee',string='Gerente RH')
#    manager_id = fields.Many2one('hr.employee',string='Gerente de departamento', required="1")
    job_id = fields.Many2one('hr.job',string="Puesto de trabajo")
    date = fields.Date('Fecha',default=fields.Date.today())
    start_date = fields.Date('Fecha de inicio',default=fields.Date.today(),required="1")
    end_date = fields.Date('Fecha de termino',compute='_get_end_date')
    term = fields.Integer('Plazos',required="1")
    loan_type_id = fields.Many2one('employee.loan.type',string='Tipo',required="1")
    payment_method = fields.Selection([('by_payslip','Nómina')],string='Método de pago',default='by_payslip', required="1")
    loan_amount = fields.Float('Monto de deducción',required="1")
    paid_amount = fields.Float('Monto de pago',compute='get_paid_amount')
    remaing_amount = fields.Float('Cantidad restante', compute='get_remaing_amount')
    installment_amount = fields.Float('Cantidad a plazos',required="1", compute='get_installment_amount')
    loan_url = fields.Char('URL', compute='get_loan_url')
    user_id = fields.Many2one('res.users',default=_get_default_user)
    is_apply_interest = fields.Boolean('Aplicar interés')
    interest_type = fields.Selection([('liner', 'Sobre monto total'), ('reduce', 'Sobre saldo pendiente')], string='Tipo de interés')
    interest_rate = fields.Float(string='Tasa de interés')
    interest_amount = fields.Float('Monto de interés', compute='get_interest_amount')
    # ins_interest_amount = fields.Float('Installment Interest Amount', compute='get_install_interest_amount')
    installment_lines = fields.One2many('installment.line','loan_id',string='Cuotas',)
    notes = fields.Text('Razón', required="1")
    is_close = fields.Boolean('Esta cerrado',compute='is_ready_to_close')
    move_id = fields.Many2one('account.move',string='Diario')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)

    @api.depends('remaing_amount')
    def is_ready_to_close(self):
        for loan in self:
            if loan.state == 'done':
               if loan.remaing_amount <= 0.01:
                   loan.is_close = True
               else:
                   loan.is_close = False
            else:
               loan.is_close = False

    @api.depends('installment_lines')
    def get_paid_amount(self):
        for loan in self:
            amt = 0
            for line in loan.installment_lines:
                if line.is_paid:
                    if line.is_skip:
                        amt += line.ins_interest
                    else:
                        amt += line.total_installment
                    
            loan.paid_amount = amt

    
    def compute_installment(self):
        vals=[]

        for i in range(0,self.term):
            date = self.start_date #datetime.strptime(self.start_date, '%Y-%m-%d')
            
            periodo_de_pago = self.loan_type_id.periodo_de_pago or ''
            if periodo_de_pago=='Semanal':
                date = date+relativedelta(weeks=i)
            elif periodo_de_pago=='Quincenal':
                if i!=0:
                    date = date+relativedelta(days=i*15)
                    month_last_day = monthrange(date.year,date.month)[1]
                    items = [date+relativedelta(day=month_last_day), date+relativedelta(day=15)]
                    previous_month_date = date+relativedelta(months=-1)
                    previous_month_last_day = monthrange(previous_month_date.year,previous_month_date.month)[1]
                    items.append(previous_month_date+relativedelta(day=previous_month_last_day),)
                    if date.day>15:
                        items.append(date+relativedelta(months=1,day=15))
                    date = self.nearest_date(items,date)
            else:
                date = date+relativedelta(months=i)
            
            amount = self.loan_amount
            interest_amount = 0.0
            ins_interest_amount=0.0
            if self.is_apply_interest:
                amount = self.loan_amount
                interest_amount = (amount  * self.interest_rate)/100 #* self.term/12

                if self.interest_rate and self.loan_amount and self.interest_type == 'reduce':
                    amount = self.loan_amount - self.installment_amount * i
                    interest_amount = (amount * self.term * self.interest_rate) / 100 # / 12
                ins_interest_amount = interest_amount / self.term
            vals.append((0, 0,{
                #'name':'INS - '+self.name+ ' - '+str(i+1),
                'name': self.name+ ' - '+str(i+1),
                'employee_id':self.employee_id and self.employee_id.id or False,
                'date':date,
                'amount':amount,
                'interest':interest_amount,
                'installment_amt':self.installment_amount,
                'ins_interest':ins_interest_amount,
                'tipo_deduccion': self.loan_type_id.tipo_deduccion,
            }))
        if self.installment_lines:
            for l in self.installment_lines:
                l.unlink()
        self.installment_lines=vals

    @api.depends('paid_amount','loan_amount')
    def get_remaing_amount(self):
        for loan in self:
            loan.remaing_amount = (loan.loan_amount + loan.interest_amount) - loan.paid_amount

    @api.depends('loan_amount') #,'interest_rate','is_apply_interest')
    def get_interest_amount(self):
        for loan in self:
            if loan.loan_type_id:
                if loan.loan_type_id.is_apply_interest:
                    if loan.interest_rate and loan.loan_amount and loan.loan_type_id.interest_type == 'liner':
                        loan.interest_amount = (loan.loan_amount  * loan.loan_type_id.interest_rate)/100 #* loan.term/12
                    if loan.interest_rate and loan.loan_amount and loan.loan_type_id.interest_type == 'reduce':
                        loan.interest_amount = (loan.remaing_amount  * loan.loan_type_id.interest_rate)/100 #* loan.term/12
                        amt=0.0
                        for line in loan.installment_lines:
                            amt += line.ins_interest
                        if amt:
                            loan.interest_amount = amt
                else:
                    loan.interest_amount = 0
            else:
                loan.interest_amount = 0

    # @api.depends('interest_amount')
    # def get_install_interest_amount(self):
    #     for loan in self:
    #         if loan.is_apply_interest:
    #             if loan.interest_amount and loan.term:
    #                 loan.ins_interest_amount = loan.interest_amount / loan.term

    @api.onchange('interest_type','interest_rate')
    def onchange_interest_rate_type(self):
        if self.interest_type and self.is_apply_interest:
            if self.interest_rate != self.loan_type_id.interest_rate:
                self.interest_rate = self.loan_type_id.interest_rate
            if self.interest_type != self.loan_type_id.interest_type:
                self.interest_type = self.loan_type_id.interest_type

    @api.depends('term')
    def get_loan_url(self):
        for loan in self:
            if loan.term:
                base_url = self.env['ir.config_parameter'].get_param('web.base.url', default='http://localhost:8069')
                if base_url:
                    base_url += '/web/login?db=%s&login=%s&key=%s#id=%s&model=%s' % (
                    self._cr.dbname, '', '', loan.id, 'employee.loan')
                    loan.loan_url = base_url
                else:
                    loan.loan_url = ''
            else:
                loan.loan_url = ''

    @api.depends('term','loan_amount')
    def get_installment_amount(self):
        for loan in self:
            if loan.loan_amount and loan.term:
                loan.installment_amount = loan.loan_amount / loan.term
            else:
                loan.installment_amount = 0.0

    @api.constrains('employee_id')
    def _check_loan(self):
        now = datetime.now()
        year = now.year
        s_date = str(year)+'-01-01'
        e_date = str(year)+'-12-01'
        
        loan_ids = self.search([('employee_id','=',self.employee_id.id),('date','<=',e_date),('date','>=',s_date)])
        loan = len(loan_ids)
        if loan > self.employee_id.loan_request:
            raise ValidationError("Puedes crear un máximo de %s de prestamo" % self.employee_id.loan_request)

    @api.constrains('loan_amount','term','loan_type_id','employee_id.loan_request')
    def _check_loan_amount_term(self):
        for loan in self:
            if loan.loan_amount <= 0:
                raise ValidationError("El monto del préstamo debe ser mayor de 0.00")
            elif loan.loan_amount > loan.loan_type_id.loan_limit:
                raise ValidationError("Usted solo puede solicitar el %s del préstamo" % loan.loan_type_id.loan_limit)

            if loan.term <= 0:
                raise ValidationError("El plazo del préstamos debe ser mayor de 0.00")
            elif loan.term > loan.loan_type_id.loan_term:
                raise ValidationError("El límite del plazo del préstamo para su prestamo es de %s meses" % loan.loan_type_id.loan_term)

    @api.onchange('loan_type_id')
    def _onchange_loan_type(self):
        if self.loan_type_id:
            self.term = self.loan_type_id.loan_term
            self.is_apply_interest = self.loan_type_id.is_apply_interest
            if self.is_apply_interest:
                self.interest_rate = self.loan_type_id.interest_rate
                self.interest_type = self.loan_type_id.interest_type

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        if self.employee_id:
            self.department_id = self.employee_id and self.employee_id.department_id and \
                                 self.employee_id.department_id.id or False,

#            self.manager_id = self.department_id and self.department_id.manager_id and \
#                                  self.department_id.manager_id.id or self.employee_id.parent_id.id or False,

            self.job_id = self.employee_id.job_id and self.employee_id.job_id.id or False,

    
    def action_send_request(self):
        self.state = 'hr_approval'
        if not self.installment_lines:
            self.compute_installment()
    
    def dep_manager_approval_loan(self):
        self.state = 'dep_approval'

    
    def hr_manager_approval_loan(self):
        self.state = 'hr_approval'

    
    def dep_manager_reject_loan(self):
        self.state = 'reject'

    
    def action_close_loan(self):
        self.state = 'close'

    
    def hr_manager_reject_loan(self):
        self.state = 'reject'


    
    def cancel_loan(self):
        self.state = 'cancel'

    
    def set_to_draft(self):
        self.state = 'draft'
#        self.hr_manager_id = False

    
    def paid_loan(self):
        if self.loan_type_id.tipo_deduccion == '1':
           if not self.employee_id.address_home_id:
               raise ValidationError(_('Para realizar un préstamo el empleado debe tener una dirección asignada'))

           self.state = 'paid'
           vals={
               'date':self.date,
               'ref':self.name,
               'journal_id':self.loan_type_id.journal_id and self.loan_type_id.journal_id.id,
               'company_id':self.env.user.company_id.id
           }
           acc_move_id = self.env['account.move'].create(vals)
           lst = []
           lst.append((0,0,{
                           'account_id':self.loan_type_id and self.loan_type_id.loan_account.id,
                           'partner_id':self.employee_id.address_home_id and self.employee_id.address_home_id.id or False,
                           'name':self.name,
                           'credit':self.loan_amount or 0.0,
                       }))

           if self.interest_amount:
               lst.append((0,0,{
                               'account_id':self.loan_type_id and self.loan_type_id.interest_account.id,
                               'partner_id':self.employee_id.address_home_id and self.employee_id.address_home_id.id or False,
                               'name':str(self.name)+' - '+'Interes',
                               'credit':self.interest_amount or 0.0,
                           }))

           credit_account=False
           if self.employee_id.address_home_id and self.employee_id.address_home_id.property_account_payable_id:
               credit_account = self.employee_id.address_home_id.property_account_payable_id.id or False
                    
           debit_amount = self.loan_amount
           if self.interest_amount:
               debit_amount += self.interest_amount

           lst.append((0,0,{
                           'account_id':credit_account or False,
                           'partner_id':self.employee_id.address_home_id and self.employee_id.address_home_id.id or False,
                           'name':'/',
                           'debit':debit_amount  or 0.0,
                       }))
           acc_move_id.line_ids = lst
           if acc_move_id:
               self.move_id = acc_move_id.id
        else:
           self.state = 'paid'


    
    def view_journal_entry(self):
        if self.move_id:
            return {
                'view_mode': 'form',
                'res_id': self.move_id.id,
                'res_model': 'account.move',
                'view_type': 'form',
                'type': 'ir.actions.act_window',
            }

    
    def action_done_loan(self):
        self.state = 'done'
        
    @api.model
    def init(self):
        company_id = self.env['res.company'].search([])
        for company in company_id:
            employee_loan_sequence = self.env['ir.sequence'].search([('code', '=', 'employee.loan'), ('company_id', '=', company.id)])
            if not employee_loan_sequence:
                employee_loan_sequence.create({
                        'name': 'Secuencia de prestamo',
                        'code': 'employee.loan',
                        'prefix': 'PRES/',
                        'padding': 4,
                        'company_id': company.id,
                    })

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_company(vals['company_id']).next_by_code(
                    'employee.loan') or '/'
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'employee.loan') or '/'
        return super(employee_loan, self).create(vals)

    
    def copy(self, default=None):
        if default is None:
            default = {}
        default['name'] = '/'
        return super(employee_loan, self).copy(default=default)

    
    def unlink(self):
        for loan in self:
            if loan.state != 'draft':
                raise ValidationError(_('El préstamo solo se puede eliminar si está en estaado de borrador'))
        return super(employee_loan,self).unlink()

    
    def xls_generate_for_employee_loans(self):
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Reporte de préstamos')
        col_width = 256 * 20
        try:
            for i in itertools.count():
                worksheet.col(i).width = col_width
        except ValueError:
            pass
        bold = xlwt.easyxf("font: bold on;")
        
        worksheet.write(0, 0, 'Numero de empleado', bold)
        worksheet.write(0, 1, 'Nombre de empleado', bold)
        worksheet.write(0, 2, 'Status', bold)
        worksheet.write(0, 3, 'Monto de deducción', bold)
        worksheet.write(0, 4, 'Monto de pago', bold)
        worksheet.write(0, 5, 'Cantidad restante', bold)
        worksheet.write(0, 6, 'Tipo', bold)
        worksheet.write(0, 7, 'Referencia', bold)
        worksheet.write(0, 8, 'Cantidad a plazos', bold)
        worksheet.write(0, 9, 'Fecha de incio', bold)
        
        employee_loans = self.env['employee.loan'].search([], order="employee_id")
        if not employee_loans:
            return
        
        row = 1
        for emp_loan in employee_loans:
            numero_de_empleado = emp_loan.employee_id.no_empleado or ''
            nombre_de_empleado = emp_loan.employee_id.name or ''
            status = 'P' if emp_loan.remaing_amount == 0 else 'N'
            monto_de_deduccion = emp_loan.loan_amount or ''
            monto_de_pago = emp_loan.paid_amount or ''
            cantidad_restante = emp_loan.remaing_amount or ''
            tipo = emp_loan.loan_type_id and emp_loan.loan_type_id.name or ''
            referencia = emp_loan.name or ''
            cantidad_a_plazos = round(emp_loan.installment_amount,2) or ''
            fecha_de_incio = emp_loan.start_date and emp_loan.start_date.strftime("%m/%d/%Y") or ''
            
            worksheet.write(row, 0, numero_de_empleado)
            worksheet.write(row, 1, nombre_de_empleado)
            worksheet.write(row, 2, status)
            worksheet.write(row, 3, monto_de_deduccion)
            worksheet.write(row, 4, monto_de_pago)
            worksheet.write(row, 5, cantidad_restante)
            worksheet.write(row, 6, tipo)
            worksheet.write(row, 7, referencia)
            worksheet.write(row, 8, cantidad_a_plazos)
            worksheet.write(row, 9, fecha_de_incio)
            row += 1
        
        fp = io.BytesIO()
        workbook.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        
        employee_loans[0].write({'file_data':base64.b64encode(data)})
        action = {
            'name': 'Reporte de préstamos',
            'type': 'ir.actions.act_url',
            'url': "/web/content/?model="+self._name+"&id=" + str(employee_loans[0].id) + "&field=file_data&download=true&filename=reporte_de_prestamos.xls",
            'target': 'self',
            }
        return action


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
