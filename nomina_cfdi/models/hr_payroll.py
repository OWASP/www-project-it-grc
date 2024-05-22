# -*- coding: utf-8 -*-

import base64
import json
import requests
from lxml import etree
import datetime
from datetime import timedelta, date
from pytz import timezone
import math
import urllib.parse
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.lib.units import mm
import logging
_logger = logging.getLogger(__name__)
import pytz
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF, DEFAULT_SERVER_DATETIME_FORMAT as DTF 

from collections import defaultdict

class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    tipo_cpercepcion = fields.Many2one('nomina.percepcion', string='Tipo de percepción')
    tipo_cdeduccion = fields.Many2one('nomina.deduccion', string='Tipo de deducción')
    tipo_cotro_pago = fields.Many2one('nomina.otropago', string='Otros Pagos')

    category_code = fields.Char("Category Code",related="category_id.code",store=True)

    forma_pago = fields.Selection(
        selection=[('001', 'Efectivo'), 
                   ('002', 'Especie'),],
        string=_('Forma de pago'),default='001')
    exencion = fields.Boolean('Percepción con exención de ISR')
    integrar_al_ingreso = fields.Selection(
        selection=[('001', 'Ordinaria'), 
                   ('002', 'Extraordinaria mensual'),
                   ('003', 'Extraordinaria anual'),
                   ('004', 'Parte exenta por día'),],
        string=_('Integrar al ingreso gravable como percepción'))
#    monto_exencion = fields.Float('Exención (UMA)', digits = (12,3))
    variable_imss = fields.Boolean('Percepción variable para el IMSS')
    variable_imss_tipo = fields.Selection(
        selection=[('001', 'Todo el monto'), 
                   ('002', 'Excedente del (% de UMA)'),
                   ('003', 'Excedente del (% de SBC)'),],
        string=_('Tipo'),default='001')
    variable_imss_monto = fields.Float('Monto')
    integrar_ptu = fields.Boolean('Integrar para el PTU')
    integrar_estatal = fields.Boolean('Integrar para el impuesto estatal')
    parte_gravada = fields.Many2one('hr.salary.rule', string='Parte gravada')
    parte_exenta = fields.Many2one('hr.salary.rule', string='Parte exenta')
    cuenta_especie = fields.Many2one('account.account', 'Cuenta de pago', domain=[('deprecated', '=', False)])
    fondo_ahorro_aux = fields.Boolean('Fondo de ahorro')

