# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class TablasAntiguedadesLine(models.Model):
    _name = 'tablas.antiguedades.line'
    _description = 'TablasAntiguedadesLine'

    form_id = fields.Many2one('tablas.cfdi', string='Vacaciones y aguinaldos', required=True)
    antiguedad = fields.Float('Antigüedad/Años') 
    vacaciones = fields.Float('Vacaciones/Días') 
    prima_vac = fields.Float('Prima vacacional (%)')
    aguinaldo = fields.Float('Aguinaldo/Días')

class TablasGeneralLine(models.Model):
    _name = 'tablas.general.line'
    _description = 'TablasGeneralLine'

    form_id = fields.Many2one('tablas.cfdi', string='ISR Mensual Art. 113 LISR', required=True)
    lim_inf = fields.Float('Límite inferior') 
    c_fija = fields.Float('Cuota fija') 
    s_excedente = fields.Float('Sobre excedente (%)')

class TablasSubsidiolLine(models.Model):
    _name = 'tablas.subsidio.line'
    _description = 'TablasSubsidiolLine'

    form_id = fields.Many2one('tablas.cfdi', string='Subem mensual/CAS Mensual', required=True)
    lim_inf = fields.Float('Límite inferior') 
    s_mensual = fields.Float('Subsidio mensual')

class TablasPeriodoISR(models.Model):
    _name = 'tablas.isr.periodo'
    _description = 'TablasGeneralLine'

    form_id = fields.Many2one('tablas.cfdi', string='ISR Semanal / Quincenal', required=True)
    lim_inf = fields.Float('Límite inferior') 
    c_fija = fields.Float('Cuota fija') 
    s_excedente = fields.Float('Sobre excedente (%)')

class TablasPeriodoBimestrallLine(models.Model):
    _name = 'tablas.periodo.bimestral'
    _description = 'TablasPeriodoBimestrallLine'

    form_id = fields.Many2one('tablas.cfdi', string='Periodo bimestral', required=True)
    dia_inicio = fields.Date('Primer día del periodo') 
    dia_fin = fields.Date('Ultímo día del periodo') 
    no_dias = fields.Float('Dias en el periodo', store=True)

    @api.onchange('dia_inicio', 'dia_fin')
    def compute_dias(self):
        if self.dia_fin and self.dia_inicio:
           delta = self.dia_fin - self.dia_inicio
           self.no_dias = delta.days + 1

class TablasPeriodoMensuallLine(models.Model):
    _name = 'tablas.periodo.mensual'
    _description = 'TablasPeriodoMensuallLine'

    form_id = fields.Many2one('tablas.cfdi', string='Periodo mensual', required=True)
    dia_inicio = fields.Date('Primer día del mes / periodo') 
    dia_fin = fields.Date('Ultímo día del mes / periodo') 
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
        string=_('Mes / Periodo'),)
    no_dias = fields.Float('Número de dias', store=True)

    @api.onchange('dia_inicio', 'dia_fin')
    def compute_dias(self):
        if self.dia_fin and self.dia_inicio:
           delta = self.dia_fin - self.dia_inicio
           self.no_dias = delta.days + 1

class TablasAnualISR(models.Model):
    _name = 'tablas.isr.anual'
    _description = 'TablasAnualISR'

    form_id = fields.Many2one('tablas.cfdi', string='ISR Anual', required=True)
    lim_inf = fields.Float('Límite inferior') 
    c_fija = fields.Float('Cuota fija') 
    s_excedente = fields.Float('Sobre excedente (%)')

class TablasCesantia(models.Model):
    _name = 'tablas.cesantia.line'
    _description = 'TablasCesantiaLine'

    form_id = fields.Many2one('tablas.cfdi', string='Cesantía', required=True)
    lim_inf = fields.Float('Límite inferior')
   # lim_sup = fields.Float('Límite superior')
    cuota = fields.Float('Cuota patronal (%)', digits = (12,3))

class TablasCFDI(models.Model):
    _name = 'tablas.cfdi'
    _description = 'TablasCFDI'

    name = fields.Char("Nombre")
    tabla_antiguedades = fields.One2many('tablas.antiguedades.line', 'form_id', copy=True) 
    tabla_LISR = fields.One2many('tablas.general.line', 'form_id', copy=True)
    tabla_ISR_anual = fields.One2many('tablas.isr.anual', 'form_id', copy=True)
    tabla_subem = fields.One2many('tablas.subsidio.line', 'form_id', copy=True)
    tabla_ISR_periodo = fields.One2many('tablas.isr.periodo', 'form_id', copy=True)
