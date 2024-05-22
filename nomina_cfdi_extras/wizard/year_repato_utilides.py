# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import timedelta, date
import io
from odoo.tools.misc import xlwt
import base64
from odoo.exceptions import UserError, Warning
import logging
_logger = logging.getLogger(__name__)

class XLSUploadWizard(models.TransientModel):
    _name = 'repart.outilidades.wizard'
    _description = 'Reparto utilidades'

    ano = fields.Selection([('2022','2022'),('2023','2023'),('2024','2024')],string="Año")
    total_repartir = fields.Float("Monto a repartir")
    file_data = fields.Binary("File Data")
    date_slip = fields.Date(string='Fecha')

    def reparto_utilidades_data(self):
        monto_total = 0
        dias_laborados = 0

        if not self.ano:
            raise UserError(_('Falta colocar un año'))

        if not self.total_repartir:
            raise UserError(_('Falta colocar una monto para repartir'))

        domain=[('state','=', 'done')]
        domain.append(('date_from','>=',date(int(self.ano), 1, 1)))
        domain.append(('date_from','<=',date(int(self.ano), 12, 31)))
        domain.append(('employee_id.regimen','=','02'))
        payslips = self.env['hr.payslip'].search(domain)
        domain.append(('tipo_nomina','=','O'))
        payslips2 = self.env['hr.payslip'].search(domain)

        payslip_lines = payslips.mapped('line_ids').filtered(lambda x: x.code == 'NET')
        work_lines = payslips2.mapped('worked_days_line_ids').filtered(lambda x: x.code in ['WORK100', 'VAC', 'FJC', 'SEPT'])

        for slip in payslip_lines:
           monto_total += slip.total
        if monto_total == 0:
           raise UserError(_('No hay monto pagado en las nóminas del periodo seleccionado'))

        for work in work_lines:
           dias_laborados += work.number_of_days
        if dias_laborados == 0:
           raise UserError(_('No hay dias laborados en las nóminas del periodo seleccionado.'))

        workbook = xlwt.Workbook()
        bold = xlwt.easyxf("font: bold on;")

        worksheet = workbook.add_sheet('Reparto de utilidades')

        from_to_date = 'De  %s'%(self.ano)

        worksheet.write_merge(1, 1, 0, 4, 'Reparto de utilidades', bold)
        worksheet.write_merge(2, 2, 0, 4, from_to_date, bold)
        #worksheet.write_merge(3, 3, 0, 4, concepto, bold)
        
        worksheet.write(4, 0, 'Monto a repartir', bold)
        worksheet.write(4, 1, self.total_repartir)
        worksheet.write(5, 0, 'Monto total', bold)
        worksheet.write(5, 1, monto_total)
        worksheet.write(6, 0, 'Dias totales', bold)
        worksheet.write(6, 1, dias_laborados)

        coef_dias = (self.total_repartir / 2) / dias_laborados
        coef_monto = (self.total_repartir / 2) / monto_total

        worksheet.write(7, 0, 'Coeficiente monto', bold)
        worksheet.write(7, 1, coef_monto)
        worksheet.write(8, 0, 'Coeficiente dias', bold)
        worksheet.write(8, 1, coef_dias)

        worksheet.write(10, 0, 'Empleado', bold)
        worksheet.write(10, 1, 'Salario acumulado', bold)
        worksheet.write(10, 2, 'Dias acumulados', bold)
        worksheet.write(10, 3, 'PTU Salario', bold)
        worksheet.write(10, 4, 'PTU dias', bold)
        worksheet.write(10, 5, 'PTU total', bold)
        row = 11

        amount = {}
        for line in payslip_lines:
            if line.slip_id.employee_id not in amount:
                amount[line.slip_id.employee_id] = line.total
            else:
                amount[line.slip_id.employee_id] += line.total

        days = {}
        for line in work_lines:
            if line.payslip_id.employee_id not in days:
                days[line.payslip_id.employee_id] = line.number_of_days
            else:
                days[line.payslip_id.employee_id] += line.number_of_days

        _logger.info('days %s', days)
        tot_empl_amount = 0
        tot_empl_days = 0
        for employee in amount.items():
           # _logger.info('empleado %s', employee)
             worksheet.write(row, 0, employee[0].name)
             tot_empl_amount = employee[1]
             worksheet.write(row, 1, tot_empl_amount)
             try:
                 id_days = list(days).index(employee[0])
             except Exception as e:
                 _logger.info('Empleado %s no tiene dias laborados', employee[0].name)
                 row += 1
                 continue
             tot_empl_days = list(days.values())[id_days]
             worksheet.write(row, 2, tot_empl_days)
             worksheet.write(row, 3, tot_empl_amount * coef_monto)
             worksheet.write(row, 4, tot_empl_days * coef_dias)
             total01 = tot_empl_amount * coef_monto + tot_empl_days * coef_dias
             # revisar monto exento  límite máximo tres meses del salario del trabajador o el promedio de la participación recibida en los últimos tres años.
             contract_id = employee[0].contract_id
             if not contract_id:
                 contract_id = self.env['hr.contract'].search([('employee_id','=',employee[0].id)], limit=1)
             max_limit = contract_id.sueldo_diario * 90
             if total01 > max_limit:
                 total01 = max_limit
             worksheet.write(row, 5, total01)
             row += 1

        fp = io.BytesIO()
        workbook.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()

        self.write({'file_data':base64.b64encode(data)})
        action = {
            'name': 'Payslips',
            'type': 'ir.actions.act_url',
            'url': "/web/content/?model="+self._name+"&id=" + str(self.id) + "&field=file_data&download=true&filename=Reparto_utilidades.xls",
            'target': 'self',
            }
        return action

    def reparto_utilidades_payslip(self):
        monto_total = 0
        dias_laborados = 0

        if not self.ano:
            raise UserError(_('Falta colocar un año'))

        if not self.date_slip:
            raise UserError(_('Falta colocar una fecha para la nómina'))

        if not self.total_repartir:
            raise UserError(_('Falta colocar una monto para repartir'))

        domain=[('state','=', 'done')]
        domain.append(('date_from','>=',date(int(self.ano), 1, 1)))
        domain.append(('date_from','<=',date(int(self.ano), 12, 31)))
        domain.append(('employee_id.regimen','=','02'))
        payslips = self.env['hr.payslip'].search(domain)
        domain.append(('tipo_nomina','=','O'))
        payslips2 = self.env['hr.payslip'].search(domain)

        payslip_lines = payslips.mapped('line_ids').filtered(lambda x: x.code == 'NET')
        work_lines = payslips2.mapped('worked_days_line_ids').filtered(lambda x: x.code in ['WORK100', 'VAC', 'FJC', 'SEPT'])

        for slip in payslip_lines:
           monto_total += slip.total
        if monto_total == 0:
           raise UserError(_('No hay monto pagado en las nóminas del periodo seleccionado'))

        for work in work_lines:
           dias_laborados += work.number_of_days
        if dias_laborados == 0:
           raise UserError(_('No hay dias laborados en las nóminas del periodo seleccionado.'))

        coef_dias = (self.total_repartir / 2) / dias_laborados
        coef_monto = (self.total_repartir / 2) / monto_total

        amount = {}
        for line in payslip_lines:
            if line.slip_id.employee_id not in amount:
                amount[line.slip_id.employee_id] = line.total
            else:
                amount[line.slip_id.employee_id] += line.total

        days = {}
        for line in work_lines:
            if line.payslip_id.employee_id not in days:
                days[line.payslip_id.employee_id] = line.number_of_days
            else:
                days[line.payslip_id.employee_id] += line.number_of_days

        tot_empl_amount = 0
        tot_empl_days = 0

        payslip_batch_nm = 'Reparto Utilidades ' + self.ano
        batch = self.env['hr.payslip.run'].create({
               'name' : payslip_batch_nm,
               'date_start': self.date_slip,
               'date_end': self.date_slip,
               'periodicidad_pago': '99',
               'tipo_nomina': 'E',
               'fecha_pago' : self.date_slip,
        })

        for employee in amount.items():
            tot_empl_amount = employee[1]
            try:
                id_days = list(days).index(employee[0])
            except Exception as e:
                _logger.info('Empleado %s no tiene dias laborados', employee[0].name)
                continue

            tot_empl_days = list(days.values())[id_days]
            total01 = tot_empl_amount * coef_monto + tot_empl_days * coef_dias
            # revisar monto exento  límite máximo tres meses del salario del trabajador o el promedio de la participación recibida en los últimos tres años.
            contract_id = employee[0].contract_id
            if not contract_id:
                contract_id = self.env['hr.contract'].search([('employee_id','=',employee[0].id)], limit=1)
            max_limit = contract_id.sueldo_diario * 90
            if total01 > max_limit:
                 total01 = max_limit

            #nomina
            payslip_obj = self.env['hr.payslip']
            payslip_onchange_vals = payslip_obj.onchange_employee_id(self.date_slip, self.date_slip, employee_id=employee[0].id)
            payslip_vals2 = {**payslip_onchange_vals.get('value',{})}
            structure = self.env['hr.payroll.structure'].search([('code','=','PTU')], limit=1)
            if structure: 
                payslip_vals2['struct_id'] = structure.id

            other_inputs = []
            other_inputs.append((0,0,{'name' :'Reparto utilidades', 'code' : 'PTU', 'contract_id':contract_id.id, 'amount': total01}))
            worked_days2 = []
            worked_days2.append((0,0,{'name' :'Dias a pagar', 'code' : 'WORK100', 'contract_id':contract_id.id, 'number_of_days': 0}))

            payslip_vals2.update({
               'employee_id' : employee[0].id,
               'tipo_nomina' : 'E',
               'input_line_ids' : other_inputs,
               'payslip_run_id' : batch.id,
               'date_from': self.date_slip,
               'date_to': self.date_slip,
               'contract_id' : contract_id.id,
               'dias_pagar': 1,
               'fecha_pago' : self.date_slip,
               'worked_days_line_ids': worked_days2,
            })
            #if module and module.state == 'installed':
            #    payslip_vals2.update({'journal_id': self.journal_id.id})
            payslip_obj.create(payslip_vals2)
