# -*- coding: utf-8 -*-
from odoo import models,fields,api
from odoo.exceptions import Warning
import os
from lxml import etree
import base64
import json, xmltodict
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

class NominaLiquidaciones(models.TransientModel):
    _name ='nomina.liquidaciones'
    _description ='Liquidaciones'

    employee_id = fields.Many2one("hr.employee", string='Empleado')

    def generate_liquidaciones_report(self):
        self.ensure_one()
        [data] = self.read()
        ctx = self._context.copy()
        
        if ctx.get('active_ids'):
            payslips = self.env['hr.payslip.run'].browse(ctx.get('active_id')).slip_ids.filtered(lambda x: x.employee_id.id == self.employee_id.id and x.nom_liquidacion == True)

            datas = {
                'ids': self.ids,
                'model': 'hr.payslip.run',
                'form': data,
                'payslips': payslips,
            }
            
            return self.env.ref('nomina_cfdi_extras.report_nomina_liquidaciones').report_action(self, data=datas)

class LiquidacionesReport(models.AbstractModel):
    _name = "report.nomina_cfdi_extras.report_liquidaciones_document"
    _description = "Liquidaciones PDF Report"
    
    @api.model
    def _get_report_values(self, docids, data=None):
        ctx = self._context.copy()
        model = ctx.get('active_model')
        active_model = self.env[model].browse(ctx.get('active_id'))
        wizard_id = self.env['nomina.liquidaciones'].browse(data['ids'])
        payslips = active_model.browse(ctx.get('active_id')).slip_ids.filtered(lambda x: x.employee_id.id == wizard_id.employee_id.id and x.nom_liquidacion == True)
        docs = payslips
        docargs = {
            'doc_ids': self.ids,
            'doc_model': model,
            'docs': docs,
            'data': data,
        }
        return docargs