class HrPayslip(models.Model):
    _name = "hr.payslip"
    _inherit = ['hr.payslip','mail.thread']


    tipo_nomina = fields.Selection(
        selection=[('O', 'Nómina ordinaria'), 
                   ('E', 'Nómina extraordinaria'),],
        string=_('Tipo de nómina'), required=True, default='O'
    )

    estado_factura = fields.Selection(
        selection=[('factura_no_generada', 'Factura no generada'), ('factura_correcta', 'Factura correcta'), 
                   ('problemas_factura', 'Problemas con la factura'), ('factura_cancelada', 'Factura cancelada')],
        string=_('Estado de factura'),
        default='factura_no_generada',
        readonly=True,
    )
    imss_dias = fields.Float('Cotizar en el IMSS',default='15') #, readonly=True) 
    imss_mes = fields.Float('Dias a cotizar en el mes',default='30') #, readonly=True)
    nomina_cfdi = fields.Boolean('Nomina CFDI')
    qrcode_image = fields.Binary("QRCode")
    qr_value = fields.Char(string=_('QR Code Value'))
    numero_cetificado = fields.Char(string=_('Numero de cetificado'))
    cetificaso_sat = fields.Char(string=_('Cetificao SAT'))
    folio_fiscal = fields.Char(string=_('Folio Fiscal'), readonly=True)
    fecha_certificacion = fields.Char(string=_('Fecha y Hora Certificación'))
    cadena_origenal = fields.Char(string=_('Cadena Origenal del Complemento digital de SAT'))
    selo_digital_cdfi = fields.Char(string=_('Selo Digital del CDFI'))
    selo_sat = fields.Char(string=_('Selo del SAT'))
    moneda = fields.Char(string=_('Moneda'))
    tipocambio = fields.Char(string=_('TipoCambio'))
    folio = fields.Char(string=_('Folio'))
    version = fields.Char(string=_('Version'))
    serie_emisor = fields.Char(string=_('Serie'))
    invoice_datetime = fields.Char(string=_('fecha factura'))
    rfc_emisor = fields.Char(string=_('RFC'))
    total_nomina = fields.Float('Total a pagar')
    subtotal = fields.Float('Subtotal')
    descuento = fields.Float('Descuento')
    #deducciones_lines = []
    number_folio = fields.Char(string=_('No. Folio'), compute='_get_number_folio')
    fecha_factura = fields.Datetime(string=_('Fecha Factura'))
    subsidio_periodo = fields.Float('subsidio_periodo')
    isr_periodo = fields.Float('isr_periodo')
    retencion_subsidio_pagado = fields.Float('retencion_subsidio_pagado')
    importe_imss = fields.Float('importe_imss')
    importe_isr = fields.Float('importe_isr')
    periodicidad = fields.Char('periodicidad')
    concepto_periodico = fields.Boolean('Conceptos periodicos', default = True)
    aplicar_descuentos = fields.Boolean('Aplicar descuentos', default = True)

    #imss empleado
    emp_exedente_smg = fields.Float(string='Exedente 3 SMGDF')
    emp_prest_dinero = fields.Float(string='Prest en dinero')
    emp_esp_pens = fields.Float(string='Gastos médicos')
    emp_invalidez_vida = fields.Float( string='Invalidez y Vida.')
    emp_cesantia_vejez = fields.Float(string='Cesantia y vejez')
    emp_total = fields.Float(string='IMSS trabajador')
    #imss patronal
    pat_cuota_fija_pat = fields.Float(string='Cuota fija patronal')
    pat_exedente_smg = fields.Float(string='Exedente 3 SMGDF.')
    pat_prest_dinero = fields.Float(string='Prest en dinero.')
    pat_esp_pens = fields.Float(string='Gastos médicos.')
    pat_riesgo_trabajo = fields.Float( string='Riegso de trabajo')
    pat_invalidez_vida = fields.Float( string='Invalidez y Vida')
    pat_guarderias = fields.Float(string='Guarderias y PS')
    pat_retiro = fields.Float( string='Retiro')
    pat_cesantia_vejez = fields.Float(string='Cesantia y vejez.')
    pat_infonavit = fields.Float(string='INFONAVIT')
    pat_total = fields.Float(string='IMSS patron')

    forma_pago = fields.Selection(
        selection=[('99', '99 - Por definir'),],
        string=_('Forma de pago'),default='99',
    )	
    tipo_comprobante = fields.Selection(
        selection=[('N', 'Nómina'),],
        string=_('Tipo de comprobante'),default='N',
    )	
    tipo_relacion = fields.Selection(
        selection=[('04', 'Sustitución de los CFDI previos'),],
        string=_('Tipo relación'),
    )
    uuid_relacionado = fields.Char(string=_('CFDI Relacionado'))
    methodo_pago = fields.Selection(
        selection=[('PUE', _('Pago en una sola exhibición')),],
        string=_('Método de pago'), default='PUE',
    )	
    uso_cfdi = fields.Selection(
        selection=[('P01', _('Por definir')),('CN01', _('Nomina')),],
        string=_('Uso CFDI (cliente)'),default='CN01',
    )
    fecha_pago = fields.Date(string=_('Fecha de pago'))
    dias_pagar = fields.Float('Pagar en la nomina')
    ultima_nomina = fields.Boolean(string='Última nómina del mes')
    acum_per_totales = fields.Float('Percepciones totales', readonly=True) #, compute='_get_acumulados_mensual')
    acum_per_grav  = fields.Float('Percepciones gravadas', readonly=True) #, compute='_get_acumulados_mensual')
    acum_isr  = fields.Float('ISR', readonly=True) #, compute='_get_acumulados_mensual')
    acum_isr_antes_subem  = fields.Float('ISR antes de SUBEM', readonly=True) #, compute='_get_acumulados_mensual')
    acum_subsidio_aplicado  = fields.Float('Subsidio aplicado', readonly=True) #, compute='_get_acumulados_mensual')
    acum_fondo_ahorro = fields.Float('Acumulado Caja/Fondo ahorro', readonly=True) #, compute='_get_fondo_ahorro')
    #acum_fondo_ahorro_anual = fields.Float('Fondo ahorro anual', readonly=True) #, compute='_get_fondo_ahorro_anual')
    dias_periodo = fields.Float(string=_('Dias en el periodo'), compute='_get_dias_periodo')
    #isr_devolver = fields.Boolean(string='Devolver ISR')
    isr_ajustar = fields.Boolean(string='Ajustar ISR (mensual)')
    acum_sueldo = fields.Float('Sueldo', readonly=True) #, compute='_get_acumulados_mensual')

    acum_per_grav_anual  = fields.Float('Percepciones gravadas (anual)', readonly=True) #, compute='_get_acumulados_anual')
    acum_isr_anual  = fields.Float('ISR (anual)', readonly=True) #, compute='_get_acumulados_anual')
    acum_isr_antes_subem_anual  = fields.Float('ISR antes de SUBEM (anual)', readonly=True) #, compute='_get_acumulados_anual')
    acum_subsidio_aplicado_anual  = fields.Float('Subsidio aplicado (anual)', readonly=True) #, compute='_get_acumulados_anual')
    isr_anual = fields.Boolean(string='ISR anual')
    acum_dev_isr  = fields.Float('Devolución ISR (anual)', readonly=True) #, compute='_get_acumulados_anual')
    acum_dev_subem  = fields.Float('Ajuste al SUBEM (anual)', readonly=True) #, compute='_get_acumulados_anual')
    acum_dev_subem_entregado  = fields.Float('Ajuste al SUBEM entregado (anual)', readonly=True) #, compute='_get_acumulados_anual')
    acum_isr_ajuste  = fields.Float('Ajuste ISR (anual)', readonly=True) #, compute='_get_acumulados_anual')

    acum_prima_vac_exento  = fields.Float('Acumulado Prima vacacional exento', readonly=True) #, compute='_get_acumulado_prima_vac')

    mes = fields.Selection(
        selection=[('01', 'Enero / Periodo 1'),
                   ('02', 'Febrero / Periodo 2'),
                   ('03', 'Marzo / Periodo 3'),
                   ('04', 'Abril / Periodo 4'),
                   ('05', 'Mayo / Periodo 5'),
                   ('06', 'Junio / Periodo 6'),
                   ('07', 'Julio / Periodo 7'),
                   ('08', 'Agosto / Periodo 8'),
                   ('09', 'Septiembre / Periodo 9' ),
                   ('10', 'Octubre / Periodo 10'),
                   ('11', 'Noviembre / Periodo 11'),
                   ('12', 'Diciembre / Periodo 12'),
                   ],
        string=_('Mes de la nómina'))
    nom_liquidacion = fields.Boolean(string='Nomina de liquidacion', default=False)
    periodicidad_pago = fields.Char(
        string=_('Periodicidad de pago CFDI'), compute='_get_periodicidad',
    )
    dias_infonavit = fields.Float('Días INFONAVIT')
    cumpleanos = fields.Boolean(string=_('Cumpleaños'), compute='_get_cumpleanos', default = False)
    total_nom = fields.Float('Total')

    def get_amount_from_rule_code(self, rule_code):
        line = self.env['hr.payslip.line'].search([('slip_id', '=', self.id), ('code', '=', rule_code)])
        if line:
            return round(sum(line.mapped('total')), 2)
        else:
            return 0.0

    @api.model
    def get_worked_day_lines(self, contracts, date_from, date_to):
        """
        @param contract: Browse record of contracts
        @return: returns a list of dict containing the input that should be applied for the given contract between date_from and date_to
        """
        res = []
        horas_obj = self.env['horas.nomina']
        tipo_de_hora_mapping = {'1':'HEX1', '2':'HEX2', '3':'HEX3', '4':'HEX4'}
        
        def is_number(s):
            try:
                return float(s)
            except ValueError:
                return 0

        # fill only if the contract as a working schedule linked
        for contract in contracts.filtered(lambda contract: contract.resource_calendar_id):
            day_from = datetime.datetime.combine(fields.Date.from_string(date_from), datetime.time.min)
            day_to = datetime.datetime.combine(fields.Date.from_string(date_to), datetime.time.max)
            nb_of_days = (day_to - day_from).days + 1

            # compute Prima vacacional en fecha correcta
            if contract.tipo_prima_vacacional == '01':
                date_start = contract.date_start
                if date_start:
                    d_from = fields.Date.from_string(date_from)
                    d_to = fields.Date.from_string(date_to)
                
                    date_start = fields.Date.from_string(date_start)
                    if datetime.datetime.today().year > date_start.year:
                        if str(date_start.day) == '29' and str(date_start.month) == '2':
                            date_start -=  datetime.timedelta(days=1)
                        date_start = date_start.replace(d_to.year)

                        if d_from <= date_start <= d_to:
                            diff_date = day_to - datetime.datetime.combine(contract.date_start, datetime.time.max)
                            years = diff_date.days /365.0
                            antiguedad_anos = int(years)
                            tabla_antiguedades = contract.tablas_cfdi_id.tabla_antiguedades.filtered(lambda x: x.antiguedad <= antiguedad_anos)
                            tabla_antiguedades = tabla_antiguedades.sorted(lambda x:x.antiguedad, reverse=True)
                            vacaciones = tabla_antiguedades and tabla_antiguedades[0].vacaciones or 0
                            prima_vac = tabla_antiguedades and tabla_antiguedades[0].prima_vac or 0
                            attendances = {
                                 'name': 'Prima vacacional',
                                 'sequence': 2,
                                 'code': 'PVC',
                                 'number_of_days': vacaciones * prima_vac / 100.0, #work_data['days'],
                                 'number_of_hours': vacaciones * prima_vac / 100.0 * 8,
                                 'contract_id': contract.id,
                            }
                            res.append(attendances)

            # compute Prima vacacional
            if contract.tipo_prima_vacacional == '03':
                date_start = contract.date_start
                if date_start:
                    d_from = fields.Date.from_string(date_from)
                    d_to = fields.Date.from_string(date_to)

                    date_start = fields.Date.from_string(date_start)
                    if datetime.datetime.today().year > date_start.year and d_from.day > 15:
                        if str(date_start.day) == '29' and str(date_start.month) == '2':
                            date_start -=  datetime.timedelta(days=1)
                        date_start = date_start.replace(d_to.year)
                        d_from = d_from.replace(day=1)

                        if d_from <= date_start <= d_to:
                            diff_date = day_to - datetime.datetime.combine(contract.date_start, datetime.time.max)
                            years = diff_date.days /365.0
                            antiguedad_anos = int(years)
                            tabla_antiguedades = contract.tablas_cfdi_id.tabla_antiguedades.filtered(lambda x: x.antiguedad <= antiguedad_anos)
                            tabla_antiguedades = tabla_antiguedades.sorted(lambda x:x.antiguedad, reverse=True)
                            vacaciones = tabla_antiguedades and tabla_antiguedades[0].vacaciones or 0
                            prima_vac = tabla_antiguedades and tabla_antiguedades[0].prima_vac or 0
                            attendances = {
                                 'name': 'Prima vacacional',
                                 'sequence': 2,
                                 'code': 'PVC',
                                 'number_of_days': vacaciones * prima_vac / 100.0, #work_data['days'],
                                 'number_of_hours': vacaciones * prima_vac / 100.0 * 8,
                                 'contract_id': contract.id,
                            }
                            res.append(attendances)

            # compute Prima dominical
            if contract.prima_dominical:
                domingos = 0
                d_from = fields.Date.from_string(date_from)
                d_to = fields.Date.from_string(date_to)
                for i in range((d_to - d_from).days + 1):
                    if (d_from + datetime.timedelta(days=i+1)).weekday() == 0:
                        domingos = domingos + 1
                attendances = {
                            'name': 'Prima dominical',
                            'sequence': 2,
                            'code': 'PDM',
                            'number_of_days': domingos, #work_data['days'],
                            'number_of_hours': domingos * 8,
                            'contract_id': contract.id,
                     }
                res.append(attendances)

            # compute leave days
            leaves = {}
            leave_days = 0
            inc_days = 0
            vac_days = 0
            factor = 0
            falta_days = 0
            if contract.semana_inglesa:
                factor = 7.0/5.0
            else:
                factor = 7.0/6.0

            if contract.periodicidad_pago == '04':
                dias_pagar = 15
            elif contract.periodicidad_pago == '02':
                dias_pagar = 7
            else:
                dias_pagar = (date_to - date_from).days + 1

            calendar = contract.resource_calendar_id
            tz = timezone(calendar.tz)
            day_leave_intervals = contract.employee_id.list_leaves(day_from, day_to, calendar=contract.resource_calendar_id)
            for day, hours, leave in day_leave_intervals:
                holiday = leave.holiday_id
                if not holiday.holiday_status_id.code:
                   raise UserError(_('La ausencia no cuenta con un código'))
                current_leave_struct = leaves.setdefault(holiday.holiday_status_id, {
                    'name': holiday.holiday_status_id.name or _('Global Leaves'),
                    'sequence': 5,
                    'code': holiday.holiday_status_id.code or 'GLOBAL',
                    'number_of_days': 0.0,
                    'number_of_hours': 0.0,
                    'contract_id': contract.id,
                })
                #current_leave_struct['number_of_hours'] += hours
                work_hours = calendar.get_work_hours_count(
                    tz.localize(datetime.datetime.combine(day, datetime.time.min)),
                    tz.localize(datetime.datetime.combine(day, datetime.time.max)),
                    compute_leaves=False,
                )
                if work_hours and contract.septimo_dia:
                        if contract.incapa_sept_dia:
                           if holiday.holiday_status_id.code == 'FJS' or holiday.holiday_status_id.code == 'FI' or holiday.holiday_status_id.code == 'FR':
                              falta_days += 1
                              leave_days += (hours / work_hours)*factor
                              current_leave_struct['number_of_days'] += (hours / work_hours)*factor
                              if leave_days > dias_pagar:
                                 leave_days = dias_pagar
                              if current_leave_struct['number_of_days'] > dias_pagar:
                                 current_leave_struct['number_of_days'] = dias_pagar
                           elif holiday.holiday_status_id.code == 'INC_EG' or holiday.holiday_status_id.code == 'INC_RT' or holiday.holiday_status_id.code == 'INC_MAT':
                              leave_days += hours / work_hours
                              inc_days += 1
                              current_leave_struct['number_of_days'] += hours / work_hours
                           else:
                              if holiday.holiday_status_id.code != 'DFES' and holiday.holiday_status_id.code != 'DFES_3':
                                 leave_days += hours / work_hours
                              current_leave_struct['number_of_days'] += hours / work_hours
                              if holiday.holiday_status_id.code == 'VAC' or holiday.holiday_status_id.code == 'FJC':
                                 vac_days += 1
                        else:
                           if holiday.holiday_status_id.code == 'FJS' or holiday.holiday_status_id.code == 'FI' or holiday.holiday_status_id.code == 'FR':
                              falta_days += 1
                              leave_days += (hours / work_hours)*factor
                              current_leave_struct['number_of_days'] += (hours / work_hours)*factor
                              if leave_days > dias_pagar:
                                 leave_days = dias_pagar
                              if current_leave_struct['number_of_days'] > dias_pagar:
                                 current_leave_struct['number_of_days'] = dias_pagar
                           else:
                              if holiday.holiday_status_id.code != 'DFES' and holiday.holiday_status_id.code != 'DFES_3':
                                 leave_days += hours / work_hours
                              current_leave_struct['number_of_days'] += hours / work_hours
                              if holiday.holiday_status_id.code == 'VAC' or holiday.holiday_status_id.code == 'FJC':
                                 vac_days += 1
                elif work_hours:
                        if contract.incapa_sept_dia:
                           if holiday.holiday_status_id.code == 'INC_EG' or holiday.holiday_status_id.code == 'INC_RT' or holiday.holiday_status_id.code == 'INC_MAT':
                              leave_days += (hours / work_hours)*factor
                              inc_days += 1
                              current_leave_struct['number_of_days'] += (hours / work_hours)*factor
                           else:
                              if holiday.holiday_status_id.code != 'DFES' and holiday.holiday_status_id.code != 'DFES_3':
                                 leave_days += hours / work_hours
                              current_leave_struct['number_of_days'] += hours / work_hours
                              if holiday.holiday_status_id.code == 'VAC' or holiday.holiday_status_id.code == 'FJC':
                                 vac_days += 1
                        else:
                           if holiday.holiday_status_id.code != 'DFES' and holiday.holiday_status_id.code != 'DFES_3':
                              leave_days += hours / work_hours
                           current_leave_struct['number_of_days'] += hours / work_hours
                           if holiday.holiday_status_id.code == 'VAC' or holiday.holiday_status_id.code == 'FJC':
                              vac_days += 1
                           if holiday.holiday_status_id.code == 'INC_EG' or holiday.holiday_status_id.code == 'INC_RT' or holiday.holiday_status_id.code == 'INC_MAT':
                              inc_days += 1

            # compute worked days
            work_data = contract.employee_id._get_work_days_data(day_from, day_to, calendar=contract.resource_calendar_id)
            number_of_days = 0

            # ajuste en caso de nuevo ingreso
            nvo_ingreso = False
            date_start_1 = contract.date_start
            d_from_1 = fields.Date.from_string(date_from)
            d_to_1 = fields.Date.from_string(date_to)
            if date_start_1 > d_from_1:
                   work_data['days'] =  (date_to - date_start_1).days + 1
                   nvo_ingreso = True
            if contract.date_end:
               if d_from_1 <= contract.date_end <= d_to_1:
                   if d_to_1 > date_start_1:
                       work_data['days'] =  (contract.date_end - date_from).days + 1
                       nvo_ingreso = True

            #dias_a_pagar = contract.dias_pagar
            #_logger.info('dias trabajados %s  dias incidencia %s', work_data['days'], leave_days)

            if work_data['days'] < 100:
            #periodo para nómina quincenal
               if contract.periodicidad_pago == '04':
                   if contract.tipo_pago == '01' and nb_of_days < 17:
                      total_days = work_data['days'] + leave_days
                      if total_days != 15 or leave_days != 0:
                         if leave_days == 0 and not nvo_ingreso:
                            number_of_days = 15
                         elif nvo_ingreso:
                            number_of_days = work_data['days'] - leave_days
                         else:
                            number_of_days = 15 - leave_days
                      else:
                         number_of_days = work_data['days']
                      if contract.sept_dia:
                         aux = 2.5
                         number_of_days -=  aux
                         attendances = {
                             'name': _("Séptimo día"),
                             'sequence': 3,
                             'code': "SEPT",
                             'number_of_days': aux, 
                             'number_of_hours': 0.0,
                             'contract_id': contract.id,
                         }
                         res.append(attendances)
                   elif contract.tipo_pago == '03' and nb_of_days < 17:
                      total_days = work_data['days'] + leave_days
                      if total_days != 15.21 or leave_days != 0:
                         if leave_days == 0  and not nvo_ingreso:
                            number_of_days = 15.21
                         elif nvo_ingreso:
                            number_of_days = work_data['days'] * 15.21 / 15 - leave_days
                         else:
                            number_of_days = 15.21 - leave_days
                      else:
                         number_of_days = work_data['days'] * 15.21 / 15
                      if contract.sept_dia:
                         aux = 2.21
                         number_of_days -=  aux
                         attendances = {
                             'name': _("Séptimo día"),
                             'sequence': 3,
                             'code': "SEPT",
                             'number_of_days': aux, 
                             'number_of_hours': 0.0,
                             'contract_id': contract.id,
                         }
                         res.append(attendances)
                   else:
                      dias_periodo = (date_to - date_from).days + 1
                      total_days = work_data['days'] + leave_days
                      if total_days != dias_periodo or leave_days != 0:
                         if leave_days == 0  and not nvo_ingreso:
                            number_of_days = dias_periodo
                         elif nvo_ingreso:
                            number_of_days = work_data['days'] - leave_days
                         else:
                            number_of_days = dias_periodo - leave_days
                      else:
                         number_of_days = work_data['days']
                   if falta_days >= 15 or inc_days >= 15 or vac_days >= 15:
                      number_of_days = 0
               #calculo para nóminas semanales
               elif contract.periodicidad_pago == '02' and nb_of_days < 8:
                   number_of_days = work_data['days']
                ##   if contract.septimo_dia: #falta proporcional por septimo día
                   total_days = work_data['days'] + leave_days
                   if total_days != 7 or leave_days != 0:
                      if leave_days == 0  and not nvo_ingreso:
                         number_of_days = 7
                      elif nvo_ingreso:
                         number_of_days = work_data['days'] - leave_days
                      else:
                         number_of_days = 7 - leave_days
                   else:
                      number_of_days = work_data['days']
                   if contract.sept_dia: # septimo día
                      if number_of_days == 0:
                         if leave_days != 7:
                            number_of_days = work_data['days']
                      if contract.semana_inglesa:
                         aux = number_of_days / 7 * 2
                      else:
                         aux = number_of_days - int(number_of_days)
                      #_logger.info('number_of_days %s  aux %s', number_of_days, aux)
                      if aux > 0:
                         number_of_days -=  aux
                      elif number_of_days > 0:
                         if contract.semana_inglesa:
                            number_of_days -= 2
                            if contract.incapa_sept_dia:
                               aux = (number_of_days + inc_days + vac_days) / 5
                            else:
                               aux = (number_of_days + vac_days)/ 5
                         else:
                            #if not nvo_ingreso:
                            number_of_days -= 1
                            if contract.incapa_sept_dia:
                               aux = (number_of_days + inc_days + vac_days) / 6
                            else:
                               aux = (number_of_days + vac_days)/ 6
                      attendances = {
                          'name': _("Séptimo día"),
                          'sequence': 3,
                          'code': "SEPT",
                          'number_of_days': aux, 
                          'number_of_hours': round(aux*8,2),
                          'contract_id': contract.id,
                      }
                      res.append(attendances)
                      if falta_days >= 6 or inc_days >= 6 or vac_days >= 6:
                         number_of_days = 0
                   else:
                      if falta_days >= 6 or inc_days >= 6 or vac_days >= 6:
                         number_of_days = 0
               #calculo para nóminas mensuales
               elif contract.periodicidad_pago == '05':
                  if contract.tipo_pago == '01':
                      total_days = work_data['days'] + leave_days
                      if total_days != 30:
                         if leave_days == 0 and not nvo_ingreso:
                            number_of_days = 30
                         elif nvo_ingreso:
                            number_of_days = work_data['days'] - leave_days
                         else:
                            number_of_days = 30 - leave_days
                  elif contract.tipo_pago == '03':
                      total_days = work_data['days'] + leave_days
                      if total_days != 30.42:
                         if leave_days == 0  and not nvo_ingreso:
                            number_of_days = 30.42
                         elif nvo_ingreso:
                            number_of_days = work_data['days'] * 30.42 / 30 - leave_days
                         else:
                            number_of_days = 30.42 - leave_days
                      else:
                         number_of_days = work_data['days'] * 30.42 / 30
                  else:
                      dias_periodo = (date_to - date_from).days + 1
                      total_days = work_data['days'] + leave_days
                      if total_days != dias_periodo:
                         if leave_days == 0  and not nvo_ingreso:
                            number_of_days = dias_periodo
                         elif nvo_ingreso:
                            number_of_days = work_data['days'] - leave_days
                         else:
                            number_of_days = dias_periodo - leave_days
                      else:
                         number_of_days = work_data['days']
               else:
                  number_of_days = work_data['days']
            else:
               date_start = contract.date_start
               if date_start:
                   d_from = fields.Date.from_string(date_from)
                   d_to = fields.Date.from_string(date_to)
               if date_start > date_from:
                   number_of_days =  (date_to - date_start).days + 1 - leave_days
               else:
                   number_of_days =  (date_to - date_from).days + 1 - leave_days
            attendances = {
                'name': _("Días de trabajo"),
                'sequence': 1,
                'code': 'WORK100',
                'number_of_days': number_of_days, #work_data['days'],
                'number_of_hours': round(number_of_days*8,2), # work_data['hours'],
                'contract_id': contract.id,
            }
            res.append(attendances)

            #Compute horas extas
            horas = horas_obj.search([('employee_id','=',contract.employee_id.id),('fecha','>=',date_from), ('fecha', '<=', date_to),('state','=','done')])
            horas_by_tipo_de_horaextra = defaultdict(list)
            for h in horas:
                horas_by_tipo_de_horaextra[h.tipo_de_hora].append(h.horas)
            
            for tipo_de_hora, horas_set in horas_by_tipo_de_horaextra.items():
                work_code = tipo_de_hora_mapping.get(tipo_de_hora,'')
                number_of_days = len(horas_set)
                number_of_hours = sum(is_number(hs) for hs in horas_set)

                if work_code == 'HEX4':
                   if contract.periodicidad_pago == '04': #quincenal
                      if number_of_hours <= 18:
                         attendances = {
                            'name': _("Horas extras"),
                            'sequence': 2,
                            'code': 'HEX2',
                            'number_of_days': int(math.ceil(number_of_hours/3)), 
                            'number_of_hours': number_of_hours,
                            'contract_id': contract.id,
                         }
                      else:
                         attendances2 = {
                            'name': _("Horas extras"),
                            'sequence': 2,
                            'code': 'HEX2',
                            'number_of_days': 6, 
                            'number_of_hours': 18,
                            'contract_id': contract.id,
                         }
                         res.append(attendances2)
                         attendances = {
                            'name': _("Horas extras"),
                            'sequence': 2,
                            'code': 'HEX3',
                            'number_of_days': int(math.ceil((number_of_hours - 18)/3)),
                            'number_of_hours': number_of_hours - 18,
                            'contract_id': contract.id,
                         }
                else:
                   attendances = {
                       'name': _("Horas extras"),
                       'sequence': 2,
                       'code': work_code,
                       'number_of_days': number_of_days, 
                       'number_of_hours': number_of_hours,
                       'contract_id': contract.id,
                   }
                res.append(attendances)

            #Compute prima dominical
            prima_dominical_obj = self.env['prima.dominical']
            prima_dominical = prima_dominical_obj.search([('employee_id','=',contract.employee_id.id),('fecha','>=',date_from), ('fecha', '<=', date_to),('state','=','done')])
            if prima_dominical:
                   attendances = {
                            'name': 'Prima dominical',
                            'sequence': 2,
                            'code': 'PDM',
                            'number_of_days': len(prima_dominical),
                            'number_of_hours': len(prima_dominical) * 8,
                            'contract_id': contract.id,
                   }
                   res.append(attendances)

            res.extend(leaves.values())

        return res

   # @api.onchange('contract_id')
    def _get_periodicidad(self):
        for invoice in self:
          invoice.periodicidad_pago = invoice.contract_id.periodicidad_pago

    def set_fecha_pago(self, payroll_name):
            values = {
                'payslip_run_id': payroll_name
                }
            self.update(values)

    @api.onchange('date_to')
    def _get_fecha_pago(self):
        if self.date_to:
            values = {
                'fecha_pago': self.date_to
                }
            self.update(values)

    @api.onchange('date_to')
    def _get_dias_periodo(self):
        self.dias_periodo = 0
        if self.mes:
            line = self.contract_id.env['tablas.periodo.mensual'].search([('form_id','=',self.contract_id.tablas_cfdi_id.id),('mes','=',self.mes)],limit=1)
            if line:
                self.dias_periodo = line.no_dias
            else:
                raise UserError(_('No están configurados correctamente los periodos en las tablas CFDI'))

    @api.model
    def create(self, vals):
        if not vals.get('fecha_pago') and vals.get('date_to'):
            vals.update({'fecha_pago': vals.get('date_to')})
            
        res = super(HrPayslip, self).create(vals)
        return res
    
    @api.depends('number')
    def _get_number_folio(self):
        if self.number:
            self.number_folio = self.number.replace('SLIP','').replace('NOM','').replace('/','')
        else:
            raise UserError(_('La nómina no tiene un número asignado.'))

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {})
        if self.estado_factura == 'factura_correcta' or self.estado_factura == 'factura_cancelada':
            default['estado_factura'] = 'factura_no_generada'
            default['folio_fiscal'] = ''
            default['fecha_factura'] = None
            default['nomina_cfdi'] = False
        return super(HrPayslip, self).copy(default=default)

    def _get_fondo_ahorro(self):
        total = 0
        if self.employee_id and self.contract_id.tablas_cfdi_id:
            abono = 0
            retiro = 0
            domain=[('state','=', 'done')]
            domain.append(('employee_id','=',self.employee_id.id))
            if self.contract_id.tablas_cfdi_id.caja_ahorro_abono:
                        rules = self.env['hr.salary.rule'].search([('code', '=', self.contract_id.tablas_cfdi_id.caja_ahorro_abono.code)])
                        payslips = self.env['hr.payslip'].search(domain)
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
            if self.contract_id.tablas_cfdi_id.caja_ahorro_retiro:
                        rules = self.env['hr.salary.rule'].search([('code', '=', self.contract_id.tablas_cfdi_id.caja_ahorro_retiro.code)])
                        payslips = self.env['hr.payslip'].search(domain)
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
            self.acum_fondo_ahorro = abono - retiro

    def acumulado_mes(self, codigo):
        total = 0
        if self.employee_id and self.contract_id.tablas_cfdi_id:
            mes_actual = self.contract_id.tablas_cfdi_id.tabla_mensual.search([('mes', '=', self.mes), ('form_id', '=', self.contract_id.tablas_cfdi_id.id)],limit =1)
            date_start = mes_actual.dia_inicio # self.date_from
            date_end = mes_actual.dia_fin #self.date_to
            domain=[('state','=', 'done')]
            if date_start:
                domain.append(('date_from','>=',date_start))
            if date_end:
                domain.append(('date_to','<=',date_end))
            domain.append(('employee_id','=',self.employee_id.id))
            if not self.contract_id.calc_isr_extra:
               domain.append(('tipo_nomina','=','O'))
            rules = self.env['hr.salary.rule'].search([('code', '=', codigo)])
            payslips = self.env['hr.payslip'].search(domain)
            payslip_lines = payslips.mapped('line_ids').filtered(lambda x: x.salary_rule_id.id in rules.ids)
            employees = {}
            for line in payslip_lines:
                if line.slip_id.employee_id not in employees:
                    employees[line.slip_id.employee_id] = {line.slip_id: []}
                if line.slip_id not in employees[line.slip_id.employee_id]:
                    employees[line.slip_id.employee_id].update({line.slip_id: []})
                employees[line.slip_id.employee_id][line.slip_id].append(line)

            for employee, payslips in employees.items():
                for payslip,lines in payslips.items():
                    for line in lines:
                        total += line.total
        return total

    def mensual(self, employee_id, contract_id, mes, codigo):
        total = 0
        if employee_id and contract_id.tablas_cfdi_id:
            mes_actual = contract_id.tablas_cfdi_id.tabla_mensual.search([('mes', '=', mes), ('form_id', '=', contract_id.tablas_cfdi_id.id)],limit =1)
            date_start = mes_actual.dia_inicio # self.date_from
            date_end = mes_actual.dia_fin #self.date_to
            domain=[('state','=', 'done')]
            if date_start:
                domain.append(('date_from','>=',date_start))
            if date_end:
                domain.append(('date_to','<=',date_end))
            domain.append(('employee_id','=',employee_id.id))
            if not contract_id.calc_isr_extra:
               domain.append(('tipo_nomina','=','O'))
            rules = self.env['hr.salary.rule'].search([('code', '=', codigo)])
            payslips = self.env['hr.payslip'].search(domain)
            payslip_lines = payslips.mapped('line_ids').filtered(lambda x: x.salary_rule_id.id in rules.ids)
            employees = {}
            for line in payslip_lines:
                if line.slip_id.employee_id not in employees:
                    employees[line.slip_id.employee_id] = {line.slip_id: []}
                if line.slip_id not in employees[line.slip_id.employee_id]:
                    employees[line.slip_id.employee_id].update({line.slip_id: []})
                employees[line.slip_id.employee_id][line.slip_id].append(line)

            for employee, payslips in employees.items():
                for payslip,lines in payslips.items():
                    for line in lines:
                        total += line.total
        return total

    def anual(self, employee_id, contract_id, date_from, codigo):
        total = 0
        if employee_id and contract_id.tablas_cfdi_id:
            date_start = date(fields.Date.from_string(date_from).year, 1, 1)
            date_end = date(fields.Date.from_string(date_from).year, 12, 31)
            domain=[('state','=', 'done')]
            if date_start:
                domain.append(('date_from','>=',date_start))
            if date_end:
                domain.append(('date_to','<=',date_end))
            domain.append(('employee_id','=',employee_id.id))
            if codigo != 'ISR2':
               rules = self.env['hr.salary.rule'].search([('code', '=', codigo)])
               payslips = self.env['hr.payslip'].search(domain)
               payslip_lines = payslips.mapped('line_ids').filtered(lambda x: x.salary_rule_id.id in rules.ids)
               employees = {}
               for line in payslip_lines:
                   if line.slip_id.employee_id not in employees:
                       employees[line.slip_id.employee_id] = {line.slip_id: []}
                   if line.slip_id not in employees[line.slip_id.employee_id]:
                       employees[line.slip_id.employee_id].update({line.slip_id: []})
                   employees[line.slip_id.employee_id][line.slip_id].append(line)

               for employee, payslips in employees.items():
                   for payslip,lines in payslips.items():
                       for line in lines:
                           total += line.total
            else:
               payslips = self.env['hr.payslip'].search(domain)
               for slip in payslips:
                   isr = 0
                   isr_antes = 0
                   for line in slip.line_ids:
                      if line.code == 'ISR2':
                         isr = line.total
                      elif line.code == 'ISR':
                         isr_antes = line.total
                   if isr > isr_antes:
                      total += isr
                   else:
                      total += isr_antes
        return total

    def acumulado_anual(self, codigo):
        total = 0
        if self.employee_id and self.contract_id.tablas_cfdi_id:
            date_start = date(fields.Date.from_string(self.date_from).year, 1, 1)
            date_end = date(fields.Date.from_string(self.date_from).year, 12, 31)
            domain=[('state','=', 'done')]
            if date_start:
                domain.append(('date_from','>=',date_start))
            if date_end:
                domain.append(('date_to','<=',date_end))
            domain.append(('employee_id','=',self.employee_id.id))
            if codigo != 'ISR2':
               rules = self.env['hr.salary.rule'].search([('code', '=', codigo)])
               payslips = self.env['hr.payslip'].search(domain)
               payslip_lines = payslips.mapped('line_ids').filtered(lambda x: x.salary_rule_id.id in rules.ids)
               employees = {}
               for line in payslip_lines:
                   if line.slip_id.employee_id not in employees:
                       employees[line.slip_id.employee_id] = {line.slip_id: []}
                   if line.slip_id not in employees[line.slip_id.employee_id]:
                       employees[line.slip_id.employee_id].update({line.slip_id: []})
                   employees[line.slip_id.employee_id][line.slip_id].append(line)

               for employee, payslips in employees.items():
                   for payslip,lines in payslips.items():
                       for line in lines:
                           total += line.total
            else:
               payslips = self.env['hr.payslip'].search(domain)
               for slip in payslips:
                   isr = 0
                   isr_antes = 0
                   for line in slip.line_ids:
                      if line.code == 'ISR2':
                         isr = line.total
                      elif line.code == 'ISR':
                         isr_antes = line.total
                   if isr > isr_antes:
                      total += isr
                   else:
                      total += isr_antes
        return total

    def _get_acumulados_mensual(self):
         if self.state != 'done':
             self.acum_sueldo = self.acumulado_mes('P001')
             self.acum_per_totales = self.acumulado_mes('TPER')
             self.acum_subsidio_aplicado = self.acumulado_mes('SUB')
             self.acum_isr_antes_subem = self.acumulado_mes('ISR')
             self.acum_per_grav = self.acumulado_mes('TPERG')
             self.acum_isr = self.acumulado_mes('ISR2')

    def _get_acumulados_anual(self):
         if self.state != 'done' and self.isr_anual:
             self.acum_subsidio_aplicado_anual = self.acumulado_anual('SUB')
            # self.acum_isr_antes_subem_anual = self.acumulado_anual('ISR')
             self.acum_per_grav_anual = self.acumulado_anual('TPERG')
             self.acum_isr_anual = self.acumulado_anual('ISR2')
             self.acum_dev_isr = self.acumulado_anual('O007')
             self.acum_dev_subem = self.acumulado_anual('D061')
             self.acum_dev_subem_entregado = self.acumulado_anual('D062')
             self.acum_isr_ajuste = self.acumulado_anual('D060')

    def _get_acumulado_prima_vac(self):
         self.acum_prima_vac_exento = self.acumulado_anual('PE010')

    def _validate_slip_fields(self):
         if not self.contract_id:
             raise UserError(_('El empleado %s no tiene contrato asignado.') % (self.employee_id.name))
         if not self.contract_id.tablas_cfdi_id:
             raise UserError(_('El empleado %s no tiene tablas CFDI asignado en el contrato.') % (self.employee_id.name))
         if self.dias_pagar <= 0:
             raise UserError(_('El empleado %s no tiene asignados días a pagar.') % (self.employee_id.name))

    @api.model
    def to_json(self):
        payslip_total_TOP = 0
        payslip_total_TDED = 0
        payslip_total_PERG = 0
        payslip_total_PERE = 0
        payslip_total_SEIN = 0
        payslip_total_JPRE = 0
        antiguedad = 1
        #if self.contract_id.date_end and self.contract_id.date_start:
        #    antiguedad = int((self.contract_id.date_end - self.contract_id.date_start + timedelta(days=1)).days/7)
        if self.date_to and self.contract_id.date_start:
            antiguedad = int((self.date_to - self.contract_id.date_start + timedelta(days=1)).days/7)

