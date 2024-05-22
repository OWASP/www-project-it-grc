# -*- coding: utf-8 -*-
from odoo import models, fields, _, api
import pytz
from odoo.exceptions import UserError
from datetime import datetime
from odoo import tools

class FaltasNomina(models.Model):
    _name = 'faltas.nomina'
    _description = 'FaltasNomina'

    name = fields.Char("Name", required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Empleado')
    fecha_inicio = fields.Date('Fecha inicio')
    fecha_fin = fields.Date('Fecha fin')
    tipo_de_falta = fields.Selection([('Justificada con goce de sueldo','Justificada con goce de sueldo'),
                                      ('Justificada sin goce de sueldo','Justificada sin goce de sueldo'),
                                      ('Injustificada', 'Injustificada'), 
                                      ('retardo', 'Por retardos')], string='Tipo de falta')
    state = fields.Selection([('draft', 'Borrador'), ('done', 'Hecho'), ('cancel', 'Cancelado')], string='Estado', default='draft')
    dias = fields.Integer("Dias")
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)

    @api.model
    def init(self):
        company_id = self.env['res.company'].search([])
        for company in company_id:
            faltas_sequence = self.env['ir.sequence'].search([('code', '=', 'faltas.nomina'), ('company_id', '=', company.id)])
            if not faltas_sequence:
                faltas_sequence.create({
                        'name': 'Faltas nomina',
                        'code': 'faltas.nomina',
                        'padding': 4,
                        'company_id': company.id,
                    })

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_company(vals['company_id']).next_by_code('faltas.nomina') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('faltas.nomina') or _('New')
        result = super(FaltasNomina, self).create(vals)
        return result

   
    @api.onchange('fecha_inicio', 'fecha_fin')
    def _get_dias(self):
        if self.fecha_inicio and self.fecha_fin:
            values = {
                'dias': (self.fecha_fin - self.fecha_inicio).days + 1
                }
            self.update(values)
    
   
    def action_validar(self):
        leave_type = None
        if self.tipo_de_falta=='Justificada con goce de sueldo':
            if self.company_id.leave_type_fjc: 
               leave_type = self.company_id.leave_type_fjc
            else:
               raise UserError(_('Falta configurar el tipo de falta'))
        elif self.tipo_de_falta=='Justificada sin goce de sueldo':
            if self.company_id.leave_type_fjs: 
               leave_type = self.company_id.leave_type_fjs
            else:
               raise UserError(_('Falta configurar el tipo de falta'))
        elif self.tipo_de_falta=='Injustificada':
            if self.company_id.leave_type_fi: 
               leave_type = self.company_id.leave_type_fi
            else:
               raise UserError(_('Falta configurar el tipo de falta'))
        elif self.tipo_de_falta=='retardo':
            if self.company_id.leave_type_fr: 
               leave_type = self.company_id.leave_type_fr
            else:
               raise UserError(_('Falta configurar el tipo de falta'))

        date_from = self.fecha_inicio.strftime('%Y-%m-%d') # +' 00:00:00'
        date_to = self.fecha_fin.strftime('%Y-%m-%d') # +' 23:59:59'
        
    #    timezone = self._context.get('tz')
    #    if not timezone:
    #        timezone = self.env.user.partner_id.tz or 'UTC'

#        local = pytz.timezone(timezone) #get_localzone()
#        naive_from = datetime.strptime (date_from, "%Y-%m-%d %H:%M:%S")
#        local_dt_from = local.localize(naive_from, is_dst=None)
#        utc_dt_from = local_dt_from.astimezone (pytz.utc)
#        date_from = utc_dt_from.strftime ("%Y-%m-%d %H:%M:%S")
 
#        naive_to = datetime.strptime (date_to, "%Y-%m-%d %H:%M:%S")
#        local_dt_to = local.localize(naive_to, is_dst=None)
#        utc_dt_to = local_dt_to.astimezone (pytz.utc)
#        date_to = utc_dt_to.strftime ("%Y-%m-%d %H:%M:%S")
        
        nombre = 'Faltas_' + self.name
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
           vals = {#'date_from' : date_from,
               'holiday_status_id' : leave_type and leave_type.id,
               'employee_id' : self.employee_id.id,
               'name' : 'Faltas_'+self.name,
               #'date_to' : date_to,
               'request_date_from' : date_from,
               'request_date_to' : date_to,
               'state': 'confirm',}

           holiday = holidays_obj.new(vals)
           holiday._compute_from_employee_id()
           holiday._compute_number_of_days()
           vals.update(holiday._convert_to_write({name: holiday[name] for name in holiday._cache}))
           vals.update({'holiday_status_id' : leave_type and leave_type.id,})
           falta = self.env['hr.leave'].create(vals)
           falta.action_validate()
        self.write({'state':'done'})
        return

    def action_cancelar(self):
        for record in self:
           if record.state == 'draft':
               record.write({'state':'cancel'})
           else:
              record.write({'state':'cancel'})
              nombre = 'Faltas_'+ record.name
              registro_falta = record.env['hr.leave'].search([('name','=', nombre)], limit=1)
              if registro_falta:
                 registro_falta.action_refuse()

    def action_draft(self):
        self.write({'state':'draft'})

    def unlink(self):
        raise UserError("Los registros no se pueden borrar, solo cancelar.")

    def action_change_state(self):
        for falta in self:
            if falta.state == 'draft':
                falta.action_validar()
