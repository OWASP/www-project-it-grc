# -*- coding: utf-8 -*-
from odoo import models, fields, _, api
from datetime import date, datetime, timedelta
from odoo.exceptions import UserError

class IncidenciasNomina(models.Model):
    _name = 'incidencias.nomina'
    _description = 'IncidenciasNomina'

    name = fields.Char("Name", required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    tipo_de_incidencia = fields.Selection([('Cambio salario', 'Cambio salario'), 
                                            ('Alta', 'Alta'),
                                            ('Reingreso', 'Reingreso'),
                                            ('Baja','Baja'),
                                            ('Cambio reg. patronal','Cambio reg. patronal')],
                                            string='Tipo de incidencia')
    employee_id = fields.Many2one('hr.employee', string='Empleado')
    fecha = fields.Date('Fecha')
    registro_patronal = fields.Many2one('registro.patronal', string='Registro patronal')
    sueldo_mensual = fields.Float('Sueldo mensual')
    sueldo_diario = fields.Float('Sueldo diario')
    sueldo_diario_integrado = fields.Float('Sueldo diario integrado')
    sueldo_por_horas = fields.Float("Sueldo por horas")
    sueldo_cotizacion_base = fields.Float('Sueldo cotización base')
    state = fields.Selection([('draft', 'Borrador'), ('done', 'Hecho'), ('cancel', 'Cancelado')], string='Estado', default='draft')
    tipo_de_baja = fields.Selection([('1','Término de contrato'),
                                      ('2','Separación voluntaria'),
                                      ('3','Abandono de empleo'),
                                      ('4','Defunción'),
                                      ('5','Clausura'),
                                      ('6','Otras'),
                                      ('7','Ausentismo'),
                                      ('8','Rescisión de contrato'),
                                      ('9','Jubilación'),
                                      ('A', 'Pensión')], string='Tipo de baja')
    contract_id = fields.Many2one('hr.contract', string='Contrato')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)
    registro_patronal_ant = fields.Many2one('registro.patronal', string='Registro patronal anterior')
    sueldo_mensual_ant = fields.Float('Sueldo mensual ant')
    sueldo_diario_ant = fields.Float('Sueldo diario ant')
    sueldo_diario_integrado_ant = fields.Float('Sueldo diario integrado ant')
    sueldo_por_horas_ant = fields.Float("Sueldo por horas ant")
    sueldo_cotizacion_base_ant = fields.Float('Sueldo cotización base ant')
    fecha_anterior = fields.Date('Fecha anterior')

    @api.onchange('tipo_de_incidencia')
    def _onchange_incidencia(self):
        if self.tipo_de_incidencia == 'Reingreso':
            return {'domain': {'employee_id': [('active', '=', False)]}}
        else:
            return {'domain': {'employee_id': [('active', '=', True)]}}

    
    @api.onchange('sueldo_mensual')
    def _compute_sueldo(self):
        if self.sueldo_mensual:
            values = {
            'sueldo_diario': self.sueldo_mensual/self.contract_id.tablas_cfdi_id.dias_mes,
            'sueldo_por_horas': self.sueldo_mensual/self.contract_id.tablas_cfdi_id.dias_mes/8,
            'sueldo_diario_integrado': self.calculate_sueldo_diario_integrado(),
            'sueldo_cotizacion_base': self.calculate_sueldo_cotizacion_base(),
            }
            self.update(values)

    @api.model
    def calculate_sueldo_cotizacion_base(self): 
        if self.contract_id and self.contract_id.date_start:
            if self.tipo_de_incidencia == 'Cambio salario':
               date_start = self.contract_id.date_start
            else:
               date_start = fields.Date.from_string(self.fecha)
            today = datetime.today().date()
            diff_date = (today - date_start + timedelta(days=1)).days
            years = diff_date /365.0
            #_logger.info('years ... %s', years)
            tablas_cfdi = self.contract_id.tablas_cfdi_id 
            if not tablas_cfdi: 
                tablas_cfdi = self.env['tablas.cfdi'].search([],limit=1)
            if not tablas_cfdi:
                return 
            if years < 1.0: 
                tablas_cfdi_lines = tablas_cfdi.tabla_antiguedades.filtered(lambda x: x.antiguedad >= years).sorted(key=lambda x:x.antiguedad) 
            else: 
                tablas_cfdi_lines = tablas_cfdi.tabla_antiguedades.filtered(lambda x: x.antiguedad <= years).sorted(key=lambda x:x.antiguedad, reverse=True) 
            if not tablas_cfdi_lines: 
                return 
            tablas_cfdi_line = tablas_cfdi_lines[0]
            max_sdi = tablas_cfdi.uma * 25
            sdi = ((365 + tablas_cfdi_line.aguinaldo + (tablas_cfdi_line.vacaciones)* (tablas_cfdi_line.prima_vac/100) ) / 365 ) * self.sueldo_mensual/tablas_cfdi.dias_mes
            if sdi > max_sdi:
                sueldo_cotizacion_base = max_sdi
            else:
                sueldo_cotizacion_base = sdi
        else: 
            sueldo_cotizacion_base = 0
        return sueldo_cotizacion_base

    @api.model
    def calculate_sueldo_diario_integrado(self): 
        if self.contract_id and self.contract_id.date_start: 
            if self.tipo_de_incidencia == 'Cambio salario':
               date_start = self.contract_id.date_start
            else:
               date_start = fields.Date.from_string(self.fecha)
            today = datetime.today().date()
            diff_date = (today - date_start + timedelta(days=1)).days
            years = diff_date /365.0
            #_logger.info('years ... %s', years)
            tablas_cfdi = self.contract_id.tablas_cfdi_id 
            if not tablas_cfdi: 
                tablas_cfdi = self.env['tablas.cfdi'].search([],limit=1) 
            if not tablas_cfdi:
                return 
            if years < 1.0: 
                tablas_cfdi_lines = tablas_cfdi.tabla_antiguedades.filtered(lambda x: x.antiguedad >= years).sorted(key=lambda x:x.antiguedad) 
            else: 
                tablas_cfdi_lines = tablas_cfdi.tabla_antiguedades.filtered(lambda x: x.antiguedad <= years).sorted(key=lambda x:x.antiguedad, reverse=True) 
            if not tablas_cfdi_lines: 
                return 
            tablas_cfdi_line = tablas_cfdi_lines[0]
            max_sdi = tablas_cfdi.uma * 25
            sdi = ((365 + tablas_cfdi_line.aguinaldo + (tablas_cfdi_line.vacaciones)* (tablas_cfdi_line.prima_vac/100) ) / 365 ) * self.sueldo_mensual/tablas_cfdi.dias_mes
            sueldo_diario_integrado = sdi
        else: 
            sueldo_diario_integrado = 0
        return sueldo_diario_integrado

    @api.model
    def init(self):
        company_id = self.env['res.company'].search([])
        for company in company_id:
            incidencias_nomina_sequence = self.env['ir.sequence'].search([('code', '=', 'incidencias.nomina'), ('company_id', '=', company.id)])
            if not incidencias_nomina_sequence:
                incidencias_nomina_sequence.create({
                        'name': 'Incidencias nomina',
                        'code': 'incidencias.nomina',
                        'padding': 4,
                        'company_id': company.id,
                    })

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_company(vals['company_id']).next_by_code('incidencias.nomina') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('incidencias.nomina') or _('New')
        result = super(IncidenciasNomina, self).create(vals)
        return result

    
    def action_validar(self):
        employee = self.employee_id
        if employee:
            if self.tipo_de_incidencia=='Cambio reg. patronal':
                self.registro_patronal_ant = employee.registro_patronal_id.id
                employee.write({'registro_patronal':self.registro_patronal.id})
            elif self.tipo_de_incidencia=='Cambio salario':
                if self.contract_id:
                    self.sueldo_mensual_ant = self.contract_id.wage
                    self.sueldo_diario_ant = self.contract_id.sueldo_diario
                    self.sueldo_diario_integrado_ant = self.contract_id.sueldo_diario_integrado
                    self.sueldo_por_horas_ant = self.contract_id.sueldo_hora
                    self.sueldo_cotizacion_base_ant = self.contract_id.sueldo_base_cotizacion
                    self.contract_id.write({'wage':self.sueldo_mensual,
                                                    'sueldo_diario_integrado' : self.sueldo_diario_integrado,
                                                    'sueldo_base_cotizacion' : self.sueldo_cotizacion_base,
                                                    'sueldo_diario' : self.sueldo_diario,
                                                    'sueldo_hora' : self.sueldo_por_horas
                                                    })
                    self.env['contract.historial.salario'].create({'sueldo_mensual': self.sueldo_mensual, 'sueldo_diario': self.sueldo_diario, 'fecha_sueldo': self.fecha,
                                                                   'sueldo_por_hora' : self.sueldo_por_horas, 'sueldo_diario_integrado': self.sueldo_diario_integrado,
                                                                   'sueldo_base_cotizacion': self.sueldo_cotizacion_base, 'contract_id' : self.contract_id.id
                                                                   })
            elif self.tipo_de_incidencia=='Baja':
                employee.write({'active':False})
                if self.contract_id:
                    self.contract_id.write({'state':'cancel'})
            elif self.tipo_de_incidencia=='Reingreso':
                employee.write({'active':True, 'registro_patronal_id': self.registro_patronal.id})
                if self.contract_id:
                    self.sueldo_mensual_ant = self.contract_id.wage
                    self.sueldo_diario_ant = self.contract_id.sueldo_diario
                    self.sueldo_diario_integrado_ant = self.contract_id.sueldo_diario_integrado
                    self.sueldo_por_horas_ant = self.contract_id.sueldo_hora
                    self.sueldo_cotizacion_base_ant = self.contract_id.sueldo_base_cotizacion
                    self.fecha_anterior = self.fecha
                    self.contract_id.write({'state':'open',
                                                 'sueldo_diario' : self.sueldo_diario,
                                                 'wage' : self.sueldo_mensual,
                                                 'sueldo_diario_integrado' : self.sueldo_diario_integrado,
                                                 'sueldo_base_cotizacion' : self.sueldo_cotizacion_base,
                                                 'sueldo_hora': self.sueldo_por_horas,
                                                 'date_start': self.fecha,
                                                 })
                    self.env['contract.historial.salario'].create({'sueldo_mensual': self.sueldo_mensual, 'sueldo_diario': self.sueldo_diario, 'fecha_sueldo': self.fecha,
                                                                   'sueldo_por_hora' : self.sueldo_por_horas, 'sueldo_diario_integrado': self.sueldo_diario_integrado,
                                                                   'sueldo_base_cotizacion': self.sueldo_cotizacion_base, 'contract_id' : self.contract_id.id
                                                                   })
        self.write({'state':'done'})
        return

    
    def action_cancelar(self):
       employee = self.employee_id
       if self.state == 'draft':
         self.write({'state':'cancel'})
       else:
          if self.tipo_de_incidencia == 'Reingreso':
              historial = self.env['contract.historial.salario'].search([('fecha_sueldo', '=', self.fecha)], limit=1)
              historial.unlink()
              employee.write({'active':False})
              if self.contract_id:
                  self.contract_id.write({'state':'cancel',
                                          'sueldo_diario' : self.sueldo_diario_ant,
                                          'wage' : self.sueldo_mensual_ant,
                                          'sueldo_diario_integrado' : self.sueldo_diario_integrado_ant,
                                          'sueldo_base_cotizacion' : self.sueldo_cotizacion_base_ant,
                                          'sueldo_hora': self.sueldo_por_horas_ant,
                                          'date_start': self.fecha_anterior,
                                          })
          elif self.tipo_de_incidencia == 'Baja':
              employee.write({'active':True})
              if self.contract_id:
                  self.contract_id.write({'state':'open'})
          elif self.tipo_de_incidencia == 'Cambio reg. patronal':
              employee.write({'registro_patronal_id': self.registro_patronal_ant.id})
          elif self.tipo_de_incidencia == 'Cambio salario':
              if self.contract_id:
                 self.contract_id.write({
                                         'sueldo_diario' : self.sueldo_diario_ant,
                                         'wage' : self.sueldo_mensual_ant,
                                         'sueldo_diario_integrado' : self.sueldo_diario_integrado_ant,
                                         'sueldo_base_cotizacion' : self.sueldo_cotizacion_base_ant,
                                         'sueldo_hora': self.sueldo_por_horas_ant,
                                         })
                 historial = self.env['contract.historial.salario'].search([('fecha_sueldo', '=', self.fecha)], limit=1)
                 historial.unlink()
          self.write({'state':'cancel'})

    def action_draft(self):
        self.write({'state':'draft'})

    def unlink(self):
        raise UserError("Los registros no se pueden borrar, solo cancelar.")
    
    def action_change_state(self):
        for incidencias in self:
            if incidencias.state == 'draft':
                incidencias.action_validar()

    def action_change_cancel(self):
        for incidencias in self:
             incidencias.action_cancelar()
