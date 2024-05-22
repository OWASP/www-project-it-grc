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

class FoliosReport(models.TransientModel):
    _name = 'folios.report'

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

    def action_print_folios_report(self):
        ctx = self._context.copy()
        journal_ids = self.env['account.journal'].search(['|',('type', '=', 'sale'), ('type', '=', 'purchase')])
        domain = [('journal_id', 'in',journal_ids.ids)]
        start_date = fields.Datetime.from_string(str(self.fecha_ano) + '-' + str(self.fecha_mes) + '-01')
        end_days = calendar.monthrange(int(self.fecha_ano), int(self.fecha_mes))
        end_date = fields.Datetime.from_string(str(self.fecha_ano) + '-' + str(self.fecha_mes) + '-' + str(end_days[1]))
        domain.append(('date','>=',start_date))
        domain.append(('date','<=',end_date))

        journal_entries = self.env['account.move'].search(domain)
        company = self.env.user.company_id
        if not company.archivo_cer or not company.archivo_key:
           raise UserError("No tiene cargado el certificado correctamente.")
        archivo_cer = company.archivo_cer
        archivo_key = company.archivo_key
        request_params = {
                'informacion': {
                      'api_key': company.proveedor_timbrado,
                      'modo_prueba': company.modo_prueba,
                      'proceso': 'folios',
                      'RFC': company.vat,
                      'Mes': self.fecha_mes,
                      'Anio': self.fecha_ano,
                      'version': '2.0',
                },
                'RepAuxFol':{
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
        folios = []
        for move in journal_entries:
            if move.contabilidad_electronica:
               for line in move.line_ids:
                   if len(line.account_cfdi_ids) >= 1:
                      cfdi_line = line.account_cfdi_ids[0]
                      comprnal = {
                           'UUID_CFDI' : cfdi_line.uuid,
                           'RFC' : cfdi_line.rfc_cliente,
                           'MontoTotal' : cfdi_line.monto,
                           'Moneda' : cfdi_line.moneda if cfdi_line.moneda != 'MXN' else '',
                           'TipCamb' : cfdi_line.tipocamb if cfdi_line.moneda != 'MXN' else '',
                           }
                      folios.append({'NumUnIdenPol' : move.name, # move.ref or '',
                           'Fecha' : move.date.strftime("%Y-%m-%d"), 
                           'ComprNal':comprnal})
        request_params.update({'DetAuxFol': folios})

        #_logger.info(json.dumps(request_params))

        url=''
        company = self.env.user.company_id
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
            raise Warning("Seleccione el proveedor de timbrado en la configuración de la compañía.")

        response = requests.post(url,auth=None,verify=False, data=json.dumps(request_params),headers={"Content-type": "application/json"})
        #_logger.info('something ... %s', response.text)

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
                form_id = self.env['ir.model.data'].get_object_reference('contabilidad_cfdi', 'reporte_conta_xml_zip_download_wizard_download_form_view_itadmin')[1]
            except ValueError:
                form_id = False
            ctx.update({'default_xml_data': json_response['conta_xml'], 'default_zip_data': json_response.get('conta_zip', None)})
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'conta.xml.zip.download',
                'views': [(form_id, 'form')],
                'view_id': form_id,
                'target': 'new',
                'context': ctx,
            }
        return True
    
