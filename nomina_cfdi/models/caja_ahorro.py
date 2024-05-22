# -*- coding: utf-8 -*-
from odoo import models, fields, _, api
import pytz
from odoo.exceptions import UserError
from datetime import datetime, date
from odoo import tools
import logging
_logger = logging.getLogger(__name__)

class CajaAhorro(models.Model):
    _name = 'caja.nomina'
    _description = 'Caja de ahorro nomina'

    name = fields.Char("Name", required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Empleado')
    fecha_solicitud = fields.Date('Fecha solicitud')
    fecha_aplicacion = fields.Date('Fecha aplicación')
    descripcion = fields.Char("Descripción")
    clave = fields.Char("Código")
    importe = fields.Float(string="Importe")
    saldo = fields.Float(string="Saldo", compute='_compute_saldo', store=True)
    #contract_id = fields.Many2one('hr.contract', string='Contrato')

    state = fields.Selection([('draft', 'Borrador'), ('done', 'Hecho'), ('cancel', 'Cancelado')], string='Estado', default='draft')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)

    @api.model
    def init(self):
        company_id = self.env['res.company'].search([])
        for company in company_id:
            horas_nomina_sequence = self.env['ir.sequence'].search([('code', '=', 'caja.nomina'), ('company_id', '=', company.id)])
            if not horas_nomina_sequence:
                horas_nomina_sequence.create({
                        'name': 'Caja Ahorro',
                        'code': 'caja.nomina',
                        'padding': 4,
                        'company_id': company.id,
                    })

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_company(vals['company_id']).next_by_code('caja.nomina') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('caja.nomina') or _('New')
        result = super(CajaAhorro, self).create(vals)
        return result

    @api.onchange('employee_id')
    def _compute_saldo(self):
        for record in self:
          if record.employee_id and len(record.employee_id.contract_ids) > 0:
            contract = record.employee_id.contract_ids[0]
            if contract and record.state == 'draft':
               if contract.tablas_cfdi_id:
                   abono = 0
                   retiro = 0
                   domain=[('state','=', 'done')]
                   domain.append(('employee_id','=',record.employee_id.id))
                   if contract.tablas_cfdi_id.caja_ahorro_abono:
                        rules = record.env['hr.salary.rule'].search([('code', '=', contract.tablas_cfdi_id.caja_ahorro_abono.code)])
                        payslips = record.env['hr.payslip'].search(domain)
                        payslip_lines = payslips.mapped('line_ids').filtered(lambda x: x.salary_rule_id.id in rules.ids)
                        employees = {}
                        for line in payslip_lines:
                           if line.slip_id.employee_id not in employees:
                              employees[line.slip_id.employee_id] = {line.slip_id: []}
                           if line.slip_id not in employees[line.slip_id.employee_id]:
                              employees[line.slip_id.employee_id].update({line.slip_id: []})
                           employees[line.slip_id.employee_id][line.slip_id].append(line)
                        for employee, payslips in employees.items():
                            for payslip2,lines in payslips.items():
                               for line in lines:
                                  abono += line.total
                   if contract.tablas_cfdi_id.caja_ahorro_retiro:
                        rules = record.env['hr.salary.rule'].search([('code', '=', contract.tablas_cfdi_id.caja_ahorro_retiro.code)])
                        payslips = record.env['hr.payslip'].search(domain)
                        payslip_lines = payslips.mapped('line_ids').filtered(lambda x: x.salary_rule_id.id in rules.ids)
                        employees = {}
                        for line in payslip_lines:
                           if line.slip_id.employee_id not in employees:
                              employees[line.slip_id.employee_id] = {line.slip_id: []}
                           if line.slip_id not in employees[line.slip_id.employee_id]:
                              employees[line.slip_id.employee_id].update({line.slip_id: []})
                           employees[line.slip_id.employee_id][line.slip_id].append(line)
                        for employee, payslips in employees.items():
                            for payslip2,lines in payslips.items():
                               for line in lines:
                                  retiro += line.total
                   record.saldo = abono - retiro
            else:
               return
          else:
            return

    @api.onchange('importe')
    def _compute_importe(self):
        if self.importe and self.saldo:
            if self.importe > self.saldo:
                raise UserError(_("El importe a retirar debe ser menor o igual al saldo."))
    
    def action_validar(self):
        self.write({'state':'done'})
        return

    def action_cancelar(self):
        for record in self:
            if self.state == 'draft':
               self.write({'state':'cancel'})
            elif self.state == 'done':
               if date.today() > self.fecha_aplicacion:
                   raise UserError("Solo se puede cancelar si no ha pasado su fecha de aplicación.")
               else:
                   self.write({'state':'cancel'})

    def unlink(self):
        for record in self:
           if record.state != 'cancel':
              raise UserError("Solo se pueden eliminar registros cancelados.")
           return super(CajaAhorro, record).unlink()

    def action_change_state(self):
        for record in self:
            if record.state == 'draft':
                record.action_validar()
