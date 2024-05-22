# -*- coding: utf-8 -*-
from odoo import models, fields, _, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz
from odoo.exceptions import UserError
from odoo import tools

class IncapacidadesNomina(models.Model):
    _name = 'incapacidades.nomina'
    _description = 'IncapacidadesNomina'

    name = fields.Char("Name", required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Empleado')
    fecha = fields.Date('Fecha')
    
    ramo_de_seguro = fields.Selection([('Riesgo de trabajo', 'Riesgo de trabajo'), ('Enfermedad general', 'Enfermedad general'), ('Maternidad','Maternidad')], string='Ramo de seguro')
    tipo_de_riesgo = fields.Selection([('Accidente de trabajo', 'Accidente de trabajo'), ('Accidente de trayecto', 'Accidente de trayecto'), ('Enfermedad de trabajo','Enfermedad de trabajo')], string='Tipo de riesgo')
    secuela = fields.Selection([('Ninguna', 'Ninguna'), ('Incapacidad temporal', 'Incapacidad temporal'), ('Valuación inicial provisional','Valuación inicial provisional'), ('Valuación inicial definitiva', 'Valuación inicial definitiva')], string='Secuela')
    control = fields.Selection([('Unica', 'Unica'), ('Inicial', 'Inicial'), ('Subsecuente','Subsecuente'), ('Alta médica o ST-2', 'Alta médica o ST-2')], string='Control')
    control2 = fields.Selection([('01', 'Prenatal o ST-3'), ('02', 'Enalce'), ('03','Postnatal')], string='Control maternidad')
    dias = fields.Integer("Dias")
    porcentaje = fields.Char('Porcentaje')
    descripcion = fields.Text('Descripción')
    state = fields.Selection([('draft', 'Borrador'), ('done', 'Hecho'), ('cancel', 'Cancelado')], string='Estado', default='draft')
    folio_incapacidad = fields.Char('Folio de incapacidad')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)

    @api.model
    def init(self):
        company_id = self.env['res.company'].search([])
        for company in company_id:
            incapacidades_nomina_sequence = self.env['ir.sequence'].search([('code', '=', 'incapacidades.nomina'), ('company_id', '=', company.id)])
            if not incapacidades_nomina_sequence:
                incapacidades_nomina_sequence.create({
                        'name': 'Incapacidades nomina',
                        'code': 'incapacidades.nomina',
                        'padding': 4,
                        'company_id': company.id,
                    })

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_company(vals['company_id']).next_by_code('incapacidades.nomina') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('incapacidades.nomina') or _('New')
        result = super(IncapacidadesNomina, self).create(vals)
        return result

#   
#   onchange('folio_incapacidad')
#    def _check_folio_length(self):
#        if self.folio_incapacidad:
#            if len(self.folio_incapacidad) != 7:
#                raise UserError(_('La longitud del folio es incorrecto'))

   
    def action_validar(self):
        leave_type = None
        if self.ramo_de_seguro=='Riesgo de trabajo':
            if self.company_id.leave_type_rie_id: 
               leave_type = self.company_id.leave_type_rie_id
            else:
               raise UserError(_('Falta configurar el tipo de falta'))
        elif self.ramo_de_seguro=='Enfermedad general':
            if self.company_id.leave_type_enf_id: 
               leave_type = self.company_id.leave_type_enf_id
            else:
               raise UserError(_('Falta configurar el tipo de falta'))
        elif self.ramo_de_seguro=='Maternidad':
            if self.company_id.leave_type_mat_id: 
               leave_type = self.company_id.leave_type_mat_id
            else:
               raise UserError(_('Falta configurar el tipo de falta'))

        if self.fecha:
            date_from = self.fecha
            date_to = date_from + relativedelta(days=self.dias - 1)
            date_from = date_from.strftime("%Y-%m-%d") #+ ' 00:00:00'
            date_to = date_to.strftime("%Y-%m-%d") #+' 23:59:59'
        else:
            date_from = datetime.today().strftime("%Y-%m-%d")
            date_to = date_from + ' 20:00:00'
            date_from += ' 06:00:00'

#        timezone = self._context.get('tz')
#        if not timezone:
#            timezone = self.env.user.partner_id.tz or 'UTC'
        #timezone = tools.ustr(timezone).encode('utf-8')

#        local = pytz.timezone(timezone) #get_localzone()
#        naive_from = datetime.strptime (date_from, "%Y-%m-%d %H:%M:%S")
#        local_dt_from = local.localize(naive_from, is_dst=None)
#        utc_dt_from = local_dt_from.astimezone (pytz.utc)
#        date_from = utc_dt_from.strftime ("%Y-%m-%d %H:%M:%S")
 
#        naive_to = datetime.strptime (date_to, "%Y-%m-%d %H:%M:%S")
#        local_dt_to = local.localize(naive_to, is_dst=None)
#        utc_dt_to = local_dt_to.astimezone (pytz.utc)
#        date_to = utc_dt_to.strftime ("%Y-%m-%d %H:%M:%S")

        nombre = 'Incapacidades_'+self.name
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
               'name' : 'Incapacidades_'+self.name,
               #'date_to' : date_to,
               'request_date_from' : date_from,
               'request_date_to' : date_to,
               'state': 'confirm',}

           holiday = holidays_obj.new(vals)
           holiday._compute_from_employee_id()
           holiday._compute_number_of_days()
           vals.update(holiday._convert_to_write({name: holiday[name] for name in holiday._cache}))
           vals.update({'holiday_status_id' : leave_type and leave_type.id,})
           #holidays_obj.create(vals)
           incapacidad = self.env['hr.leave'].create(vals)
           incapacidad.action_validate()
        self.write({'state':'done'})
        return

   
    def action_cancelar(self):
        for record in self:
           if record.state == 'draft':
               record.write({'state':'cancel'})
           else:
               record.write({'state':'cancel'})
               nombre = 'Incapacidades_' + record.name
               registro_falta = record.env['hr.leave'].search([('name','=', nombre)], limit=1)
               if registro_falta:
                  registro_falta.action_refuse()

    def action_draft(self):
        self.write({'state':'draft'})

    def unlink(self):
        raise UserError("Los registros no se pueden borrar, solo cancelar.")

    def action_change_state(self):
        for record in self:
            if record.state == 'draft':
                record.action_validar()