#    tabla_subsidio = fields.One2many('tablas.subsidio2.line', 'form_id', copy=True)
#    tabla_subsidio_acreditable = fields.One2many('tablas.subsidioacreditable.line', 'form_id', copy=True)
    tabla_bimestral = fields.One2many('tablas.periodo.bimestral', 'form_id', copy=True)
    tabla_mensual = fields.One2many('tablas.periodo.mensual', 'form_id', copy=True)
    #tabla_semanal = fields.One2many('tablas.periodo.semanal', 'form_id', copy=True)
    tabla_cesantia = fields.One2many('tablas.cesantia.line', 'form_id', copy=True)

    uma = fields.Float(string=_('UMA'), default='84.49')
    salario_minimo = fields.Float(string=_('Salario mínimo'))
    imss_mes = fields.Float('Periodo mensual subsidio (dias)',default='30.4', digits = (12,4))
    dias_mes = fields.Float('Periodo mensual sueldo (dias)',default='30', digits = (12,4))

    importe_utilidades = fields.Float(string=_('Importe a repartir a todos los empleados'), default=0)
    dias_min_trabajados = fields.Float(string=_('Dias mínimos trabajados en empleados eventuales'), default=60)
    funcion_ingresos = fields.Float(string=_('% a repartir en función de los ingresos'), default=50)
    funcion_dias = fields.Float(string=_('% a repartir en función de los días trabajados'), compute='_compute_funcion_dias', readonly=True)
    total_dias_trabajados = fields.Float(string=_('Total de días trabajados'), default=0)
    total_sueldo_percibido = fields.Float(string=_('Total de sueldo percibido'), default=0)
    factor_dias = fields.Float(string=_('Factor por dias trabajados'), compute='_factor_dias', readonly=True)
    factor_sueldo = fields.Float(string=_('Factor por sueldo percibido'), compute='_factor_sueldo', readonly=True)
    fecha_inicio = fields.Date('Fecha inicio')
    fecha_fin = fields.Date('Fecha fin')

    ######## Variables del seguro ####################3
    apotacion_infonavit = fields.Float(string=_('Aportación al Infonavit (%)'), default=5, digits = (12,3))
    umi = fields.Float(string=_('UMI (Unidad Mixta INFONAVIT)'), default=82.22, digits = (12,3))
    sbcm_general = fields.Float(string=_('General (UMA)'), default=25, digits = (12,3))
    sbcm_inv_inf = fields.Float(string=_('Para invalidez e Infonavit (UMA)'), default=25, digits = (12,3))
    rt_clase1 = fields.Float(string=_('Clase 1'), default=0.55456, digits = (12,6))
    rt_clase2 = fields.Float(string=_('Clase 2'), default=1.130658, digits = (12,6))
    rt_clase3 = fields.Float(string=_('Clase 3'), default=2.59844, digits = (12,6))
    rt_clase4 = fields.Float(string=_('Clase 4'), default=4.65325, digits = (12,6))
    rt_clase5 = fields.Float(string=_('Clase 5'), default=7.58875, digits = (12,6))
    enf_mat_cuota_fija = fields.Float(string=_('Cuota fija (%)'), default=20.4, digits = (12,3))
    enf_mat_excedente_p = fields.Float(string=_('Excedente de 3 UMA P (%)'), default=1.10, digits = (12,3))
    enf_mat_excedente_e = fields.Float(string=_('Excedente de 3 UMA E (%)'), default=0.40, digits = (12,3))

    enf_mat_prestaciones_p = fields.Float(string=_('Prestaciones en dinero P (%)'), default=0.7, digits = (12,3))
    enf_mat_prestaciones_e = fields.Float(string=_('Prestaciones en dinero E (%)'), default=0.25, digits = (12,3))
    enf_mat_gastos_med_p = fields.Float(string=_('Gastos médicos personales P (%)'), default=1.05, digits = (12,3))
    enf_mat_gastos_med_e = fields.Float(string=_('Gastos médicos personales E (%)'), default=0.375, digits = (12,3))

    inv_vida_p = fields.Float(string=_('Invalidez y vida P (%)'), default=1.75, digits = (12,3))
    inv_vida_e = fields.Float(string=_('Invalidez y vida E (%)'), default=0.625, digits = (12,3))

    cesantia_vejez_p = fields.Float(string=_('Cesantía y vejez P (%)'), default=3.15, digits = (12,3))
    cesantia_vejez_e = fields.Float(string=_('Cesantía y vejez E (%)'), default=1.125, digits = (12,3))

    retiro_p = fields.Float(string=_('Retiro (%)'), default=2, digits = (12,3))
    guarderia_p = fields.Float(string=_('Guardería y prestaciones sociales (%)'), default=1, digits = (12,3))

    caja_ahorro_abono = fields.Many2one('hr.salary.rule', string='Caja / Fondo Ahorro abono')
    caja_ahorro_retiro = fields.Many2one('hr.salary.rule', string='Caja / Fondo Ahorro retiro')

    isn =  fields.Float(string=_('Impuesto sobre nómina'), default='2.0', digits = (12,2))

    @api.constrains('name')
    def _check_name(self):
        if self.name:
            if self.search([('id', '!=', self.id),('name','=',self.name)]):
                raise ValidationError(_('Reference with same name already exist.'))
            
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {})
        default.setdefault('name', _("%s (copy)") % (self.name or ''))
        return super(TablasCFDI, self).copy(default)
    
    @api.model
    def default_get(self,fields):
        res = super(TablasCFDI,self).default_get(fields)
        if 'name' in fields:
            res['name'] = self.env['ir.sequence'].next_by_code('tablas.cfdi.reference')
        return res

    @api.depends('funcion_ingresos')
    def _compute_funcion_dias(self):
        self.funcion_dias = 100 - self.funcion_ingresos

    @api.depends('total_dias_trabajados', 'total_sueldo_percibido')
    def _factor_dias(self):
        if self.total_dias_trabajados > 0:
            self.factor_dias = (self.importe_utilidades*(self.funcion_dias/100)) / self.total_dias_trabajados
        else:
            self.factor_dias = 0 

    @api.depends('total_dias_trabajados', 'total_sueldo_percibido')
    def _factor_sueldo(self):
        if self.total_sueldo_percibido > 0:
            self.factor_sueldo = (self.importe_utilidades*(self.funcion_ingresos/100)) / self.total_sueldo_percibido
        else:
            self.factor_sueldo = 0 

    def calcular_reparto_utilidades(self):
        payslips = self.env['hr.payslip'].search([('date_from', '>=', self.fecha_inicio), ('date_to', '<=', self.fecha_fin),('tipo_nomina','=', 'O')])
        work100_lines = payslips.mapped('worked_days_line_ids').filtered(lambda x:x.code=='WORK100')
        net_lines = payslips.mapped('line_ids').filtered(lambda x:x.code=='NET')
        
        total_dias_trabajados, total_sueldo_percibido = 0.0, 0.0
        
        total_dias_by_employee = {}
        total_sueldo_employee = {}
        for line in work100_lines:
            total_dias_trabajados += line.number_of_days
            if line.payslip_id.employee_id not in total_dias_by_employee:
                total_dias_by_employee.update({line.payslip_id.employee_id: 0.0})
            total_dias_by_employee[line.payslip_id.employee_id] += line.number_of_days
            
        for line in net_lines:
            total_sueldo_percibido += line.total
            if line.slip_id.employee_id not in total_sueldo_employee:
                total_sueldo_employee.update({line.slip_id.employee_id: 0.0})
            total_sueldo_employee[line.slip_id.employee_id] += line.total
        
        employees = list(set(list(total_dias_by_employee.keys())  + list(total_sueldo_employee.keys())))
        for employee in employees:
            employee.write({'dias_utilidad' : total_dias_by_employee.get(employee, 0.0), 'sueldo_utilidad' : total_sueldo_employee.get(employee,0.0)})
            
        self.write({'total_dias_trabajados': total_dias_trabajados, 'total_sueldo_percibido':total_sueldo_percibido})
        
        return True

    def button_dummy(self):
        self.calcular_reparto_utilidades()
        return True