#**********  Percepciones ************
        #total_percepciones_lines = self.env['hr.payslip.line'].search(['|',('category_id.code','=','ALW'),('category_id.code','=','BASIC'),('category_id.code','=','ALW3'),('slip_id','=',self.id)])
        percepciones_grabadas_lines = self.env['hr.payslip.line'].search(['|',('category_id.code','=','ALW'),('category_id.code','=','BASIC'),('slip_id','=',self.id)])
      #  percepciones_grabadas_lines = self.env['hr.payslip.line'].search([('slip_id','=',self.id)])
        lineas_de_percepcion = []
        lineas_de_percepcion_exentas = []
        percepciones_excentas_lines = 0
        #_logger.info('Total conceptos %s id %s', len(percepciones_grabadas_lines), self.id)
        if percepciones_grabadas_lines:
            for line in percepciones_grabadas_lines:
                parte_exenta = 0
                parte_gravada = 0
                #_logger.info('codigo %s monto %s', line.salary_rule_id.code, line.total)
                if not line.salary_rule_id.tipo_cpercepcion.clave:
                    raise UserError(_('La regla salarial %s no tiene clave del SAT configurado.') % (line.salary_rule_id.name))

                if line.salary_rule_id.exencion:
                    percepciones_excentas_lines += 1
                    #_logger.info('codigo %s', line.salary_rule_id.parte_gravada.code)
                    concepto_gravado = self.env['hr.payslip.line'].search([('code','=',line.salary_rule_id.parte_gravada.code),('slip_id','=',self.id)], limit=1)
                    if concepto_gravado:
                        parte_gravada = concepto_gravado.total
                        _logger.info('total gravado %s', concepto_gravado.total)
                    
                    #_logger.info('codigo %s', line.salary_rule_id.parte_exenta.code)
                    concepto_exento = self.env['hr.payslip.line'].search([('code','=',line.salary_rule_id.parte_exenta.code),('slip_id','=',self.id)], limit=1)
                    if concepto_exento:
                        parte_exenta = concepto_exento.total
                        _logger.info('total gravado %s', concepto_exento.total)
                    
                    # horas extras
                    if line.salary_rule_id.tipo_cpercepcion.clave == '019':
                        percepciones_horas_extras = self.env['hr.payslip.worked_days'].search([('payslip_id','=',self.id)])
                        if percepciones_horas_extras:
                            #_logger.info('si hay ..')
                            for ext_line in percepciones_horas_extras:
                                #_logger.info('codigo %s.....%s ', line.code, ext_line.code)
                                if line.code == ext_line.code:
                                    if line.code == 'HEX1':
                                        tipo_hr = '03'
                                    elif line.code == 'HEX2':
                                        tipo_hr = '01'
                                    elif line.code == 'HEX3':
                                        tipo_hr = '02'
                                    lineas_de_percepcion_exentas.append({'TipoPercepcion': line.salary_rule_id.tipo_cpercepcion.clave,
                                       'Clave': line.code,
                                       'Concepto': line.salary_rule_id.name[:100],
                                       'ImporteGravado': parte_gravada,
                                       'ImporteExento': parte_exenta,
                                       'Dias': ext_line.number_of_days,
                                       'TipoHoras': tipo_hr,
                                       'HorasExtra': ext_line.number_of_hours,
                                       'ImportePagado': line.total})
                    
                    # Ingresos en acciones o títulos valor que representan bienes
                    elif line.salary_rule_id.tipo_cpercepcion.clave == '045':
                        lineas_de_percepcion_exentas.append({'TipoPercepcion': line.salary_rule_id.tipo_cpercepcion.clave,
                           'Clave': line.code,
                           'Concepto': line.salary_rule_id.name[:100],
                           'ValorMercado': 56,
                           'PrecioAlOtorgarse': 48,
                           'ImporteGravado': parte_gravada,
                           'ImporteExento': parte_exenta})
                    else:
                        lineas_de_percepcion_exentas.append({'TipoPercepcion': line.salary_rule_id.tipo_cpercepcion.clave,
                           'Clave': line.code,
                           'Concepto': line.salary_rule_id.name[:100],
                           'ImporteGravado': parte_gravada,
                           'ImporteExento': parte_exenta})
                else:
                    parte_gravada = line.total
                    lineas_de_percepcion.append({'TipoPercepcion': line.salary_rule_id.tipo_cpercepcion.clave,
                    'Clave': line.code,
                    'Concepto': line.salary_rule_id.name[:100],
                    'ImporteGravado': line.total,
                    'ImporteExento': '0'})

                #if line.salary_rule_id.tipo_cpercepcion.clave != '022' and line.salary_rule_id.tipo_cpercepcion.clave != '023' and line.salary_rule_id.tipo_cpercepcion.clave != '025' and line.salary_rule_id.tipo_cpercepcion.clave !='039' and line.salary_rule_id.tipo_cpercepcion.clave !='044':
                payslip_total_PERE += round(parte_exenta,2)
                payslip_total_PERG += round(parte_gravada,2)
                if line.salary_rule_id.tipo_cpercepcion.clave == '022' or line.salary_rule_id.tipo_cpercepcion.clave == '023' or line.salary_rule_id.tipo_cpercepcion.clave == '025':
                    payslip_total_SEIN += round(line.total,2)
                if line.salary_rule_id.tipo_cpercepcion.clave =='039' or line.salary_rule_id.tipo_cpercepcion.clave =='044':
                    payslip_total_JPRE += round(line.total,2)

        percepcion = {
               'Totalpercepcion': {
                        'TotalSeparacionIndemnizacion': payslip_total_SEIN,
                        'TotalJubilacionPensionRetiro': payslip_total_JPRE,
                        'TotalGravado': payslip_total_PERG,
                        'TotalExento': payslip_total_PERE,
                        'TotalSueldos': payslip_total_PERG + payslip_total_PERE - payslip_total_SEIN - payslip_total_JPRE,
               },
        }

        #************ SEPARACION / INDEMNIZACION   ************#
        if payslip_total_SEIN > 0:
            if payslip_total_PERG > self.contract_id.wage:
                ingreso_acumulable = self.contract_id.wage
            else:
                ingreso_acumulable = payslip_total_PERG
            if payslip_total_PERG - self.contract_id.wage < 0:
                ingreso_no_acumulable = 0
            else:
                ingreso_no_acumulable = payslip_total_PERG - self.contract_id.wage

            percepcion.update({
               'separacion': [{
                        'TotalPagado': payslip_total_SEIN,
                        'NumAñosServicio': self.contract_id.antiguedad_anos,
                        'UltimoSueldoMensOrd': self.contract_id.wage,
                        'IngresoAcumulable': ingreso_acumulable,
                        'IngresoNoAcumulable': ingreso_no_acumulable,
                }]
            })

            #percepcion.update({'SeparacionIndemnizacion': separacion})
        percepcion.update({'lineas_de_percepcion_grabadas': lineas_de_percepcion, 'no_per_grabadas': len(percepciones_grabadas_lines)-percepciones_excentas_lines})
        percepcion.update({'lineas_de_percepcion_excentas': lineas_de_percepcion_exentas, 'no_per_excentas': percepciones_excentas_lines})
        request_params = {'percepciones': percepcion}

