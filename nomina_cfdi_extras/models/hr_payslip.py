# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval as eval

class hr_payslip(models.Model):
    _inherit = 'hr.payslip'
    
    installment_ids = fields.Many2many('installment.line',string='Pŕestamos')
    installment_amount = fields.Float('Monto Pŕestamo',compute='get_installment_amount')
    installment_int = fields.Float('Interés Péstamo',compute='get_installment_amount')
    descuento1_amount = fields.Float('Monto descuento 1',compute='get_descuento1_amount')
    descuento1_int = fields.Float('Interés descuento 1',compute='get_descuento1_amount')
    descuento2_amount = fields.Float('Monto descuento 2',compute='get_descuento2_amount')
    descuento2_int = fields.Float('Interés descuento 2',compute='get_descuento2_amount')
    descuento3_amount = fields.Float('Monto descuento 3',compute='get_descuento3_amount')
    descuento3_int = fields.Float('Interés descuento 3',compute='get_descuento3_amount')
    descuento4_amount = fields.Float('Monto descuento 4',compute='get_descuento4_amount')
    descuento4_int = fields.Float('Interés descuento 4',compute='get_descuento4_amount')
    descuento5_amount = fields.Float('Monto descuento 5',compute='get_descuento5_amount')
    descuento5_int = fields.Float('Interés descuento 5',compute='get_descuento5_amount')
    descuento6_amount = fields.Float('Monto descuento 6',compute='get_descuento6_amount')
    descuento6_int = fields.Float('Interés descuento 6',compute='get_descuento6_amount')
    descuento7_amount = fields.Float('Monto descuento 7',compute='get_descuento7_amount')
    descuento7_int = fields.Float('Interés descuento 7',compute='get_descuento7_amount')
    descuento8_amount = fields.Float('Monto descuento 8',compute='get_descuento8_amount')
    descuento8_int = fields.Float('Interés descuento 8',compute='get_descuento8_amount')
    descuento9_amount = fields.Float('Monto descuento 9',compute='get_descuento9_amount')
    descuento9_int = fields.Float('Interés descuento 9',compute='get_descuento9_amount')
    descuento10_amount = fields.Float('Monto descuento 10',compute='get_descuento10_amount')
    descuento10_int = fields.Float('Interés descuento 10',compute='get_descuento10_amount')
    descuento11_amount = fields.Float('Monto descuento 11',compute='get_descuento11_amount')
    descuento11_int = fields.Float('Interés descuento 11',compute='get_descuento11_amount')
    descuento12_amount = fields.Float('Monto descuento 12',compute='get_descuento12_amount')
    descuento12_int = fields.Float('Interés descuento 12',compute='get_descuento12_amount')
    descuento13_amount = fields.Float('Monto descuento 13',compute='get_descuento13_amount')
    descuento13_int = fields.Float('Interés descuento 13',compute='get_descuento13_amount')
    descuento14_amount = fields.Float('Monto descuento 14',compute='get_descuento14_amount')
    descuento14_int = fields.Float('Interés descuento 14',compute='get_descuento14_amount')
    descuento15_amount = fields.Float('Monto descuento 15',compute='get_descuento15_amount')
    descuento15_int = fields.Float('Interés descuento 15',compute='get_descuento15_amount')
    rp_dias_completos = fields.Float('dias completos', compute='get_dias_completos')
    rp_dias_laborados = fields.Float('dias laborados', compute='get_dias_laborados')
    rp_dias_periodo = fields.Float('dias periodo', compute='get_dias_periodo')
    rp_gravado = fields.Float('gravado', compute='get_gravado')
    rp_limite_inferior = fields.Float('rp_limite_inferior', compute='get_tablas_values')
    rp_cuota_fija = fields.Float('rp_cuota_fija', compute='get_tablas_values')
    rp_porcentaje = fields.Float('rp_porcentaje', compute='get_tablas_values')
    rp_subsidio = fields.Float('rp_subsidio', compute='get_tablas_values')
    retardo = fields.Boolean(string=_('Retardo'), compute='_get_retardo', default = False)

    
    def compute_sheet(self):
        for data in self:
          if data.concepto_periodico and data.aplicar_descuentos:
              if data.nom_liquidacion:
                 installment_ids = data.env['installment.line'].search(
                      [('employee_id', '=', data.employee_id.id), ('loan_id.state', '=', 'done'),
                       ('is_paid', '=', False)])
              else:
                 installment_ids = data.env['installment.line'].search(
                      [('employee_id', '=', data.employee_id.id), ('loan_id.state', '=', 'done'),
                       ('is_paid', '=', False),('date','<=',data.date_to)])
              if installment_ids:
                  data.installment_ids = [(6, 0, installment_ids.ids)]
          else:
              data.installment_ids = [(6, 0, [])]
        return super(hr_payslip,self).compute_sheet()
    
