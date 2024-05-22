# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import requests
import json
from odoo.exceptions import Warning, UserError
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar

class PolizasReport(models.TransientModel):
    _name = 'polizas.report'
    _description = 'polizas report'
    
    fecha_mes = fields.Selection([('01', 'Enero'), ('02', 'Febrero'), ('03', 'Marzo'), ('04', 'Abril'), ('05', 'Mayo'), ('06', 'Junio'),
                                    ('07', 'Julio'), ('08', 'Agosto'), ('09', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre')],
                                   string='Mes', required= True)
    fecha_ano = fields.Selection([('2024', '2024'),('2023', '2023'),('2022', '2022'),('2021', '2021'),('2020','2020')],
                                   required= True, string='Año')
    tiposolicitud = fields.Selection(
        selection=[('AF', 'Acto de Fiscalización'), 
                   ('FC', 'Fiscalización Compulsa'),
                   ('DE', 'Devolución'),
                   ('CO', 'Compensación'),],
        string=_('Tipo de comprobante'),
        default = 'AF',
    )
    numorden = fields.Char('Número de orden', help='Requerido para tipo de solicitud AF y FC.')
    numtramite = fields.Char('Número de trámite', help='Requerido para tipo de solicitud DE y CO.')
    account_id = fields.Many2one('account.account',string='Solo pólizas de cuenta')

    def action_print_polizas_report(self):
        ctx = self._context.copy()
        journal_ids = self.env['account.journal'].search([])
        domain = [('journal_id', 'in',journal_ids.ids)]
        start_date = fields.Datetime.from_string(str(self.fecha_ano) + '-' + str(self.fecha_mes) + '-01')
        end_days = calendar.monthrange(int(self.fecha_ano), int(self.fecha_mes))
        end_date = fields.Datetime.from_string(str(self.fecha_ano) + '-' + str(self.fecha_mes) + '-' + str(end_days[1]))
        domain.append(('date','>=',start_date))
        domain.append(('date','<=',end_date))

        journal_entries = self.env['account.move'].search(domain)
        company = self.env.company
        if not company.archivo_cer or not company.archivo_key:
           raise UserError("No tiene cargado el certificado correctamente.")
        archivo_cer = company.archivo_cer
        archivo_key = company.archivo_key
        request_params = {
                'informacion': {
                      'api_key': company.proveedor_timbrado,
                      'modo_prueba': company.modo_prueba,
                      'proceso': 'polizas',
                      'RFC': company.vat,
                      'Mes': self.fecha_mes,
                      'Anio': self.fecha_ano,
                      'version': '2.0',
                },
                'Polizas':{
                      'RFC': company.vat,
                      'Mes': self.fecha_mes,
                      'Anio': self.fecha_ano,
                      'TipoSolicitud': self.tiposolicitud,
                      'NumOrden': self.numorden,
                      'NumTramite': self.numtramite,
                },
                'certificados': {
                      'archivo_cer': archivo_cer.decode("utf-8") or False,
                      'archivo_key': archivo_key.decode("utf-8") or False,
                      'contrasena': company.contrasena,
                },}
        polizas = []
        for move in journal_entries:
            transaccion = []
            for line in move.line_ids:
                compnal = []
                if len(line.account_cfdi_ids) >= 1:
                    for cfdi_line in line.account_cfdi_ids:
                        compnal.append({
                              'UUID_CFDI' : cfdi_line.uuid,
                              'RFC' : cfdi_line.rfc_cliente,
                              'MontoTotal' : cfdi_line.monto,
                              'Moneda' : cfdi_line.moneda,
                              'TipCamb' : cfdi_line.tipocamb,
                           },)
                transaccion.append({
                       'DesCta' : line.account_id.name or '',
                       'NumCta' : line.account_id.code or '',
                      # 'cliente' : line.partner_id.name or '',
                       'Concepto' : line.name or '',
                       'Debe' : line.debit,
                       'Haber' : line.credit,
                       'compnal' : compnal,
                       })
            polizas.append({'NumUnIdenPol' : move.name, 
                        #  'reference' : move.ref or '',
                           'Concepto' : move.journal_id.name,
                           'Fecha' : move.date.strftime("%Y-%m-%d"),
                           'transaccion' : transaccion
                           })
        request_params.update({'plz': polizas})

        url=''
        if company.proveedor_timbrado == 'multifactura':
            url = '%s' % ('http://facturacion.itadmin.com.mx/api/contabilidad')
        elif company.proveedor_timbrado == 'multifactura2':
            url = '%s' % ('http://facturacion2.itadmin.com.mx/api/contabilidad')
        elif company.proveedor_timbrado == 'multifactura3':
            url = '%s' % ('http://facturacion3.itadmin.com.mx/api/contabilidad')
        elif company.proveedor_timbrado == 'gecoerp':
            if company.modo_prueba:
                url = '%s' % ('https://itadmin.gecoerp.com/invoice/?handler=OdooHandler33')
            else:
                url = '%s' % ('https://itadmin.gecoerp.com/invoice/?handler=OdooHandler33')
        if not url:
            raise UserError("Seleccione el proveedor de timbrado en la configuración de la compañía.")

        response = requests.post(url,auth=None,verify=False, data=json.dumps(request_params),headers={"Content-type": "application/json"})
        if "Whoops, looks like something went wrong." in response.text:
             invoice.write({'proceso_timbrado': False})
             self.env.cr.commit()
             raise UserError(_(
                 "Error en el proceso, espere un minuto y vuelva a intentar nuevamente. \nSi el error aparece varias veces reportarlo con la persona de sistemas."))
        else:
            json_response = response.json()

        estado_factura = json_response.get('estado_conta','')
        if not estado_factura:
           estado_factura = json_response.get('estado_factura','')
        if estado_factura == 'problemas_contabilidad' or estado_factura == 'problemas_factura':
            raise UserError(_(json_response['problemas_message']))
        if json_response.get('conta_xml'):

            #_logger.info("xml %s", json_response['conta_xml'])
            #_logger.info("zip %s", json_response['conta_zip'])
            #return base64.b64decode(json_response['conta_xml'])
            try:
                form_id = self.env['ir.model.data'].check_object_reference('contabilidad_cfdi', 'reporte_conta_xml_zip_download_wizard_download_form_view_itadmin')[1]
            except ValueError:
                form_id = False
            ctx.update({'default_xml_data': json_response['conta_xml'], 'default_zip_data': json_response.get('conta_zip', None)})
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'conta.xml.zip.download',
                'views': [(form_id, 'form')],
                'view_id': form_id,
                'target': 'new',
                'context': ctx,
            }
        return True
    