#****** OTROS PAGOS ******
        otrospagos_lines = self.env['hr.payslip.line'].search([('category_id.code','=','ALW3'),('slip_id','=',self.id)])
        #tipo_otro_pago_dict = dict(self.env['hr.salary.rule']._fields.get('tipo_otro_pago').selection)
        auxiliar_lines = self.env['hr.payslip.line'].search([('category_id.code','=','AUX'),('slip_id','=',self.id)])
        #tipo_otro_pago_dict = dict(self.env['hr.salary.rule']._fields.get('tipo_otro_pago').selection)
        lineas_de_otros = []
        if otrospagos_lines:
            for line in otrospagos_lines:
                #_#logger.info('line total ...%s', line.total)
                if not line.salary_rule_id.tipo_cotro_pago.clave:
                    raise UserError(_('La regla salarial %s no tiene clave del SAT configurado.') % (line.salary_rule_id.name))

                if line.salary_rule_id.tipo_cotro_pago.clave == '002': # and line.total > 0:
                    #line2 = self.contract_id.env['tablas.subsidio.line'].search([('form_id','=',self.contract_id.tablas_cfdi_id.id),('lim_inf','<=',self.contract_id.wage)],order='lim_inf desc',limit=1)
                    self.subsidio_periodo = 0
                    #_logger.info('entro a este ..')
                    payslip_total_TOP += line.total
                    #if line2:
                    #    self.subsidio_periodo = (line2.s_mensual/self.imss_mes)*self.imss_dias
                    for aux in auxiliar_lines:
                        if aux.code == 'SUB':
                            self.subsidio_periodo = aux.total
                            if self.subsidio_periodo > 407.02:
                               self.subsidio_periodo = 407.02
                    #_logger.info('subsidio aplicado %s importe excento %s', self.subsidio_periodo, line.total)
                    lineas_de_otros.append({'TipoOtrosPagos': line.salary_rule_id.tipo_cotro_pago.clave,
                    'Clave': line.code,
                    'Concepto': line.salary_rule_id.name[:100],
                    'ImporteGravado': '0',
                    'ImporteExento': line.total,
                    'SubsidioCausado': self.subsidio_periodo})
                else:
                    payslip_total_TOP += line.total
                    #_logger.info('entro al otro ..')
                    lineas_de_otros.append({'TipoOtrosPagos': line.salary_rule_id.tipo_cotro_pago.clave,
                        'Clave': line.code,
                        'Concepto': line.salary_rule_id.name[:100],
                        'ImporteGravado': '0',
                        'ImporteExento': line.total})
        otrospagos = {
            'otrospagos': {
                    'Totalotrospagos': payslip_total_TOP,
            },
        }
        otrospagos.update({'otros_pagos': lineas_de_otros, 'no_otros_pagos': len(otrospagos_lines)})
        request_params.update({'otros_pagos': otrospagos})

