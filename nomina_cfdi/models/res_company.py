# -*- coding: utf-8 -*-
import base64
import json
import requests
from odoo import fields, models,api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class ResCompany(models.Model):
    _inherit = 'res.company'

    curp = fields.Char(string=_('CURP'))
    serie_nomina = fields.Char(string=_('Serie nomina'))
    registro_patronal = fields.Char(string=_('Registro patronal'))
    nomina_mail = fields.Char('Nomina Mail',)
    
    @api.model
    def contract_warning_mail_cron(self):
        companies = self.search([('nomina_mail','!=',False)])
        cr = self._cr
        dt = datetime.now()
        start_week_day = (dt - timedelta(days=dt.weekday())).date()
        end_week_day = start_week_day + timedelta(days=6)

        where_clause = []
        while start_week_day<=end_week_day:
            where_clause.append("TO_CHAR(date_start,'MM-DD')='%s-%s'"%("{0:0=2d}".format(start_week_day.month),"{0:0=2d}".format(start_week_day.day)))
            start_week_day = start_week_day + timedelta(days=1) #.date()
        where_clause = " OR ".join(where_clause)
        
        for company in companies:
            cr.execute("select id from hr_contract where (%s) and company_id=%d"%(where_clause,company.id))
            contract_ids = [r[0] for r in cr.fetchall()]
            if not contract_ids:
                continue
            for contract in self.env['hr.contract'].browse(contract_ids):
                if contract.state != 'open':
                   continue
                if contract.date_start.year == datetime.today().date().year:
                   continue
                change_done =  False
                for vacation_line in contract.tabla_vacaciones:
                    if str(vacation_line.ano) == str(start_week_day.year):
                       change_done =  True
                if not change_done:
                   if company.nomina_mail:
                         mail_values = {
                         'email_to': company.nomina_mail,
                         'subject': 'Aniversario de un empleado',
                         'body_html': 'Esta semana es el aniversario de ' +  contract.employee_id.name + ' en la empresa, revisar ajuste en sueldo creado en incidencias.',
                         'auto_delete': True,
                         }
                         mail = self.env['mail.mail'].create(mail_values)
                         mail.send()
                   self.calculate_contract_vacaciones(contract)
                   self.create_cambio_salario(contract)
        return

    @api.model
    def calculate_contract_vacaciones(self, contract):
        tablas_cfdi = contract.tablas_cfdi_id
        if not tablas_cfdi:
            tablas_cfdi = self.env['tablas.cfdi'].search([],limit=1)
        if not tablas_cfdi:
            return
        if contract.date_start:
            date_start = contract.date_start
            today = datetime.today().date()
            diff_date = today - date_start
            years = diff_date.days /365.0
            antiguedad_anos = round(years)
        else:
            antiguedad_anos = 0
        if antiguedad_anos < 1.0:
            tablas_cfdi_lines = tablas_cfdi.tabla_antiguedades.filtered(lambda x: x.antiguedad >= antiguedad_anos).sorted(key=lambda x:x.antiguedad)
        else:
            tablas_cfdi_lines = tablas_cfdi.tabla_antiguedades.filtered(lambda x: x.antiguedad <= antiguedad_anos).sorted(key=lambda x:x.antiguedad, reverse=True)
        if not tablas_cfdi_lines:
            return
        tablas_cfdi_line = tablas_cfdi_lines[0]
        today = datetime.today()
        current_year = today.strftime('%Y')
        contract.write({'tabla_vacaciones': [(0, 0, {'ano':current_year, 'dias': tablas_cfdi_line.vacaciones})]})
        return True

    @api.model
    def create_cambio_salario(self, contract):
        if contract.date_start:
            today = datetime.today().date()
            diff_date = (today - contract.date_start + timedelta(days=1)).days #today - date_start 
            years = diff_date /365.0
            tablas_cfdi = contract.tablas_cfdi_id
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
            sueldo_diario_integrado = ((365 + tablas_cfdi_line.aguinaldo + (tablas_cfdi_line.vacaciones)* (tablas_cfdi_line.prima_vac/100) ) / 365) * contract.wage/tablas_cfdi.dias_mes
            if sueldo_diario_integrado > (tablas_cfdi.uma * 25):
                sueldo_base_cotizacion = tablas_cfdi.uma * 25
            else:
                sueldo_base_cotizacion = sueldo_diario_integrado
            incidencia = self.env['incidencias.nomina'].create({'tipo_de_incidencia':'Cambio salario', 
                                                                'employee_id': contract.employee_id.id,
                                                                'sueldo_mensual': contract.wage,
                                                                'sueldo_diario': contract.sueldo_diario,
                                                                'sueldo_diario_integrado': sueldo_diario_integrado,
                                                                'sueldo_por_horas' : contract.sueldo_hora,
                                                                'sueldo_cotizacion_base': sueldo_base_cotizacion,
                                                                'fecha': today,
                                                                'contract_id': contract.id
                                                                })
        return