#    
#    def compute_sheet(self):
#        installment_ids = self.env['installment.line'].search(
#                [('employee_id', '=', self.employee_id.id), ('loan_id.state', '=', 'done'),
#                 ('is_paid', '=', False),('date','<=',self.date_to)])
#        if installment_ids:
#            self.installment_ids = [(6, 0, installment_ids.ids)]
#        return super(hr_payslip,self).compute_sheet()
        

    @api.depends('installment_ids')
    def get_installment_amount(self):
        for payslip in self:
            amount = 0
            int_amount = 0
            if payslip.installment_ids:
                for installment in payslip.installment_ids:
                    if not installment.is_skip and installment.tipo_deduccion == '1':
                        amount += installment.installment_amt
                        int_amount += installment.ins_interest
            payslip.installment_amount = amount
            payslip.installment_int = int_amount

    @api.depends('installment_ids')
    def get_descuento1_amount(self):
        for payslip in self:
            amount = 0
            int_amount = 0
            if payslip.installment_ids:
                for installment in payslip.installment_ids:
                    if not installment.is_skip and installment.tipo_deduccion == '2':
                        amount += installment.installment_amt
                        int_amount += installment.ins_interest
            payslip.descuento1_amount = amount
            payslip.descuento1_int = int_amount

    @api.depends('installment_ids')
    def get_descuento2_amount(self):
        for payslip in self:
            amount = 0
            int_amount = 0
            if payslip.installment_ids:
                for installment in payslip.installment_ids:
                    if not installment.is_skip and installment.tipo_deduccion == '3':
                        amount += installment.installment_amt
                        int_amount += installment.ins_interest
            payslip.descuento2_amount = amount
            payslip.descuento2_int = int_amount

    @api.depends('installment_ids')
    def get_descuento3_amount(self):
        for payslip in self:
            amount = 0
            int_amount = 0
            if payslip.installment_ids:
                for installment in payslip.installment_ids:
                    if not installment.is_skip and installment.tipo_deduccion == '4':
                        amount += installment.installment_amt
                        int_amount += installment.ins_interest
            payslip.descuento3_amount = amount
            payslip.descuento3_int = int_amount

    @api.depends('installment_ids')
    def get_descuento4_amount(self):
        for payslip in self:
            amount = 0
            int_amount = 0
            if payslip.installment_ids:
                for installment in payslip.installment_ids:
                    if not installment.is_skip and installment.tipo_deduccion == '5':
                        amount += installment.installment_amt
                        int_amount += installment.ins_interest
            payslip.descuento4_amount = amount
            payslip.descuento4_int = int_amount

    @api.depends('installment_ids')
    def get_descuento5_amount(self):
        for payslip in self:
            amount = 0
            int_amount = 0
            if payslip.installment_ids:
                for installment in payslip.installment_ids:
                    if not installment.is_skip and installment.tipo_deduccion == '6':
                        amount += installment.installment_amt
                        int_amount += installment.ins_interest
            payslip.descuento5_amount = amount
            payslip.descuento5_int = int_amount

    @api.depends('installment_ids')
    def get_descuento6_amount(self):
        for payslip in self:
            amount = 0
            int_amount = 0
            if payslip.installment_ids:
                for installment in payslip.installment_ids:
                    if not installment.is_skip and installment.tipo_deduccion == '7':
                        amount += installment.installment_amt
                        int_amount += installment.ins_interest
            payslip.descuento6_amount = amount
            payslip.descuento6_int = int_amount

    @api.depends('installment_ids')
    def get_descuento7_amount(self):
        for payslip in self:
            amount = 0
            int_amount = 0
            if payslip.installment_ids:
                for installment in payslip.installment_ids:
                    if not installment.is_skip and installment.tipo_deduccion == '8':
                        amount += installment.installment_amt
                        int_amount += installment.ins_interest
            payslip.descuento7_amount = amount
            payslip.descuento7_int = int_amount

    @api.depends('installment_ids')
    def get_descuento8_amount(self):
        for payslip in self:
            amount = 0
            int_amount = 0
            if payslip.installment_ids:
                for installment in payslip.installment_ids:
                    if not installment.is_skip and installment.tipo_deduccion == '9':
                        amount += installment.installment_amt
                        int_amount += installment.ins_interest
            payslip.descuento8_amount = amount
            payslip.descuento8_int = int_amount

    @api.depends('installment_ids')
    def get_descuento9_amount(self):
        for payslip in self:
            amount = 0
            int_amount = 0
            if payslip.installment_ids:
                for installment in payslip.installment_ids:
                    if not installment.is_skip and installment.tipo_deduccion == '10':
                        amount += installment.installment_amt
                        int_amount += installment.ins_interest
            payslip.descuento9_amount = amount
            payslip.descuento9_int = int_amount

    @api.depends('installment_ids')
    def get_descuento10_amount(self):
        for payslip in self:
            amount = 0
            int_amount = 0
            if payslip.installment_ids:
                for installment in payslip.installment_ids:
                    if not installment.is_skip and installment.tipo_deduccion == '11':
                        amount += installment.installment_amt
                        int_amount += installment.ins_interest
            payslip.descuento10_amount = amount
            payslip.descuento10_int = int_amount

    @api.depends('installment_ids')
    def get_descuento11_amount(self):
        for payslip in self:
            amount = 0
            int_amount = 0
            if payslip.installment_ids:
                for installment in payslip.installment_ids:
                    if not installment.is_skip and installment.tipo_deduccion == '12':
                        amount += installment.installment_amt
                        int_amount += installment.ins_interest
            payslip.descuento11_amount = amount
            payslip.descuento11_int = int_amount

    @api.depends('installment_ids')
    def get_descuento12_amount(self):
        for payslip in self:
            amount = 0
            int_amount = 0
            if payslip.installment_ids:
                for installment in payslip.installment_ids:
                    if not installment.is_skip and installment.tipo_deduccion == '13':
                        amount += installment.installment_amt
                        int_amount += installment.ins_interest
            payslip.descuento12_amount = amount
            payslip.descuento12_int = int_amount

    @api.depends('installment_ids')
    def get_descuento13_amount(self):
        for payslip in self:
            amount = 0
            int_amount = 0
            if payslip.installment_ids:
                for installment in payslip.installment_ids:
                    if not installment.is_skip and installment.tipo_deduccion == '14':
                        amount += installment.installment_amt
                        int_amount += installment.ins_interest
            payslip.descuento13_amount = amount
            payslip.descuento13_int = int_amount

    @api.depends('installment_ids')
    def get_descuento14_amount(self):
        for payslip in self:
            amount = 0
            int_amount = 0
            if payslip.installment_ids:
                for installment in payslip.installment_ids:
                    if not installment.is_skip and installment.tipo_deduccion == '15':
                        amount += installment.installment_amt
                        int_amount += installment.ins_interest
            payslip.descuento14_amount = amount
            payslip.descuento14_int = int_amount

    @api.depends('installment_ids')
    def get_descuento15_amount(self):
        for payslip in self:
            amount = 0
            int_amount = 0
            if payslip.installment_ids:
                for installment in payslip.installment_ids:
                    if not installment.is_skip and installment.tipo_deduccion == '16':
                        amount += installment.installment_amt
                        int_amount += installment.ins_interest
            payslip.descuento15_amount = amount
            payslip.descuento15_int = int_amount

    @api.onchange('employee_id')
    def onchange_employee(self):
        if self.employee_id:
            installment_ids = self.env['installment.line'].search(
                [('employee_id', '=', self.employee_id.id), ('loan_id.state', '=', 'done'),
                 ('is_paid', '=', False),('date','<=',self.date_to)])
            if installment_ids:
                self.installment_ids = [(6, 0, installment_ids.ids)]

    @api.onchange('installment_ids')
    def onchange_installment_ids(self):
        if self.employee_id:
            installment_ids = self.env['installment.line'].search(
                [('employee_id', '=', self.employee_id.id), ('loan_id.state', '=', 'done'),
                 ('is_paid', '=', False), ('date', '<=', self.date_to)])
            if installment_ids:
                self.installment_ids = [(6, 0, installment_ids.ids)]

    
    def action_payslip_done(self):
        res = super(hr_payslip, self).action_payslip_done()
        if self.installment_ids:
            for installment in self.installment_ids:
                #if not installment.is_skip:
                installment.is_paid = True
                installment.payslip_id = self.id