#********** DEDUCCIONES *********
        total_imp_ret = 0
        suma_deducciones = 0
        self.importe_isr = 0
        self.isr_periodo = 0
        no_deuducciones = 0
        deducciones_lines = self.env['hr.payslip.line'].search([('category_id.code','=','DED'),('slip_id','=',self.id)])
        lineas_deduccion = []
        if deducciones_lines:
            #todas las deducciones excepto imss e isr
            for line in deducciones_lines:
                if not line.salary_rule_id.tipo_cdeduccion.clave:
                    raise UserError(_('La regla salarial %s no tiene clave del SAT configurado.') % (line.salary_rule_id.name))

                if line.salary_rule_id.tipo_cdeduccion.clave != '001' and line.salary_rule_id.tipo_cdeduccion.clave != '002':
                    #_logger.info('linea  ...')
                    no_deuducciones += 1
                    lineas_deduccion.append({'TipoDeduccion': line.salary_rule_id.tipo_cdeduccion.clave,
                   'Clave': line.code,
                   'Concepto': line.salary_rule_id.name[:100],
                   'Importe': round(line.total,2)})
                    payslip_total_TDED += round(line.total,2)

            #todas las deducciones imss
            self.importe_imss = 0
            for line in deducciones_lines:
                if line.salary_rule_id.tipo_cdeduccion.clave == '001':
                    #_logger.info('linea imss ...')
                    self.importe_imss += round(line.total,2)

            if self.importe_imss > 0:
                no_deuducciones += 1
                self.calculo_imss()
                lineas_deduccion.append({'TipoDeduccion': '001',
                  'Clave': '302',
                  'Concepto': 'Seguridad social',
                  'Importe': round(self.importe_imss,2)})
                payslip_total_TDED += round(self.importe_imss,2)

            #todas las deducciones isr
            for line in deducciones_lines:
                if line.salary_rule_id.tipo_cdeduccion.clave == '002' and line.salary_rule_id.code == 'ISR':
                    self.isr_periodo = line.total 
                if line.salary_rule_id.tipo_cdeduccion.clave == '002':
                    #_logger.info('linea ISR ...')
                    self.importe_isr += round(line.total,2)

            if self.importe_isr > 0:
                no_deuducciones += 1
                lineas_deduccion.append({'TipoDeduccion': '002',
                  'Clave': '301',
                  'Concepto': 'ISR',
                  'Importe': round(self.importe_isr,2)})
                payslip_total_TDED += round(self.importe_isr,2)
            total_imp_ret = round(self.importe_isr,2)

        deduccion = {
            'TotalDeduccion': {
                    'TotalOtrasDeducciones': round(payslip_total_TDED - total_imp_ret,2),
                    'TotalImpuestosRetenidos': total_imp_ret,
            },
        }
        deduccion.update({'lineas_de_deduccion': lineas_deduccion, 'no_deuducciones': no_deuducciones})
        request_params.update({'deducciones': deduccion})

        #************ INCAPACIDADES  ************#
        incapacidades = self.env['hr.payslip.worked_days'].search([('payslip_id','=',self.id)])
        if incapacidades:
            for ext_line in incapacidades:
                if ext_line.code == 'INC_RT' or ext_line.code == 'INC_EG' or ext_line.code == 'INC_MAT':
                    #_logger.info('codigo %s.... ', ext_line.code)
                    tipo_inc = ''
                    if ext_line.code == 'INC_RT':
                        tipo_inc = '01'
                    elif ext_line.code == 'INC_EG':
                        tipo_inc = '02'
                    elif ext_line.code == 'INC_MAT':
                        tipo_inc = '03'

                    importe_monetario = 0
                    sub_incapacidad = self.env['hr.payslip.line'].search([('category_id.code','=','ALW'),('slip_id','=',self.id)])
                    if sub_incapacidad:
                       for sub_line in sub_incapacidad:
                          if sub_line.salary_rule_id.tipo_cpercepcion.clave == '014':
                              importe_monetario += sub_line.total
                    desc_incapacidad = self.env['hr.payslip.line'].search([('category_id.code','=','DED'),('slip_id','=',self.id)])
                    if desc_incapacidad:
                       for desc_line in desc_incapacidad:
                          if desc_line.salary_rule_id.tipo_cdeduccion.clave == '006':
                              importe_monetario += desc_line.total
                    incapacidad = {
                         'Incapacidad': {
                             'DiasIncapacidad': ext_line.number_of_days,
                             'TipoIncapacidad': tipo_inc,
                             'ImporteMonetario': importe_monetario,
                         },
                    }
                    request_params.update({'incapacidades': incapacidad})

        self.retencion_subsidio_pagado = self.isr_periodo - self.subsidio_periodo
        self.total_nomina = payslip_total_PERG + payslip_total_PERE + payslip_total_TOP - payslip_total_TDED
        self.subtotal =  payslip_total_PERG + payslip_total_PERE + payslip_total_TOP
        self.descuento = payslip_total_TDED

        work_days = 0
        lineas_trabajo = self.env['hr.payslip.worked_days'].search([('payslip_id','=',self.id)])
        for dias_pagados in lineas_trabajo:
            if dias_pagados.code == 'WORK100':
                work_days += dias_pagados.number_of_days
            if dias_pagados.code == 'FJC':
                work_days += dias_pagados.number_of_days
            if dias_pagados.code == 'SEPT':
                work_days += dias_pagados.number_of_days

        if self.tipo_nomina == 'O':
            self.periodicidad = self.contract_id.periodicidad_pago
        else:
            self.periodicidad = '99'
        diaspagados = 0
        if self.struct_id.name == 'Reparto de utilidades':
            diaspagados = 1
        else:
            diaspagados = work_days
        regimen = 0
        contrato = 0
        if self.struct_id.name == 'Liquidación - indemnizacion/finiquito':
            regimen = '13'
            contrato = '99'
        else:
            regimen = self.employee_id.regimen
            contrato = self.employee_id.contrato

        #************ JUBILACION / PENSION / RETIRO   ************#
        if payslip_total_JPRE > 0:
            if payslip_total_PERG > self.contract_id.wage:
                ingreso_acumulable_jpre = self.contract_id.wage
            else:
                ingreso_acumulable_jpre = payslip_total_PERG
            if payslip_total_PERG - self.contract_id.wage < 0:
                ingreso_no_acumulable_jpre = 0
            else:
                ingreso_no_acumulable_jpre = payslip_total_PERG - self.contract_id.wage

            percepcion.update({
               'jubilacion': [{
                        'TotalParcialidad': payslip_total_JPRE,
                        'MontoDiario': payslip_total_JPRE / diaspagados,
                        'IngresoAcumulable': ingreso_acumulable_jpre,
                        'IngresoNoAcumulable': ingreso_no_acumulable_jpre,
                }]
                        #'TotalUnaExhibicion'
            })

        #corregir hora
        timezone = self._context.get('tz')
        if not timezone:
            timezone = self.env.user.partner_id.tz or 'UTC'
        #timezone = tools.ustr(timezone).encode('utf-8')

        local = pytz.timezone(timezone)
        if not self.fecha_factura:
            naive_from = datetime.datetime.now()
        else:
            naive_from = self.fecha_factura
        local_dt_from = naive_from.replace(tzinfo=pytz.UTC).astimezone(local)
        date_from = local_dt_from.strftime("%Y-%m-%d %H:%M:%S")
        if not self.fecha_factura:
            self.fecha_factura = datetime.datetime.now()

        request_params.update({
                'factura': {
                      'serie': self.company_id.serie_nomina,
                      'folio': self.number_folio,
                      'metodo_pago': self.methodo_pago,
                   #   'forma_pago': self.forma_pago,
                      'tipocomprobante': self.tipo_comprobante,
                      'moneda': 'MXN',
                      'tipodecambio': '1.0000',
                      'fecha_factura': date_from,
                      'LugarExpedicion': self.company_id.zip,
                      'RegimenFiscal': self.company_id.regimen_fiscal_id.code,
                      'subtotal': self.subtotal,
                      'descuento': self.descuento,
                      'total': self.total_nomina,
                      'Exportacion': '01',
                },
                'emisor': {
                      'rfc': self.company_id.vat,
                      'curp': self.company_id.curp,
                      'api_key': self.company_id.proveedor_timbrado,
                      'modo_prueba': self.company_id.modo_prueba,
                      'nombre_fiscal': self.company_id.nombre_fiscal.upper(),
                },
                'receptor': {
                      'rfc': self.employee_id.rfc,
                      'nombre': self.employee_id.name.upper(),
                      'uso_cfdi': self.uso_cfdi,
                      'RegimenFiscalReceptor': '605',
                      'DomicilioFiscalReceptor': self.employee_id.domicilio_receptor,
                },
                'conceptos': {
                      'cantidad': '1.0',
                      'ClaveUnidad': 'ACT',
                      'ClaveProdServ': '84111505',
                      'descripcion': 'Pago de nómina',
                      'valorunitario': self.subtotal,
                      'importe':  self.subtotal,
                      'descuento': self.descuento,
                      'ObjetoImp': '01',
                },
                'nomina12': {
                      'TipoNomina': self.tipo_nomina,
                      'FechaPago': self.fecha_pago and self.fecha_pago.strftime(DF),
                      'FechaInicialPago': self.date_from and self.date_from.strftime(DF),
                      'FechaFinalPago': self.date_to and self.date_to.strftime(DF),
                      'NumDiasPagados': diaspagados,
                      'TotalPercepciones': payslip_total_PERG + payslip_total_PERE,
                      'TotalDeducciones': self.descuento,
                      'TotalOtrosPagos': payslip_total_TOP,
                },
                'nomina12Emisor': {
                      'RegistroPatronal': self.employee_id.registro_patronal_id.registro_patronal,
                      'RfcPatronOrigen': self.company_id.vat,
                },
                'nomina12Receptor': {
                      'ClaveEntFed': self.employee_id.estado.code,
                      'Curp': self.employee_id.curp,
                      'NumEmpleado': self.employee_id.no_empleado,
                      'PeriodicidadPago': self.periodicidad, #self.contract_id.periodicidad_pago,
                      'TipoContrato': contrato,
                      'TipoRegimen': regimen,
                      'TipoJornada': self.employee_id.jornada,
                      'Antiguedad': 'P' + str(antiguedad) + 'W',
                      'Banco': self.employee_id.banco.c_banco,
                      'CuentaBancaria': self.employee_id.no_cuenta,
                      'FechaInicioRelLaboral': self.contract_id.date_start and self.contract_id.date_start.strftime(DF),
                      'NumSeguridadSocial': self.employee_id.segurosocial,
                      'Puesto': self.employee_id.job_id.name,
                      'Departamento': self.employee_id.department_id.name,
                      'Sindicalizado': 'Sí' if self.employee_id.sindicalizado else 'No',
                      'RiesgoPuesto': self.contract_id.riesgo_puesto,
                      'SalarioBaseCotApor': self.contract_id.sueldo_base_cotizacion,
                      'SalarioDiarioIntegrado': self.contract_id.sueldo_diario_integrado,
                },
                'adicional': {
                      'tipo_relacion': self.tipo_relacion,
                      'uuid_relacionado': self.uuid_relacionado,
                },
                'informacion': {
                      'cfdi': '4.0',
                      'sistema': 'odoo16',
                      'version': '1',
                      'api_key': self.company_id.proveedor_timbrado,
                      'modo_prueba': self.company_id.modo_prueba,
                },
		})

