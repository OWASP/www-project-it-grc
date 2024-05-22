# -*- coding: utf-8 -*-
from odoo import models,fields,api, _
from odoo.exceptions import Warning, UserError
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

class import_payslip_from_xml(models.TransientModel):
    _name ='import.payslip.from.xml'
    _description = 'Importar XML nomina'

    import_file = fields.Binary("Importar Archivo",required=False)
    file_name = fields.Char("Nombre del archivo")
    payslip_id = fields.Many2one("hr.payslip",'Nomina')

    def import_xml_file_button_cargar(self):
        self.ensure_one()
        payslip_id = self.env['hr.payslip'].browse(self._context.get('active_id'))
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
                                                 payslip_id.company_id.vat, 
                                                 payslip_id.employee_id.rfc,
                                                 amount_str[0].zfill(10),
                                                 len(amount_str) == 2 and amount_str[1].ljust(6, '0') or '000000',
                                                 str(TimbreFiscalDigital.attrib['SelloCFD'])[-8:],
                                                 )
        options = {'width': 275 * mm, 'height': 275 * mm}
        ret_val = createBarcodeDrawing('QR', value=qr_value, **options)
        qrcode_image = base64.encodebytes(ret_val.asString('jpg'))

        cargar_values = {
            'rfc_emisor': Emisor.attrib['Rfc'],
            #'name_emisor' : Emisor.attrib['Nombre'],
            'moneda': xml_data.attrib['Moneda'],
            'invoice_datetime': xml_data.attrib['Fecha'],
            'folio_fiscal' : TimbreFiscalDigital.attrib['UUID'],
            'nomina_cfdi': True,
            'estado_factura': 'factura_correcta',
            'numero_cetificado' : xml_data.attrib['NoCertificado'],
            'cetificaso_sat' : TimbreFiscalDigital.attrib['NoCertificadoSAT'],
            'fecha_certificacion' : TimbreFiscalDigital.attrib['FechaTimbrado'],
            'selo_digital_cdfi' : TimbreFiscalDigital.attrib['SelloCFD'],
            'selo_sat' : TimbreFiscalDigital.attrib['SelloSAT'],
            'version' : TimbreFiscalDigital.attrib['Version'],
            'tipocambio' : xml_data.find('TipoCambio') and xml_data.attrib['TipoCambio'] or '1',
            'moneda': xml_data.attrib['Moneda'],
            'number_folio': xml_data.find('Folio') and xml_data.attrib['Folio'] or ' ',
            'cadena_origenal' : '||%s|%s|%s|%s|%s||' % (TimbreFiscalDigital.attrib['Version'], TimbreFiscalDigital.attrib['UUID'], TimbreFiscalDigital.attrib['FechaTimbrado'],
                                                         TimbreFiscalDigital.attrib['SelloCFD'], TimbreFiscalDigital.attrib['NoCertificadoSAT']),
            'qrcode_image': qrcode_image
            }
        payslip_id.write(cargar_values)

        xml_file_name = payslip_id.number.replace('/','_') + '.xml'
        payslip_id.env['ir.attachment'].sudo().create(
              {
                'name': xml_file_name,
                'datas': self.import_file,
                #'datas_fname': xml_file_name,
                'res_model': payslip_id._name,
                'res_id': payslip_id.id,
                'type': 'binary'
              })

        #xml_file = open(xml_file_link, 'w')
        #xml_invoice = base64.b64decode(self.import_file)
        #xml_file.write(xml_invoice.decode("utf-8"))
        #xml_file.close()

        return True


