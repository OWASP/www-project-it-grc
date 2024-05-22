# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

from collections import defaultdict
from datetime import datetime
from dateutil.relativedelta import relativedelta

class CrearFaltasFromRetardos(models.TransientModel):
    _name = 'crear.faltas.from.retardos'
    _description = 'CrearFaltasFromRetardos'
    
    start_date = fields.Date("Fecha inicio")
    end_date = fields.Date("Fecha fin")
    
    
    def action_crear_faltas_from_ratardos(self):
        start_date = self.start_date
        end_date = self.end_date
        records = self.env['retardo.nomina'].search([('fecha','>=',start_date), ('fecha', '<=', end_date),('state','=','done')])
        record_by_employee = defaultdict(list)
        for retardo in records:
            record_by_employee[retardo.employee_id.id].append(retardo.id)
        retardos_x_falta = int(self.env['ir.config_parameter'].sudo().get_param('nomina_cfdi_extras.numoer_de_retardos_x_falta', 0))
        faltas_nomina_obj = self.env['faltas.nomina']
        
        
        field_list = faltas_nomina_obj._fields.keys()
        default_vals = faltas_nomina_obj.default_get(field_list)
        en_date = end_date #datetime.strptime(end_date,DEFAULT_SERVER_DATE_FORMAT)
        
        for emp_id,retardos in record_by_employee.items():
            record_count = len(retardos)
            if record_count >= retardos_x_falta and retardos_x_falta:
                sub_days = int(record_count/retardos_x_falta)
                fecha_inicio = en_date - relativedelta(days=sub_days) + relativedelta(days=1)
                vals = {}
                vals.update(default_vals)
                vals.update({
                    'employee_id':emp_id,
                    'fecha_inicio' : fecha_inicio.strftime(DEFAULT_SERVER_DATE_FORMAT),
                    'fecha_fin' : en_date,
                    'tipo_de_falta': 'retardo',
                    'dias': sub_days,
                    })
                faltas_nomina_obj.create(vals)

        return