#****** CERTIFICADOS *******
        if not self.company_id.archivo_cer:
            raise UserError(_('Archivo .cer path is missing.'))
        if not self.company_id.archivo_key:
            raise UserError(_('Archivo .key path is missing.'))
        archivo_cer = self.company_id.archivo_cer
        archivo_key = self.company_id.archivo_key
        request_params.update({
                'certificados': {
                      'archivo_cer': archivo_cer.decode("utf-8"),
                      'archivo_key': archivo_key.decode("utf-8"),
                      'contrasena': self.company_id.contrasena,
                }})
        return request_params

    def action_cfdi_nomina_generate(self):
        for payslip in self:
            if payslip.folio_fiscal:
                payslip.write({'nomina_cfdi': True, 'estado_factura': 'factura_correcta'})
                return True
            #if payslip.fecha_factura == False:
            #    payslip.fecha_factura= datetime.datetime.now()
            #    payslip.write({'fecha_factura': payslip.fecha_factura})
            if payslip.estado_factura == 'factura_correcta':
                raise UserError(_('Error para timbrar factura, Factura ya generada.'))
            if payslip.estado_factura == 'factura_cancelada':
                raise UserError(_('Error para timbrar factura, Factura ya generada y cancelada.'))

            values = payslip.to_json()
            #  print json.dumps(values, indent=4, sort_keys=True)
            if payslip.company_id.proveedor_timbrado == 'multifactura':
                url = '%s' % ('http://facturacion.itadmin.com.mx/api/nomina')
            elif payslip.company_id.proveedor_timbrado == 'multifactura2':
                url = '%s' % ('http://facturacion2.itadmin.com.mx/api/nomina')
            elif payslip.company_id.proveedor_timbrado == 'multifactura3':
                url = '%s' % ('http://facturacion3.itadmin.com.mx/api/nomina')
            elif payslip.company_id.proveedor_timbrado == 'gecoerp':
                if payslip.company_id.modo_prueba:
                    url = '%s' % ('https://ws.gecoerp.com/itadmin/pruebas/nomina/?handler=OdooHandler33')
                else:
                    url = '%s' % ('https://itadmin.gecoerp.com/nomina/?handler=OdooHandler33')
            else:
                raise UserError(_('Error, falta seleccionar el servidor de timbrado en la configuración de la compañía.'))

            try:
                response = requests.post(url , 
                                     auth=None,verify=False, data=json.dumps(values), 
                                     headers={"Content-type": "application/json"})
            except Exception as e:
                error = str(e)
                if "Name or service not known" in error or "Failed to establish a new connection" in error:
                    raise UserError("Servidor fuera de servicio, favor de intentar mas tarde")
                else:
                   raise UserError(error)

            if "Whoops, looks like something went wrong." in response.text:
                raise UserError("Error en el proceso de timbrado, espere un minuto y vuelva a intentar timbrar nuevamente. \nSi el error aparece varias veces reportarlo con la persona de sistemas.")

