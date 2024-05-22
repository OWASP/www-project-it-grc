# -*- coding: utf-8 -*-
from odoo import models,fields,api, _
from odoo.exceptions import UserError
import os
from lxml import etree
import base64
import json
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.parser import parse
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.lib.units import mm

import logging
_logger = logging.getLogger(__name__)

class import_account_payment_from_xml(models.TransientModel):
    _name ='import.account.payment.from.xml'

    import_file = fields.Binary("Importar Archivo",required=False)
    file_name = fields.Char("Nombre del archivo")
    payment_id = fields.Many2one("account.payment",'Payment')

    def import_xml_file_button(self):
        self.ensure_one()
        if not self.import_file:
            raise UserError(_('Seleccione primero el archivo.'))
        p, ext = os.path.splitext(self.file_name)
        if ext[1:].lower() !='xml':
            raise UserError(_("Formato no soportado \"{}\", importa solo archivos XML").format(self.file_name))
        
        file_content = base64.b64decode(self.import_file)
        tree = etree.fromstring(file_content)
        payment_vals = {
            'cep_sello': tree.get('sello'),
            'cep_numeroCertificado' : tree.get('numeroCertificado',tree.get('NumeroCertificado')),
            'cep_cadenaCDA' : tree.get('cadenaCDA',tree.get('CadenaCDA')),
            'cep_claveSPEI' : tree.get('ClaveSPEI',tree.get('claveSPEI')),
            }
        self.payment_id.write(payment_vals)
        return True

    def import_xml_file_button_cargar(self):
        self.ensure_one()
        invoice_id = self.env['account.move'].browse(self._context.get('active_id'))
        if not self.import_file:
            raise UserError(_('Seleccione primero el archivo.'))
        p, ext = os.path.splitext(self.file_name)
        if ext[1:].lower() !='xml':
            raise UserError(_("Formato no soportado \"{}\", importa solo archivos XML").format(self.file_name))

        file_content = base64.b64decode(self.import_file)
        xml_data = etree.fromstring(file_content)
        if b'Version=\"4.0\"' in file_content:
           NSMAP = {
                 'xsi':'http://www.w3.org/2001/XMLSchema-instance',
                 'cfdi':'http://www.sat.gob.mx/cfd/4', 
                 'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital',
                 }
        else:
           NSMAP = {
                 'xsi':'http://www.w3.org/2001/XMLSchema-instance',
                 'cfdi':'http://www.sat.gob.mx/cfd/3', 
                 'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital',
                 }

        Emisor = xml_data.find('cfdi:Emisor', NSMAP)
        Receptor = xml_data.find('cfdi:Receptor', NSMAP)
        Complemento = xml_data.findall('cfdi:Complemento', NSMAP)

        for complementos in Complemento:
            TimbreFiscalDigital = complementos.find('tfd:TimbreFiscalDigital', NSMAP)
            if TimbreFiscalDigital:
                break

        amount_str = str(xml_data.attrib['Total']).split('.')
        qr_value = 'https://verificacfdi.facturaelectronica.sat.gob.mx/default.aspx?&id=%s&re=%s&rr=%s&tt=%s.%s&fe=%s' % (TimbreFiscalDigital.attrib['UUID'],
                                                 invoice_id.company_id.vat, 
                                                 invoice_id.partner_id.vat,
                                                 amount_str[0].zfill(10),
                                                 len(amount_str) == 2 and amount_str[1].ljust(6, '0') or '000000',
                                                 str(TimbreFiscalDigital.attrib['SelloCFD'])[-8:],
                                                 )
        options = {'width': 275 * mm, 'height': 275 * mm}
        ret_val = createBarcodeDrawing('QR', value=qr_value, **options)
        qrcode_image = base64.encodebytes(ret_val.asString('jpg'))

        cargar_values = {
            'total_factura': xml_data.attrib['Total'],
            'methodo_pago': 'MetodoPago' in xml_data.attrib and xml_data.attrib['MetodoPago'] or '',
            'forma_pago_id' : 'FormaPago' in xml_data.attrib and  self.env['catalogo.forma.pago'].sudo().search([('code','=',xml_data.attrib['FormaPago'])]) or '',
            'uso_cfdi_id': self.env['catalogo.uso.cfdi'].sudo().search([('code','=',Receptor.attrib['UsoCFDI'])]),
            'folio_fiscal' : TimbreFiscalDigital.attrib['UUID'],
            'tipo_comprobante': xml_data.attrib['TipoDeComprobante'],
            'fecha_factura': xml_data.attrib['Fecha'] and parse(xml_data.attrib['Fecha']).strftime(DEFAULT_SERVER_DATETIME_FORMAT) or False,
           # 'xml_invoice_link': xml_file_link,
            'factura_cfdi': True,
            'estado_factura': 'factura_correcta',
            'numero_cetificado' : xml_data.attrib['NoCertificado'],
            'cetificaso_sat' : TimbreFiscalDigital.attrib['NoCertificadoSAT'],
            'fecha_certificacion' : TimbreFiscalDigital.attrib['FechaTimbrado'],
            'selo_digital_cdfi' : TimbreFiscalDigital.attrib['SelloCFD'],
            'selo_sat' : TimbreFiscalDigital.attrib['SelloSAT'],
            'tipocambio' : xml_data.find('TipoCambio') and xml_data.attrib['TipoCambio'] or '1',
            'moneda': xml_data.attrib['Moneda'],
            'number_folio': xml_data.find('Folio') and xml_data.attrib['Folio'] or ' ',
            'cadena_origenal' : '||%s|%s|%s|%s|%s||' % (TimbreFiscalDigital.attrib['Version'], TimbreFiscalDigital.attrib['UUID'], TimbreFiscalDigital.attrib['FechaTimbrado'],
                                                         TimbreFiscalDigital.attrib['SelloCFD'], TimbreFiscalDigital.attrib['NoCertificadoSAT']),
            'qrcode_image': qrcode_image
            }
        invoice_id.write(cargar_values)

        if invoice_id.move_type == 'out_invoice':
           tax_grouped_tras = {}
           tax_grouped_ret = {}
           Conceptos = xml_data.find('cfdi:Conceptos', NSMAP)
           for concepto in Conceptos:
              imp_prod = concepto.find('cfdi:Impuestos', NSMAP)
              if imp_prod:
                 traslados = imp_prod.find('cfdi:Traslados', NSMAP)
                 if traslados:
                    for traslado in traslados:
                       if 'TasaOCuota' in traslado.attrib:
                          if traslado.attrib['TipoFactor'] == 'Cuota':
                             tasa = str(float(traslado.attrib['TasaOCuota']))
                          else:
                             tasa = str(float(traslado.attrib['TasaOCuota'])*100)
                       else:
                          tasa = str(0)
                       tax_exist = self.env['account.tax'].search([('impuesto','=',traslado.attrib['Impuesto']), ('type_tax_use','=','sale'), 
                                                   ('tipo_factor','=',traslado.attrib['TipoFactor']), ('amount', '=', tasa), 
                                                   ('company_id','=',self.env.company.id)],limit=1)
                       if not tax_exist:
                          raise UserError(_("Un impuesto en el XML no está configurado en el sistema"))

                       if 'Importe' in traslado.attrib:
                          importe = traslado.attrib['Importe']
                       else:
                          importe = 0
                       key = tax_exist.id
                       val = {'tax_id': tax_exist.id,
                              'base': float(traslado.attrib['Base']),
                              'amount': float(importe),}
                       if key not in tax_grouped_tras:
                           tax_grouped_tras[key] = val
                       else:
                           tax_grouped_tras[key]['base'] += float(traslado.attrib['Base'])
                           tax_grouped_tras[key]['amount'] += float(importe)


                 retenciones = imp_prod.find('cfdi:Retenciones', NSMAP)
                 if retenciones:
                    for retencion in retenciones:
                       if 'TasaOCuota' in retencion.attrib:
                          tasa = str(float(retencion.attrib['TasaOCuota'])*-100)
                       else:
                          tasa = str(0)
                       tax_exist = self.env['account.tax'].search([('impuesto','=',retencion.attrib['Impuesto']), ('type_tax_use','=','sale'), 
                                                   ('tipo_factor','=',retencion.attrib['TipoFactor']), ('amount', '=', tasa), 
                                                   ('company_id','=',self.env.company.id)],limit=1)
                       if not tax_exist:
                          raise UserError(_("Un impuesto en el XML no está configurado en el sistema"))

                       if 'Importe' in retencion.attrib:
                          importe = retencion.attrib['Importe']
                       else:
                          importe = 0
                       key = tax_exist.id
                       val = {'tax_id': tax_exist.id,
                              'base': float(retencion.attrib['Base']),
                              'amount': float(importe),}
                       if key not in tax_grouped_ret:
                           tax_grouped_ret[key] = val
                       else:
                           tax_grouped_ret[key]['base'] += float(retencion.attrib['Base'])
                           tax_grouped_ret[key]['amount'] += float(importe)

           impuestos = {}
           if tax_grouped_tras or tax_grouped_ret:
                retenciones = []
                traslados = []
                if tax_grouped_tras:
                   for line in tax_grouped_tras.values():
                       tax = self.env['account.tax'].browse(line['tax_id'])
                       if tax.tipo_factor == 'Exento':
                          tasa_tr = ''
                       elif tax.tipo_factor == 'Cuota':
                          tasa_tr = invoice_id.set_decimals(tax.amount, 6)
                       else:
                          tasa_tr = invoice_id.set_decimals(tax.amount / 100.0, 6)
                       traslados.append({'impuesto': tax.impuesto,
                                         'TipoFactor': tax.tipo_factor,
                                         'tasa': tasa_tr,
                                         'importe': invoice_id.set_decimals(line['amount'], invoice_id.currency_id.no_decimales) if tax.tipo_factor != 'Exento' else '',
                                         'base': invoice_id.set_decimals(line['base'], invoice_id.currency_id.no_decimales),
                                         'tax_id': line['tax_id'],
                                         })
                   impuestos.update({'translados': traslados,})
                if tax_grouped_ret:
                   for line in tax_grouped_ret.values():
                       tax = self.env['account.tax'].browse(line['tax_id'])
                       retenciones.append({'impuesto': tax.impuesto,
                                         'TipoFactor': tax.tipo_factor,
                                         'tasa': invoice_id.set_decimals(float(tax.amount) / 100.0 * -1, 6),
                                         'importe': invoice_id.set_decimals(line['amount'], invoice_id.currency_id.no_decimales),
                                         'base': invoice_id.set_decimals(line['base'], invoice_id.currency_id.no_decimales),
                                         'tax_id': line['tax_id'],
                                         })
                   impuestos.update({'retenciones': retenciones,})
           invoice_id.write({'tax_payment': json.dumps(impuestos)})

        #xml_file = open(xml_file_link, 'w')
        #xml_invoice = base64.b64decode(self.import_file)
        #xml_file.write(xml_invoice.decode("utf-8"))
        #xml_file.close()

        return True

    def import_xml_file_payment(self):
        self.ensure_one()
        payment_id = self.env['account.payment'].browse(self._context.get('active_id'))
        if not self.import_file:
            raise UserError("Seleccione primero el archivo.")
        p, ext = os.path.splitext(self.file_name)
        if ext[1:].lower() !='xml':
            raise UserError(_("Formato no soportado \"{}\", importa solo archivos XML").format(self.file_name))

        file_content = base64.b64decode(self.import_file)
        xml_data = etree.fromstring(file_content)
        if b'Version=\"4.0\"' in file_content:
           NSMAP = {
                 'xsi':'http://www.w3.org/2001/XMLSchema-instance',
                 'cfdi':'http://www.sat.gob.mx/cfd/4', 
                 'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital',
                 'pago20': 'http://www.sat.gob.mx/Pagos20'
                 }
        else:
           NSMAP = {
                 'xsi':'http://www.w3.org/2001/XMLSchema-instance',
                 'cfdi':'http://www.sat.gob.mx/cfd/3', 
                 'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital',
                 'pago10': 'http://www.sat.gob.mx/Pagos',
                 }

        Emisor = xml_data.find('cfdi:Emisor', NSMAP)
        Receptor = xml_data.find('cfdi:Receptor', NSMAP)
        Complemento = xml_data.find('cfdi:Complemento', NSMAP)

        TimbreFiscalDigital = Complemento.find('tfd:TimbreFiscalDigital', NSMAP)

        cfdi_version = xml_data.attrib['Version']
        monto_total = 0
        if cfdi_version == '4.0':
            pagos = Complemento.find('pago20:Pagos', NSMAP)
            pago = pagos.find('pago20:Totales', NSMAP)
            monto_total = pago.attrib['MontoTotalPagos']
        else:
            pagos = Complemento.find('pago10:Pagos', NSMAP)
            try:
                pago = pagos.find('pago10:Pago',NSMAP)
                monto_total = pago.attrib['Monto']
            except Exception as e:
                for payment in pagos.find('pago10:Pago',NSMAP):
                     monto_total += float(payment.attrib['Monto'])

        amount_str = str(monto_total).split('.')
        qr_value = 'https://verificacfdi.facturaelectronica.sat.gob.mx/default.aspx?&id=%s&re=%s&rr=%s&tt=%s.%s&fe=%s' % (TimbreFiscalDigital.attrib['UUID'],
                                                 payment_id.company_id.vat, 
                                                 payment_id.partner_id.vat,
                                                 amount_str[0].zfill(10),
                                                 len(amount_str) == 2 and amount_str[1].ljust(6, '0') or '000000',
                                                 str(TimbreFiscalDigital.attrib['SelloCFD'])[-8:],
                                                 )
        options = {'width': 275 * mm, 'height': 275 * mm}
        ret_val = createBarcodeDrawing('QR', value=qr_value, **options)
        qrcode_image = base64.encodebytes(ret_val.asString('jpg'))

        cargar_values = {
            'total_pago': monto_total,
            'methodo_pago': 'MetodoPago' in xml_data.attrib and xml_data.attrib['MetodoPago'] or '',
            'forma_pago_id' : 'FormaPago' in xml_data.attrib and  self.env['catalogo.forma.pago'].sudo().search([('code','=',xml_data.attrib['FormaPago'])]) or '',
#            'uso_cfdi': Receptor.attrib['UsoCFDI'],
            'folio_fiscal' : TimbreFiscalDigital.attrib['UUID'],
            #'tipo_comprobante': xml_data.attrib['TipoDeComprobante'],
            'fecha_pago': xml_data.attrib['Fecha'] and parse(xml_data.attrib['Fecha']).strftime(DEFAULT_SERVER_DATETIME_FORMAT) or False,
           # 'xml_invoice_link': xml_file_link,
            #'factura_cfdi': True,
            'estado_pago': 'pago_correcto',
            'numero_cetificado' : xml_data.attrib['NoCertificado'],
            'cetificaso_sat' : TimbreFiscalDigital.attrib['NoCertificadoSAT'],
            'fecha_certificacion' : TimbreFiscalDigital.attrib['FechaTimbrado'],
            'selo_digital_cdfi' : TimbreFiscalDigital.attrib['SelloCFD'],
            'selo_sat' : TimbreFiscalDigital.attrib['SelloSAT'],
            'tipocambiop' : xml_data.find('TipoCambio') and xml_data.attrib['TipoCambio'] or '1',
            'monedap': xml_data.attrib['Moneda'],
            'number_folio': xml_data.find('Folio') and xml_data.attrib['Folio'] or ' ',
            'cadena_origenal' : '||%s|%s|%s|%s|%s||' % (TimbreFiscalDigital.attrib['Version'], TimbreFiscalDigital.attrib['UUID'], TimbreFiscalDigital.attrib['FechaTimbrado'],
                                                         TimbreFiscalDigital.attrib['SelloCFD'], TimbreFiscalDigital.attrib['NoCertificadoSAT']),
            'qrcode_image': qrcode_image
            }
        payment_id.add_resitual_amounts()
        payment_id.write(cargar_values)

        #xml_file = open(xml_file_link, 'w')
        #xml_invoice = base64.b64decode(self.import_file)
        #xml_file.write(xml_invoice.decode("utf-8"))
        #xml_file.close()

        return True
