# -*- coding: utf-8 -*-

from odoo import models, fields, _, api
from datetime import datetime
import pytz
from odoo.exceptions import UserError
from odoo import tools

class DiasFeriados(models.Model):
    _name = 'dias.feriados'
    _description = 'DiasFeriados'

    name = fields.Char("Name", required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Empleado')
    fecha = fields.Date('Fecha')
    state = fields.Selection([('draft', 'Borrador'), ('done', 'Hecho'), ('cancel', 'Cancelado')], string='Estado', default='draft')
    tipo = fields.Selection([('doble', 'Doble'), ('triple', 'Triple')], string='Tipo', default='doble')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)

    @api.model
    def init(self):
        company_id = self.env['res.company'].search([])
        for company in company_id:
            dias_feriados_sequence = self.env['ir.sequence'].search([('code', '=', 'dias.feriados'), ('company_id', '=', company.id)])
            if not dias_feriados_sequence:
                dias_feriados_sequence.create({
                        'name': 'Dias feriados',
                        'code': 'dias.feriados',
                        'padding': 4,
                        'company_id': company.id,
                    })

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_company(vals['company_id']).next_by_code('dias.feriados') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('dias.feriados') or _('New')
        result = super(DiasFeriados, self).create(vals)
        return result

   
    def action_validar(self):
        if self.fecha:
            fecha = self.fecha
            date_from = fecha.strftime("%Y-%m-%d") #+ ' 00:00:00'
            date_to = fecha.strftime("%Y-%m-%d") #+' 23:59:59'
        else:
            date_from = datetime.today().strftime("%Y-%m-%d")
            date_to = date_from + ' 20:00:00'
            date_from += ' 06:00:00'

 #       timezone = self._context.get('tz')
 #       if not timezone:
 #           timezone = self.env.user.partner_id.tz or 'UTC'
       # timezone = tools.ustr(timezone).encode('utf-8')

 #       local = pytz.timezone(timezone) #get_localzone()
 #       naive_from = datetime.strptime (date_from, "%Y-%m-%d %H:%M:%S")
 #       local_dt_from = local.localize(naive_from, is_dst=None)
 #       utc_dt_from = local_dt_from.astimezone (pytz.utc)
 #       date_from = utc_dt_from.strftime ("%Y-%m-%d %H:%M:%S")
 
 #       naive_to = datetime.strptime (date_to, "%Y-%m-%d %H:%M:%S")
 #       local_dt_to = local.localize(naive_to, is_dst=None)
 #       utc_dt_to = local_dt_to.astimezone (pytz.utc)
 #       date_to = utc_dt_to.strftime ("%Y-%m-%d %H:%M:%S")

        leave_type = None
        if self.tipo=='doble':
           if self.company_id.leave_type_dfes: 
              leave_type = self.company_id.leave_type_dfes
           else:
              raise UserError(_('Falta configurar el tipo de falta'))
        elif self.tipo=='triple':
           if self.company_id.leave_type_dfes3: 
              leave_type = self.company_id.leave_type_dfes3
           else:
              raise UserError(_('Falta configurar el tipo de falta'))
        if not leave_type:
           leave_type = self.env['hr.leave.type'].create({'name': 'DFES'})

        nombre = 'Feriado_'+self.name
        registro_falta = self.env['hr.leave'].search([('name','=', nombre)], limit=1)
        if registro_falta:
           registro_falta.write({'date_from' : date_from,
                   'date_to' : date_to,
                   'employee_id' : self.employee_id.id,
                   'holiday_status_id' : leave_type and leave_type.id,
                   'state': 'validate',
                   })
        else:
           holidays_obj = self.env['hr.leave']
           #fields_list = holidays_obj._fields.keys()

           #vals = holidays_obj.default_get(fields_list)
           vals= {#'date_from' : date_from,
               'holiday_status_id' : leave_type and leave_type.id,
               'employee_id' : self.employee_id.id,
               'name' : 'Feriado_'+self.name,
               #'date_to' : date_to,
               'request_date_from' : date_from,
               'request_date_to' : date_to,
               'state': 'confirm',
               }

           holiday = holidays_obj.new(vals)
           holiday._compute_from_employee_id()
           holiday._compute_number_of_days()
           vals.update(holiday._convert_to_write({name: holiday[name] for name in holiday._cache}))
           vals.update({'holiday_status_id' : leave_type and leave_type.id,})
           feriado = self.env['hr.leave'].create(vals)
           feriado.action_validate()
        self.write({'state':'done'})
        return

    def action_cancelar(self):
        for record in self:
           if record.state == 'draft':
               record.write({'state':'cancel'})
           else:
               record.write({'state':'cancel'})
               nombre = 'Feriado_' + record.name
               registro_falta = record.env['hr.leave'].search([('name','=', nombre)], limit=1)
               if registro_falta:
                  registro_falta.action_refuse()

    def action_draft(self):
        self.write({'state':'draft'})

    def unlink(self):
        raise UserError("Los registros no se pueden borrar, solo cancelar.")

    def action_change_state(self):
        for diaf in self:
            if diaf.state == 'draft':
                diaf.action_validar()