#            _logger.info('something ... %s', response.text)
            json_response = response.json()
            xml_file_link = False
            estado_factura = json_response['estado_factura']
            if estado_factura == 'problemas_factura':
                raise UserError(_(json_response['problemas_message']))
            # Receive and stroe XML 
            if json_response.get('factura_xml'):
                payslip._set_data_from_xml(base64.b64decode(json_response['factura_xml']))
                    
                xml_file_name = payslip.number.replace('/','_') + '.xml'
                payslip.env['ir.attachment'].sudo().create(
                                            {
                                                'name': xml_file_name,
                                                'datas': json_response['factura_xml'],
                                                #'datas_fname': xml_file_name,
                                                'res_model': payslip._name,
                                                'res_id': payslip.id,
                                                'type': 'binary'
                                            })	
            #    report = payslip.env['ir.actions.report']._get_report_from_name('nomina_cfdi.report_payslip')
            #    report_data = report._render_qweb_pdf([payslip.id])[0]
            #    pdf_file_name = payslip.number.replace('/','_') + '.pdf'
            #    payslip.env['ir.attachment'].sudo().create(
            #                                {
            #                                    'name': pdf_file_name,
            #                                    'datas': base64.b64encode(report_data),
                                                #'datas_fname': pdf_file_name,
            #                                    'res_model': payslip._name,
            #                                    'res_id': payslip.id,
            #                                    'type': 'binary'
            #                                })

            payslip.write({'estado_factura': estado_factura,
                    'nomina_cfdi': True})

    def _set_data_from_xml(self, xml_invoice):
        if not xml_invoice:
            return None
        NSMAP = {
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'cfdi': 'http://www.sat.gob.mx/cfd/4',
            'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital',
        }

        xml_data = etree.fromstring(xml_invoice)
        Complemento = xml_data.find('cfdi:Complemento', NSMAP)
        TimbreFiscalDigital = Complemento.find('tfd:TimbreFiscalDigital', NSMAP)

        self.tipocambio = xml_data.find('TipoCambio') and xml_data.attrib['TipoCambio'] or '1'
        self.moneda = xml_data.attrib['Moneda']
        self.numero_cetificado = xml_data.attrib['NoCertificado']
        self.cetificaso_sat = TimbreFiscalDigital.attrib['NoCertificadoSAT']
        self.fecha_certificacion = TimbreFiscalDigital.attrib['FechaTimbrado']
        self.selo_digital_cdfi = TimbreFiscalDigital.attrib['SelloCFD']
        self.selo_sat = TimbreFiscalDigital.attrib['SelloSAT']
        self.folio_fiscal = TimbreFiscalDigital.attrib['UUID']
     #   if self.number:
     #       self.folio = xml_data.attrib['Folio']
     #   if self.company_id.serie_nomina:
     #       self.serie_emisor = xml_data.attrib['Serie']
        self.invoice_datetime = xml_data.attrib['Fecha']
        version = TimbreFiscalDigital.attrib['Version']
        self.cadena_origenal = '||%s|%s|%s|%s|%s||' % (version, self.folio_fiscal, self.fecha_certificacion,
                                                       self.selo_digital_cdfi, self.cetificaso_sat)

        options = {'width': 275 * mm, 'height': 275 * mm}
        amount_str = str(self.total_nomina).split('.')
        qr_value = 'https://verificacfdi.facturaelectronica.sat.gob.mx/default.aspx?&id=%s&re=%s&rr=%s&tt=%s.%s&fe=%s' % (
            self.folio_fiscal,
            self.company_id.vat,
            self.employee_id.rfc,
            amount_str[0].zfill(10),
            amount_str[1].ljust(6, '0')[:6],
            self.selo_digital_cdfi[-8:],
        )
        self.qr_value = qr_value
        ret_val = createBarcodeDrawing('QR', value=qr_value, **options)
        self.qrcode_image = base64.encodebytes(ret_val.asString('jpg'))

    def action_cfdi_cancel(self):
        for payslip in self:
            if payslip.nomina_cfdi:
                if payslip.estado_factura == 'factura_cancelada':
                    pass
                    # raise UserError(_('La factura ya fue cancelada, no puede volver a cancelarse.'))
                if not payslip.company_id.archivo_cer:
                    raise UserError(_('Falta la ruta del archivo .cer'))
                if not payslip.company_id.archivo_key:
                    raise UserError(_('Falta la ruta del archivo .key'))
                archivo_cer = payslip.company_id.archivo_cer
                archivo_key = payslip.company_id.archivo_key
                domain = [
                     ('res_id', '=', payslip.id),
                     ('res_model', '=', payslip._name),
                     ('name', '=', payslip.number.replace('/','_') + '.xml')]
                xml_file = payslip.env['ir.attachment'].search(domain)[0]
                if not xml_file:
                    raise UserError(_('No se encontró el archivo XML para enviar a cancelar.'))
                values = {
                          'rfc': payslip.company_id.vat,
                          'api_key': payslip.company_id.proveedor_timbrado,
                          'uuid': payslip.folio_fiscal,
                          'folio': payslip.folio,
                          'serie_factura': payslip.company_id.serie_nomina,
                          'modo_prueba': payslip.company_id.modo_prueba,
                            'certificados': {
                                  'archivo_cer': archivo_cer.decode("utf-8"),
                                  'archivo_key': archivo_key.decode("utf-8"),
                                  'contrasena': payslip.company_id.contrasena,
                            },
                          'xml': xml_file.datas.decode("utf-8"),
                          'motivo': payslip.env.context.get('motivo_cancelacion','02'),
                          'foliosustitucion': payslip.env.context.get('foliosustitucion',''),
                          }
                if payslip.company_id.proveedor_timbrado == 'multifactura':
                    url = '%s' % ('http://facturacion.itadmin.com.mx/api/refund')
                elif payslip.company_id.proveedor_timbrado == 'multifactura2':
                    url = '%s' % ('http://facturacion2.itadmin.com.mx/api/refund')
                elif payslip.company_id.proveedor_timbrado == 'multifactura3':
                    url = '%s' % ('http://facturacion3.itadmin.com.mx/api/refund')
                elif payslip.company_id.proveedor_timbrado == 'gecoerp':
                    if payslip.company_id.modo_prueba:
                        url = '%s' % ('https://ws.gecoerp.com/itadmin/pruebas/refund/?handler=OdooHandler33')
                    else:
                        url = '%s' % ('https://itadmin.gecoerp.com/refund/?handler=OdooHandler33')
                else:
                    raise UserError(_('Error, falta seleccionar el servidor de timbrado en la configuración de la compañía.'))

                try:
                    response = requests.post(url , 
                                         auth=None,verify=False, data=json.dumps(values), 
                                         headers={"Content-type": "application/json"})
                except Exception as e:
                    error = str(e)
                    if "Name or service not known" in error or "Failed to establish a new connection" in error:
                        raise UserError("Servidor fuera de servicio, favor de intentar mas tarde")
                    else:
                       raise UserError(error)

                if "Whoops, looks like something went wrong." in response.text:
                    raise UserError("Error en el proceso de timbrado, espere un minuto y vuelva a intentar timbrar nuevamente. \nSi el error aparece varias veces reportarlo con la persona de sistemas.")

                json_response = response.json()
                #_logger.info('log de la exception ... %s', response.text)

                if json_response['estado_factura'] == 'problemas_factura':
                    raise UserError(_(json_response['problemas_message']))
                elif json_response.get('factura_xml', False):
                    if payslip.number:
                        file_name = 'CANCEL_' + payslip.number.replace('/','_') + '.xml'
                    else:
                        raise UserError(_('La nómina no tiene nombre'))
                    payslip.env['ir.attachment'].sudo().create(
                                                {
                                                    'name': file_name,
                                                    'datas': json_response['factura_xml'],
                                                    'store_fname': file_name,
                                                    'res_model': payslip._name,
                                                    'res_id': payslip.id,
                                                    'type': 'binary'
                                                })
                payslip.write({'estado_factura': json_response['estado_factura']})

    def send_nomina(self):
        self.ensure_one()
        template = self.env.ref('nomina_cfdi.email_template_payroll', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
            
        ctx = dict()
        ctx.update({
            'default_model': 'hr.payslip',
            'default_res_id': self.id,
            'default_use_template': bool(template),
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
        })
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

    def action_payslip_done(self):
        res = super(HrPayslip,self).action_payslip_done()
        for rec in self:
            rec._get_fondo_ahorro()
        return res

    def compute_sheet(self):
        for invoice in self:
            invoice._validate_slip_fields()
            invoice._get_acumulados_mensual()
            invoice._get_acumulados_anual()
            invoice._get_acumulado_prima_vac()

        res = super(HrPayslip, self).compute_sheet()
        for rec in self:
            rec.calculo_imss()
            rec.total_nom = rec.get_amount_from_rule_code('NET')
            #calculo de especie
            total = 0
            #_logger.info('monto especie')
            for line in rec.line_ids:
                #_logger.info('codigo %s monto %s', line.code, line.total)
                if line.salary_rule_id.forma_pago == '002':
                   #_logger.info('entro codigo %s monto %s', line.code, line.total)
                   total += line.total
            #_logger.info('total especie %s', total)
            lines = []
            for line in rec.line_ids:
                if line.code == 'EFECT':
                   #_logger.info('codigo %s monto %s', line.code, line.total)
                   line.update({'total': line.total - total, 'amount': line.total - total})
                   line.refresh()
            rec.refresh()
            #quitar prestamos cuando nomina en cero
            if rec.total_nom <= 0 and rec.aplicar_descuentos:
               rec.aplicar_descuentos = False
        return res

    @api.model
    def calculo_imss(self):
        #cuota del IMSS parte del Empleado
        dias_laborados = 0
        dias_completos = 0
        dias_falta = 0
        dias_trabajo = 0

        dias_completos = self.imss_dias
        dias_laborados =  dias_completos
        dias_falta =  dias_completos

        dias_registrados = self.env['hr.payslip.worked_days'].search([('payslip_id','=',self.id)])
        if dias_registrados:
            for dias in dias_registrados:
                if dias.code == 'FI' or dias.code == 'FJS':
                    dias_laborados = dias_laborados - dias.number_of_days
                    dias_falta = dias_falta - dias.number_of_days
                if dias.code == 'INC_MAT' or dias.code == 'INC_EG' or dias.code == 'INC_RT':
                    dias_laborados = dias_laborados - dias.number_of_days
                    dias_completos = dias_completos - dias.number_of_days
                if dias.code == 'WORK100' or dias.code == 'FJC' or dias.code == 'SEPT' or dias.code == 'VAC':
                    dias_trabajo = dias_trabajo + dias.number_of_days
        if dias_trabajo == 0:
            dias_laborados = 0
            dias_completos = 0

        #salario_cotizado = self.contract_id.sueldo_base_cotizacion
        base_calculo = 0
        base_execente = 0
        if self.contract_id.sueldo_base_cotizacion < 25 * self.contract_id.tablas_cfdi_id.uma:
            base_calculo = self.contract_id.sueldo_base_cotizacion
        else:
            base_calculo = 25 * self.contract_id.tablas_cfdi_id.uma

        if base_calculo > 3 * self.contract_id.tablas_cfdi_id.uma:
            base_execente = base_calculo - 3 * self.contract_id.tablas_cfdi_id.uma

        if self.employee_id.regimen == '02' or self.employee_id.regimen == '13':
            self.emp_exedente_smg = round(dias_completos * self.contract_id.tablas_cfdi_id.enf_mat_excedente_e/100 * base_execente,2)
            self.emp_prest_dinero = round(dias_completos * self.contract_id.tablas_cfdi_id.enf_mat_prestaciones_e/100 * base_calculo,2)
            self.emp_esp_pens = round(dias_completos * self.contract_id.tablas_cfdi_id.enf_mat_gastos_med_e/100 * base_calculo,2)
            self.emp_invalidez_vida = round(dias_laborados * self.contract_id.tablas_cfdi_id.inv_vida_e/100 * base_calculo,2)
            self.emp_cesantia_vejez = round(dias_laborados * self.contract_id.tablas_cfdi_id.cesantia_vejez_e/100 * base_calculo,2)
            self.emp_total = self.emp_exedente_smg + self.emp_prest_dinero + self.emp_esp_pens + self.emp_invalidez_vida + self.emp_cesantia_vejez
            
            #imss patronal
            factor_riesgo = 0
            if self.contract_id.riesgo_puesto == '1':
                factor_riesgo = self.contract_id.tablas_cfdi_id.rt_clase1
            elif self.contract_id.riesgo_puesto == '2':
                factor_riesgo = self.contract_id.tablas_cfdi_id.rt_clase2
            elif self.contract_id.riesgo_puesto == '3':
                factor_riesgo = self.contract_id.tablas_cfdi_id.rt_clase3
            elif self.contract_id.riesgo_puesto == '4':
                factor_riesgo = self.contract_id.tablas_cfdi_id.rt_clase4
            elif self.contract_id.riesgo_puesto == '5':
                factor_riesgo = self.contract_id.tablas_cfdi_id.rt_clase5

            tabla_cesantia = self.env['tablas.cesantia.line'].search([('form_id','=', self.contract_id.tablas_cfdi_id.id), 
                                                                      ('lim_inf','<=',self.contract_id.sueldo_base_cotizacion)],
                                                                      #('lim_sup','>=',self.contract_id.sueldo_base_cotizacion)],
                                                                       order='lim_inf desc',limit=1)
            if not tabla_cesantia:
                cesantia_vejez_p = self.contract_id.tablas_cfdi_id.cesantia_vejez_p
            else:
                cesantia_vejez_p = tabla_cesantia.cuota

            _logger.info('cesantia: %s', cesantia_vejez_p)

            self.pat_cuota_fija_pat = round(dias_completos * self.contract_id.tablas_cfdi_id.enf_mat_cuota_fija/100 * self.contract_id.tablas_cfdi_id.uma,2)
            self.pat_exedente_smg =round(dias_completos * self.contract_id.tablas_cfdi_id.enf_mat_excedente_p/100 * base_execente,2)
            self.pat_prest_dinero = round(dias_completos * self.contract_id.tablas_cfdi_id.enf_mat_prestaciones_p/100 * base_calculo,2)
            self.pat_esp_pens = round(dias_completos * self.contract_id.tablas_cfdi_id.enf_mat_gastos_med_p/100 * base_calculo,2)
            self.pat_riesgo_trabajo = round(dias_laborados * factor_riesgo/100 * base_calculo,2) # falta
            self.pat_invalidez_vida = round(dias_laborados * self.contract_id.tablas_cfdi_id.inv_vida_p/100 * base_calculo,2)
            self.pat_guarderias = round(dias_laborados * self.contract_id.tablas_cfdi_id.guarderia_p/100 * base_calculo,2)
            self.pat_retiro = round(dias_falta * self.contract_id.tablas_cfdi_id.retiro_p/100 * base_calculo,2)
            self.pat_cesantia_vejez = round(dias_laborados * cesantia_vejez_p/100 * base_calculo,2)
            self.pat_infonavit = round(dias_falta * self.contract_id.tablas_cfdi_id.apotacion_infonavit/100 * base_calculo,2)
            self.pat_total = self.pat_cuota_fija_pat + self.pat_exedente_smg + self.pat_prest_dinero + self.pat_esp_pens + self.pat_riesgo_trabajo + self.pat_invalidez_vida + self.pat_guarderias + self.pat_retiro + self.pat_cesantia_vejez + self.pat_infonavit
            if self.contract_id.sueldo_diario <= self.contract_id.tablas_cfdi_id.salario_minimo:
               self.pat_exedente_smg += self.emp_exedente_smg
               self.pat_prest_dinero += self.emp_prest_dinero
               self.pat_esp_pens += self.emp_esp_pens
               self.pat_invalidez_vida += self.emp_invalidez_vida
               self.pat_cesantia_vejez += self.emp_cesantia_vejez
               self.pat_total += self.emp_exedente_smg + self.emp_prest_dinero + self.emp_esp_pens + self.emp_invalidez_vida + self.emp_cesantia_vejez
               self.emp_exedente_smg = 0
               self.emp_prest_dinero = 0
               self.emp_esp_pens = 0
               self.emp_invalidez_vida = 0
               self.emp_cesantia_vejez = 0
               self.emp_total = 0
        else:
            #imss empleado
            self.emp_exedente_smg = 0
            self.emp_prest_dinero = 0
            self.emp_esp_pens = 0
            self.emp_invalidez_vida = 0
            self.emp_cesantia_vejez = 0
            self.emp_total = 0
            
            #imss patronal
            self.pat_cuota_fija_pat = 0
            self.pat_exedente_smg =0
            self.pat_prest_dinero = 0
            self.pat_esp_pens = 0
            self.pat_riesgo_trabajo = 0
            self.pat_invalidez_vida = 0
            self.pat_guarderias = 0
            self.pat_retiro = 0
            self.pat_cesantia_vejez = 0
            self.pat_infonavit = 0
            self.pat_total = 0

    def _get_cumpleanos(self):
        if self.employee_id.birthday:
          date_cumple = fields.Date.from_string(self.employee_id.birthday)
          if str(date_cumple.day) == '29' and str(date_cumple.month) == '2':
               date_cumple -=  datetime.timedelta(days=1)
          date_cumple = date_cumple.replace(self.date_to.year)
          d_from = fields.Date.from_string(self.date_from)
          #d_from = d_from.replace(date_cumple.year)
          d_to = fields.Date.from_string(self.date_to)
          #d_to = d_to.replace(date_cumple.year)
          if d_from <= date_cumple <= d_to:
              self.cumpleanos = True
          else:
              self.cumpleanos = False
        else:
          self.cumpleanos = False

class HrPayslipMail(models.Model):
    _name = "hr.payslip.mail"
    _inherit = ['mail.thread']
    _description = "Nomina Mail"

    payslip_id = fields.Many2one('hr.payslip', string='Nomina')
    name = fields.Char(related='payslip_id.name')
    employee_id = fields.Many2one(related='payslip_id.employee_id')
    company_id = fields.Many2one(related='payslip_id.company_id')
    
class MailTemplate(models.Model):
    "Templates for sending email"
    _inherit = 'mail.template'
    
    @api.model
    def _get_file(self, url):
        url = url.encode('utf8')
        filename, headers = urllib.urlretrieve(url)
        fn, file_extension = os.path.splitext(filename)
        return  filename, file_extension.replace('.', '')

    def generate_email(self, res_ids, fields=None):
        multi_mode = True
        if isinstance(res_ids, (int)):
            res_ids = [res_ids]
            multi_mode = False
        results = super(MailTemplate, self).generate_email(res_ids, fields=fields)

        template_id = self.env.ref('nomina_cfdi.email_template_payroll')
        for lang, (template, template_res_ids) in self._classify_per_lang(res_ids).items():
            if template.id  == template_id.id:
                for res_id in template_res_ids:
                    payment = self.env[template.model].browse(res_id)
                    if payment.estado_factura != 'factura_no_generada':
                        attachments =  results[res_id]['attachments'] or []
                        domain = [
                            ('res_id', '=', payment.id),
                            ('res_model', '=', payment._name),
                            ('name', '=', payment.number.replace('/','_') + '.xml')]
                        xml_file = self.env['ir.attachment'].search(domain)[0]
                        attachments.append((payment.number.replace('/','_') + '.xml', xml_file.datas))
                        results[res_id]['attachments'] = attachments
        return multi_mode and results or results[res_ids[0]]
