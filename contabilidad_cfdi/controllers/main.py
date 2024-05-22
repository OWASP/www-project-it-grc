# -*- coding: utf-8 -*-
from odoo import _
import odoo.http as http
from odoo.http import request
from odoo.addons.web.controllers.export import ExcelExport
from datetime import datetime
import json

class TableExporterXML(http.Controller):
    @http.route('/web/pivot/export_xml', type='http', auth="user")
    def export_xml(self, data, token):
        jdata = json.loads(data)
        headers = jdata['headers']
        rows = jdata['rows']
        jdata['measure_row']
        
class ExcelExportViewAccount(ExcelExport):
    def __getattr__(self, name):
        if name == 'fmt':
            raise AttributeError()
        return super(ExcelExportViewAccount, self).__getattr__(name)
    
    @http.route('/web/export/xls_txt_diot_download', type='http', auth='user')
    def export_account_xls_txt_view(self, token, **kw):
        record_ids = json.loads(kw.get('record_ids'))
        report_type = kw.get('report_type')
        lines = request.env['reporte.diot.wizard.line'].sudo().search([('id', 'in',record_ids)])
        rows = []
        tipo_proveedor_dict = dict([('04', _('04 - Proveedor nacional')),('05', _('05 - Proveedor extranjero')), ('15', _('15 - Proveedor global'))])
        tipo_operacion_dict = dict([('03', _('03 - Provisión de servicios profesionales')),('06', _('06 - Arrendamientos')), ('85', _('85 - Otros')),])
        for line in lines:
            data = [line.tipo_proveedor or '', #tipo_proveedor_dict.get(line.tipo_proveedor) or '',
                    line.tipo_operacion or '', #tipo_operacion_dict.get(line.tipo_operacion) or '', 
                    line.rfc or '', 
                    line.registro_tributario or '', 
                    line.partner_id.name or '',
                    line.pais or '',
                    line.nacionalidad or '',
                    round(line.pagado_16_15_amount) or '',
                    round(line.pagado_15_amount) or '',
                    round(line.pagado_16_amount_no_acreditable) or '',
                    round(line.pagado_11_10_amount) or '',
                    round(line.pagado_10_amount) or '',
                    round(line.pagado_8_amount) or '',
                    round(line.pagado_11_amount_no_acreditable) or '',
                    round(line.pagado_8_amount_no_acreditable) or '',
                    round(line.importacion_16) or '',
                    round(line.importacion_16_na) or '',
                    round(line.importacion_11) or '',
                    round(line.importacion_11_na) or '',
                    round(line.importacion_exento) or '',
                    round(line.pagado_0_amount) or '',
                    round(line.pagado_exento) or '',
                    round(line.iva_retenido) or '',
                    round(line.iva_devoluciones) or '',
                    ]

            if report_type=='txt':
                rows.append('|'.join(str(v) for v in data)+'|')
            else:
                rows.append(data)
        if report_type=='txt':
            content = '\n'.join(rows)
            filename = 'DIOT_%s.txt'%(datetime.today().strftime("%Y_%m_%d_%H_%M_%S"))
            content_type = 'text/csv;charset=utf8'
        else:
            columns_headers = ["Tipo de tercero", "Tipo de operacion","RFC", "No. ID fiscal", "Nombre", "Pais", "Nacionalidad", 'Pagado 16%', 'Pagado 15%', 'Pagado 16% NA', 'Pagado 11%','Pagado 10%', 'Pagado 8%', 'Pagado 11% NA','Pagado 8% NA', 'Importacion 16%', 'Importacion 16% NA', 'Importacion 11%', 'Importacion 11 NA%', 'Importacion Exento%', 'Pagado 0%', 'Pagado exento', 'IVA Retenido', 'IVA devoluciones']

            filename = 'DIOT_%s.xls'%(datetime.today().strftime("%Y_%m_%d_%H_%M_%S"))
            content = self.from_data(columns_headers, rows)
            content_type = self.content_type
            
        return request.make_response(
            content,
            headers=[
                ('Content-Disposition', 'attachment; filename="%s"'
                 % filename),
                ('Content-Type', content_type)
            ],
            cookies={'fileToken': token}
        )

    @http.route('/web/export/xml_account_view', type='http', auth='user')
    def export_account_xml_view(self, token):
        datas = request.env['account.account'].sudo().create_coa()
        filename = (request.env.user.company_id.factura_dir or '') + 'Accounts.xml'
        return request.make_response(
            datas,
            headers=[
                ('Content-Disposition', 'attachment; filename="%s"'
                 % filename),
                ('Content-Type', 'application/xml')
            ],
            cookies={'fileToken': token}
        )
        