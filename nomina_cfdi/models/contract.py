# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
#import datetime
from datetime import datetime, timedelta
import logging
_logger = logging.getLogger(__name__)

class Contract(models.Model):
    _inherit = "hr.contract"
    
    periodicidad_pago = fields.Selection(
        selection=[('01', 'Diario'), 
                   ('02', 'Semanal'), 
                   ('03', 'Catorcenal'),
                   ('04', 'Quincenal'), 
                   ('05', 'Mensual'),
                   ('06', 'Bimensual'), 
                   ('07', 'Unidad obra'),
                   ('08', 'Comisión'), 
                   ('09', 'Precio alzado'), 
                   ('10', 'Pago por consignación'), 
                   ('99', 'Otra periodicidad'),],
        string=_('Periodicidad de pago CFDI'),
    )

    riesgo_puesto = fields.Selection(
        selection=[('1', 'Clase I'), 
                   ('2', 'Clase II'), 
                   ('3', 'Clase III'),
                   ('4', 'Clase IV'), 
                   ('5', 'Clase V'), 
                   ('99', 'No aplica'),],
        string=_('Riesgo del puesto'),
    )	
    sueldo_diario = fields.Float('Sueldo diario')
    sueldo_hora = fields.Float('Sueldo por hora')
    sueldo_diario_integrado = fields.Float('Sueldo diario integrado')
    sueldo_base_cotizacion = fields.Float('Sueldo base cotización (IMSS)')
    tablas_cfdi_id = fields.Many2one('tablas.cfdi','Tabla CFDI')

    bono_productividad = fields.Boolean('Bono productividad')
    bono_productividad_amount = fields.Float('Monto bono productividad')
    bono_asistencia = fields.Boolean('Bono asistencia')
    bono_asistencia_amount = fields.Float('Monto bono asistencia')
    bono_puntualidad = fields.Boolean('Bono puntualidad')
    bono_puntualidad_amount = fields.Float('Monto bono puntualidad')
    fondo_ahorro  = fields.Boolean('Fondo de ahorro')
    fondo_ahorro_amount  = fields.Float('Monto fondo de ahorro')
    vale_despensa  = fields.Boolean('Vale de despensa')
    vale_despensa_amount  = fields.Float('Monto vale de despensa')
    alimentacion  = fields.Boolean('Alimentación')
    alimentacion_amount  = fields.Float('Monto alimentación')
    percepcion_adicional  = fields.Boolean('Percepcion adicional')
    percepcion_adicional_amount  = fields.Float('Monto percepcion adicional')

    infonavit_fijo = fields.Float(string=_('Infonavit (fijo)'), digits = (12,4))
    infonavit_vsm = fields.Float(string=_('Infonavit (vsm)'), digits = (12,4))
    infonavit_porc = fields.Float(string=_('Infonavit (%)'), digits = (12,4))
    prestamo_fonacot = fields.Float('Prestamo FONACOT')
    pens_alim = fields.Float('Pensión alimenticia (%)')
    pens_alim_fijo = fields.Float('Pensión alimenticia (fijo)')
    caja_ahorro  = fields.Boolean('Caja de ahorro')
    caja_ahorro_amount  = fields.Float('Monto caja de ahorro')
    deduccion_adicional  = fields.Boolean('Deduccion adicional')
    deduccion_adicional_amount  = fields.Float('Monto deduccion adicional')

    antiguedad_anos = fields.Float('Años de antiguedad', compute='_compute_antiguedad_anos')

    tabla_vacaciones = fields.One2many('tablas.vacaciones.line', 'form_id') 
    tipo_pago = fields.Selection(
        selection=[('01', 'Por periodo'), 
                   ('02', 'Por día'),
                   ('03', 'Mes proporcional'),],
        string=_('Conteo de días'),
    )
    tipo_prima_vacacional = fields.Selection(
        selection=[('01', 'Al cumplir el año'), 
                   ('02', 'Con día de vacaciones'),
                   ('03', 'Al cumplir el año - 2da qna'),],
        string=_('Prima vacacional'),
        default = '02'
    )
    septimo_dia = fields.Boolean(string='Falta proporcional 7mo día')
    incapa_sept_dia = fields.Boolean(string='Incluir incapacidad en 7mo día')
    sept_dia = fields.Boolean(string='Séptimo día separado')
    semana_inglesa = fields.Boolean(string='Semana inglesa')
    prima_dominical = fields.Boolean(string='Prima dominical')
    calc_isr_extra = fields.Boolean(string='Incluir nóminas extraordinarias en calculo ISR mensual', default = False)

    @api.onchange('wage')
    def _compute_sueldo(self):
        if self.wage and self.tablas_cfdi_id:
            values = {
            'sueldo_diario': self.wage/self.tablas_cfdi_id.dias_mes,
            'sueldo_hora': self.wage/self.tablas_cfdi_id.dias_mes/8,
            'sueldo_diario_integrado': self.calculate_sueldo_diario_integrado(),
            'sueldo_base_cotizacion': self.calculate_sueldo_base_cotizacion(),
            }
            self.update(values)

    @api.depends('date_start')
    def _compute_antiguedad_anos(self):
        for contract in self:
           if contract.date_start:
               date_start = contract.date_start
               today = datetime.today().date()
               diff_date = today - date_start
               years = diff_date.days /365.0
               contract.antiguedad_anos = int(years)
           else:
               contract.antiguedad_anos = 0

    def antiguedad_to(self, contract_id, date_to):
        antiguedad = 0
        if contract_id.date_start: 
            date_start = contract_id.date_start
            diff_date = date_to - date_start 
            antiguedad = diff_date.days / 365.0
        return antiguedad

    @api.model
    def calcular_liquidacion(self):
        if self.date_end:
            diff_date = (self.date_end - self.date_start + timedelta(days=1)).days
            years = diff_date /365.0
            self.antiguedad_anos = int(years)
            self.dias_totales = self.antiguedad_anos * self.dias_x_ano + self.dias_base

    def button_dummy(self):
        self.calcular_liquidacion()
        return True

    @api.model
    def calculate_sueldo_base_cotizacion(self): 
        if self.date_start: 
            today = datetime.today().date()
            diff_date = (today - self.date_start + timedelta(days=1)).days
            years = diff_date /365.0
            #_logger.info('years ... %s', years)
            tablas_cfdi = self.tablas_cfdi_id 
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
            sdi = ((365 + tablas_cfdi_line.aguinaldo + (tablas_cfdi_line.vacaciones)* (tablas_cfdi_line.prima_vac/100) ) / 365 ) * self.wage/self.tablas_cfdi_id.dias_mes
            if sdi > max_sdi:
                sueldo_base_cotizacion = max_sdi
            else:
                sueldo_base_cotizacion = sdi
        else: 
            sueldo_base_cotizacion = 0
        return sueldo_base_cotizacion

    @api.model
    def calculate_sueldo_diario_integrado(self): 
        if self.date_start: 
            today = datetime.today().date()
            diff_date = (today - self.date_start + timedelta(days=1)).days
            years = diff_date /365.0
            #_logger.info('years ... %s', years)
            tablas_cfdi = self.tablas_cfdi_id 
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
            sdi = ((365 + tablas_cfdi_line.aguinaldo + (tablas_cfdi_line.vacaciones)* (tablas_cfdi_line.prima_vac/100.0) ) / 365.0 ) * self.wage/self.tablas_cfdi_id.dias_mes
            sueldo_diario_integrado = sdi
        else: 
            sueldo_diario_integrado = 0
        return sueldo_diario_integrado

    #FUNCTION TO CREATE INCIDENTIA DAR ALTA
    def action_dar_alta(self):
        for contract in self:
           vals = {
              'tipo_de_incidencia': 'Alta',
              'employee_id': contract.employee_id.id,
              'fecha': contract.date_start,
              'state': 'done',
           }
           contract.env['incidencias.nomina'].create(vals)


class TablasVacacioneslLine(models.Model):
    _name = 'tablas.vacaciones.line'
    _description = 'tablas vacaciones'

    form_id = fields.Many2one('hr.contract', string='Vacaciones', required=True)
    dias = fields.Integer('Dias disponibles')
    ano = fields.Selection(
        selection=[('2018', '2018'),
                   ('2019', '2019'),
                   ('2020', '2020'),
                   ('2021', '2021'),
                   ('2022', '2022'),
                   ('2023', '2023'),
                   ('2024', '2024'),
                   ],
        string=_('Año'), required=True)
    estado = fields.Selection(
        selection=[('activo', 'Activo'),
                   ('inactivo', 'Inactivo'),
                   ],
        string=_('Estatus'),)
    dias_consumido = fields.Integer('Dias consumidos')
    dias_otorgados = fields.Integer('Dias otorgados') 
    caducidad = fields.Date('Caducidad')
