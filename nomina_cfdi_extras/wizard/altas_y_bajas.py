# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from collections import defaultdict
from datetime import datetime
from dateutil.relativedelta import relativedelta
from collections import defaultdict
import io
import xlwt
import itertools
from odoo.tools.misc import xlwt
import base64

class AltasYBajas(models.TransientModel):
    _name = 'altas.y.bajas'
    _description = 'Altas Y Bajas'
    
    start_date = fields.Date("Fecha inicio")
    end_date = fields.Date("Fecha fin")
    tipo = fields.Selection([('altas','Altas'),('bajas','Bajas')], string='Tipo')
    file_data = fields.Binary("File Data")
    
    def print_altas_y_bajas_report(self):
        domain = []
        if self.start_date:
            domain.append(('fecha','>=', self.start_date))
        if self.end_date:
            domain.append(('fecha','<=', self.end_date))
        if self.tipo == 'altas':
            domain.append(('tipo_de_incidencia', 'in', ('Alta','Reingreso')))
        if self.tipo == 'bajas':
            domain.append(('tipo_de_incidencia', '=', 'Baja'))
        domain.append(('state', '=', 'done'))

        incidencias = self.env['incidencias.nomina'].search(domain)

        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Altas y Bajas')
        col_width = 256 * 20
        try:
            for i in itertools.count():
                worksheet.col(i).width = col_width
        except ValueError:
            pass
        bold = xlwt.easyxf("font: bold on;")
        
        company = self.env.user.company_id
        start_date = self.start_date and self.start_date.strftime('%d/%m/%Y') or ''
        end_date = self.end_date and self.end_date.strftime('%d/%m/%Y') or ''
        
        worksheet.write(0, 0, company.name, bold)
        worksheet.write(2, 0, 'Fecha', bold)
        worksheet.write(2, 1, start_date)
        worksheet.write(2, 3, end_date)
        worksheet.write(3, 0, 'Tipo de movimiento', bold)
        worksheet.write(3, 1, 'Altas' if self.tipo == 'altas' else 'Bajas')
        
        worksheet.write(5, 0, 'No. Empleado', bold)
        worksheet.write(5, 1, 'Nombre', bold)
        worksheet.write(5, 2, 'Fecha', bold)
        worksheet.write(5, 3, 'Salario', bold)
        worksheet.write(5, 4, 'SDI', bold)
        worksheet.write(5, 5, 'Puesto', bold)
        worksheet.write(5, 6, 'Registro Patronal', bold)
        worksheet.write(5, 7, 'Seguro Social', bold)
        worksheet.write(5, 8, 'Curp', bold)
        
        row = 6
        for incidencia in incidencias:
            employee_no = incidencia.employee_id and incidencia.employee_id.no_empleado or False
            employee_name = incidencia.employee_id and incidencia.employee_id.name or False
            incidencia_fecha = incidencia.fecha.strftime('%d/%m/%Y')
            contract = incidencia.employee_id and incidencia.employee_id.contract_id or False
            salario = contract and contract.sueldo_diario or False
            sdi = contract and contract.sueldo_diario_integrado or False
            puesto = incidencia.employee_id and incidencia.employee_id.job_title or False
            registro_patronal = incidencia.employee_id and incidencia.employee_id.registro_patronal_id.registro_patronal or False
            seguro_social = incidencia.employee_id and incidencia.employee_id.segurosocial or False
            curp = incidencia.employee_id and incidencia.employee_id.curp or False
            
            worksheet.write(row, 0, employee_no)
            worksheet.write(row, 1, employee_name)
            worksheet.write(row, 2, incidencia_fecha)
            worksheet.write(row, 3, salario)
            worksheet.write(row, 4, sdi)
            worksheet.write(row, 5, puesto)
            worksheet.write(row, 6, registro_patronal)
            worksheet.write(row, 7, seguro_social)
            worksheet.write(row, 8, curp)
            row += 1
            
        fp = io.BytesIO()
        workbook.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        
        self.write({'file_data':base64.b64encode(data)})
        action = {
            'name': 'Altas y Bajas',
            'type': 'ir.actions.act_url',
            'url': "/web/content/?model="+self._name+"&id=" + str(self.id) + "&field=file_data&download=true&filename=altas_y_bajas.xls",
            'target': 'self',
            }
        return action
    
    
        
        