#    @api.depends('installment_ids')
    def get_dias_laborados(self):
        for payslip in self:
            dias = payslip.imss_dias
            work_lines = payslip.env['hr.payslip.worked_days'].search([('payslip_id','=',payslip.id)])
            for line in work_lines:
                if line.code == 'FI' or line.code == 'FJS' or line.code == 'FR' or line.code == 'INC_RT' or line.code == 'INC_EG' or line.code == 'INC_MAT':
                    dias -= 1
            payslip.rp_dias_laborados =  dias

    def get_dias_completos(self):
        for payslip in self:
            dias = payslip.imss_dias
            work_lines = payslip.env['hr.payslip.worked_days'].search([('payslip_id','=',payslip.id)])
            for line in work_lines:
                if line.code == 'INC_RT' or line.code == 'INC_EG' or line.code == 'INC_MAT':
                    dias -= 1
            payslip.rp_dias_completos =  dias

    def get_dias_periodo(self):
        for payslip in self:
            dias = 0
            lines = payslip.contract_id.env['tablas.periodo.bimestral'].search([('form_id','=',payslip.contract_id.tablas_cfdi_id.id),('dia_fin','>=',payslip.date_to),('dia_inicio','<=',payslip.date_to)],limit=1)
            if lines:
                dias = lines.no_dias/4
            payslip.rp_dias_periodo =  dias

    def get_gravado(self):
        for payslip in self:
            gravado = 0
            lines = payslip.env['hr.payslip.line'].search([('code','=','TPERG'),('slip_id','=',payslip.id)],limit=1)
            if lines:
                gravado = lines.amount
            payslip.rp_gravado =  gravado

    @api.depends('rp_gravado')
    def get_tablas_values(self):
        grabado_mensual = 0
        for payslip in self:
            if payslip.ultima_nomina:
                grabado_mensual = payslip.rp_gravado + payslip.acum_per_grav
            else:
                grabado_mensual = payslip.rp_gravado  / payslip.dias_pagar * payslip.contract_id.tablas_cfdi_id.imss_mes

            lines = payslip.contract_id.env['tablas.general.line'].search([('form_id','=',payslip.contract_id.tablas_cfdi_id.id),('lim_inf','<=',grabado_mensual)],order='lim_inf desc',limit=1)
            if lines:
                payslip.rp_limite_inferior =  lines.lim_inf
                payslip.rp_cuota_fija =  lines.c_fija
                payslip.rp_porcentaje =  lines.s_excedente
            lines2 = payslip.contract_id.env['tablas.subsidio.line'].search([('form_id','=',payslip.contract_id.tablas_cfdi_id.id),('lim_inf','<=',grabado_mensual)],order='lim_inf desc',limit=1)
            if lines2:
               payslip.rp_subsidio =  lines2.s_mensual


    @api.onchange('date_to')
    def _get_retardo(self):
        if self.date_to and self.date_from:
            line = self.env['retardo.nomina'].search([('employee_id','=',self.employee_id.id),('fecha','>=',self.date_from),
                                                                    ('fecha','<=',self.date_to),('state','=','done')])
            if line:
                self.retardo = True
            else:
                self.retardo = False

    def monto_a_texto(self, monto):
        currency_type = 'M.N'
        # Split integer and decimal part
        amount_i, amount_d = divmod(monto, 1)
        amount_d = round(amount_d, 2)
        amount_d = int(round(amount_d * 100, 2))
        currency = self.env['res.currency'].search([('name','=', 'MXN')], limit=1)
        words = currency.with_context(lang='es_MX').amount_to_text(amount_i).upper()
        invoice_words = '%(words)s %(amount_d)02d/100 %(curr_t)s' % dict(
            words=words, amount_d=amount_d, curr_t=currency_type)
        return invoice_words

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'
    
    
    @api.depends('slip_ids.state','slip_ids.estado_factura')
    def _compute_show_cancelar_button(self):
        for payslip_batch in self:
            show_button = True
            for payslip in payslip_batch.slip_ids:
                if payslip.state != 'done'  or payslip.estado_factura!='factura_correcta':
                    show_button=False
                    break
            payslip_batch.show_cancelar_button = show_button
        
    show_cancelar_button = fields.Boolean('Show Cancelar CFDI/Payslip Button', compute='_compute_show_cancelar_button')
    
    
    def action_cancelar_cfdi(self):
        if hasattr(self.slip_ids, 'action_cfdi_cancel'):
            self.slip_ids.action_cfdi_cancel()
        return True
    
    
    def action_cancelar_nomina(self):
        self.slip_ids.action_payslip_cancel()
        return True
    
    
    
   
    def get_department(self):
        result = {}
        department = self.env['hr.department'].search([])
        for dept in department:
            result[dept.id] = dept.name
        return result

  
    def get_payslip_group_by_department(self):
        result = {}
        for line in self.slip_ids:
            if line.employee_id.department_id.id in result.keys():
                result[line.employee_id.department_id.id].append(line)
            else:
                result[line.employee_id.department_id.id] = [line]
        return result
    
class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def action_payslip_cancel(self):
        for payslip in self:
            module = self.env['ir.module.module'].sudo().search([('name','=','om_hr_payroll_account')])
            if module and module.state == 'installed':
               moves = payslip.mapped('move_id')
               moves.filtered(lambda x: x.state == 'posted').button_cancel()
               payslip.write({'move_id': None})
            payslip.write({'acum_fondo_ahorro': 0})
            #quitar los prestamos
            if payslip.installment_ids:
                for installment in payslip.installment_ids:
                   installment.is_paid = False
                   installment.payslip_id = None
            payslip.write({'state': 'cancel'})
        return
