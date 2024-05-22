# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class HrEmployeePublic(models.Model):
    _inherit = "hr.employee.public"
    
    no_empleado = fields.Char(_('Número de empleado'))
    tipo_pago = fields.Selection(selection=[('transferencia', 'Transferencia'),('efectivo', 'Efectivo'),
                                         ('cheque', 'Cheque')],
        string=_('Tipo de Pago'),
    )
    banco = fields.Many2one('res.bank','Banco empleado')
    no_cuenta = fields.Char(_('No. cuenta empleado'))
    rfc = fields.Char(_('RFC'))
    curp = fields.Char(_('CURP'))
    segurosocial = fields.Char(_('Seguro social'))
    correo_electronico = fields.Char(_('Correo electrónico'))	
    tipo_cuenta = fields.Selection(selection=[('t_debido', 'Tarjeta de débito'),('cheques', 'Cheques'),
                                         ('c_ahorro', 'Cuenta de ahorro'),('t_credito', 'Tarjeta de crédito')],
        string=_('Tipo de cuenta'),
    )
    diario_pago = fields.Many2one('account.journal', string='Cuenta de pago', domain=[('type', 'in', ('bank', 'cash'))])

    registro_patronal_id = fields.Many2one('registro.patronal', string='Registro patronal')

    regimen = fields.Selection(
        selection=[('02', '02 - Sueldos'),
                   ('03', '03 - Jubilados'),
                   ('04', '04 - Pensionados'),
                   ('05', '05 - Asimilados Miembros Sociedades Cooperativas Produccion'),
                   ('06', '06 - Asimilados Integrantes Sociedades Asociaciones Civiles'),
                   ('07', '07 - Asimilados Miembros consejos'),
                   ('08', '08 - Asimilados comisionistas'),
                   ('09', '09 - Asimilados Honorarios'),
                   ('10', '10 - Asimilados acciones'),
                   ('11', '11 - Asimilados otros'),
                   ('12', '12 - Jubilados o Pensionados'),
                   ('13', '13 - Indemnización o Separación'),
                   ('99', '99 - Otro Regimen'),],
        string=_('Régimen'),
    )
    contrato = fields.Selection(
        selection=[('01', '01 - Contrato de trabajo por tiempo indeterminado'), 
                   ('02', '02 - Contrato de trabajo para obra determinada'), 
                   ('03', '03 - Contrato de trabajo por tiempo determinado'),
                   ('04', '04 - Contrato de trabajo por temporada'), 
                   ('05', '05 - Contrato de trabajo sujeto a prueba'),
                   ('06', '06 - Contrato de trabajo con capacitación inicial'), 
                   ('07', '07 - Modalidad de contratación por pago de hora laborada'), 
                   ('08', '08 - Modalidad de trabajo por comisión laboral'), 
                   ('09', '09 - Modalidades de contratación donde no existe relación de trabajo'), 
                   ('10', '10 - Jubilación, pensión, retiro'), 
                   ('99', '99 - Otro contrato'),],
        string=_('Contrato'),
    )

    jornada = fields.Selection(
        selection=[('01', '01 - Diurna'), 
                   ('02', '02 - Nocturna'), 
                   ('03', '03 - Mixta'),
                   ('04', '04 - Por hora'), 
                   ('05', '05 - Reducida'),
                   ('06', '06 - Continuada'), 
                   ('07', '07 - Partida'), 
                   ('08', '08 - Por turnos'), 
                   ('99', '99 - Otra Jornada'),],
        string=_('Jornada'),
    )
    estado = fields.Many2one('res.country.state','Lugar donde labora (estado)')

    empleado_nombre = fields.Char("Nombre")
    empleado_paterno = fields.Char("Apellido Paterno")
    empleado_materno = fields.Char("Apellido Materno")
    sindicalizado = fields.Boolean('Sindicalizado', default=False)
    domicilio_receptor = fields.Char("Código postal (SAT)")