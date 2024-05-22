# -*- coding: utf-8 -*-

import base64
import json
import requests
import datetime
from lxml import etree

from odoo import fields, models, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError

from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.lib.units import mm
from . import amount_to_text_es_MX
import pytz
import re
import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    factura_cfdi = fields.Boolean('Factura CFDI')
    tipo_comprobante = fields.Selection(
        selection=[('I', 'Ingreso'),
                   ('E', 'Egreso'),
                   ('T', 'Traslado'),
                   ],
        string=_('Tipo de comprobante'),
    )
    forma_pago_id = fields.Many2one('catalogo.forma.pago', string='Forma de pago')
    methodo_pago = fields.Selection(
        selection=[('PUE', _('Pago en una sola exhibición')),
                   ('PPD', _('Pago en parcialidades o diferido')), ],
        string=_('Método de pago'),
    )
    uso_cfdi_id = fields.Many2one('catalogo.uso.cfdi', string='Uso CFDI (cliente)')
    estado_factura = fields.Selection(
        selection=[('factura_no_generada', 'Factura no generada'), ('factura_correcta', 'Factura correcta'),
                   ('solicitud_cancelar', 'Cancelación en proceso'), ('factura_cancelada', 'Factura cancelada'),
                   ('solicitud_rechazada', 'Cancelación rechazada'), ],
        string=_('Estado de factura'),
        default='factura_no_generada',
        readonly=True
    )
    pdf_cdfi_invoice = fields.Binary("CDFI Invoice")
    qrcode_image = fields.Binary("QRCode")
    numero_cetificado = fields.Char(string=_('Numero de cetificado'))
    cetificaso_sat = fields.Char(string=_('Cetificao SAT'))
    folio_fiscal = fields.Char(string=_('Folio Fiscal'), readonly=True)
    fecha_certificacion = fields.Char(string=_('Fecha y Hora Certificación'))
    cadena_origenal = fields.Char(string=_('Cadena Origenal del Complemento digital de SAT'))
    selo_digital_cdfi = fields.Char(string=_('Selo Digital del CDFI'))
    selo_sat = fields.Char(string=_('Selo del SAT'))
    moneda = fields.Char(string=_('Moneda'))
    tipocambio = fields.Char(string=_('TipoCambio'))
    # folio = fields.Char(string=_('Folio'))
    # version = fields.Char(string=_('Version'))
    number_folio = fields.Char(string=_('Folio'), compute='_get_number_folio')
    amount_to_text = fields.Char('Amount to Text', compute='_get_amount_to_text',
                                 size=256,
                                 help='Amount of the invoice in letter')
    qr_value = fields.Char(string=_('QR Code Value'))
    fecha_factura = fields.Datetime(string=_('Fecha Factura'))
    # serie_emisor = fields.Char(string=_('A'))
    tipo_relacion = fields.Selection(
        selection=[('01', 'Nota de crédito de los documentos relacionados'),
                   ('02', 'Nota de débito de los documentos relacionados'),
                   ('03', 'Devolución de mercancía sobre facturas o traslados previos'),
                   ('04', 'Sustitución de los CFDI previos'),
                   ('05', 'Traslados de mercancías facturados previamente'),
                   ('06', 'Factura generada por los traslados previos'),
                   ('07', 'CFDI por aplicación de anticipo'), ],
        string=_('Tipo relación'),
    )
    uuid_relacionado = fields.Char(string=_('CFDI Relacionado'))
    confirmacion = fields.Char(string=_('Confirmación'))
    total_factura = fields.Float("Total factura")
    subtotal = fields.Float("Subtotal factura")
    discount = fields.Float("Descuento factura")
    facatradquirente = fields.Char(string=_('Fac Atr Adquirente'))
    exportacion = fields.Selection(
        selection=[('01', 'No aplica'),
                   ('02', 'Definitiva'),
                   ('03', 'Temporal'), ],
        string=_('Exportacion'), default='01',
    )
    proceso_timbrado = fields.Boolean(string=_('Proceso de timbrado'))
    tax_payment = fields.Text(string=_('Taxes'))
    factura_global = fields.Boolean('Factura global')
    fg_periodicidad = fields.Selection(
        selection=[('01', '01 - Diario'),
                   ('02', '02 - Semanal'),
                   ('03', '03 - Quincenal'),
                   ('04', '04 - Mensual'),
                   ('05', '05 - Bimestral'), ],
        string=_('Periodicidad'),
    )
    fg_meses = fields.Selection(
        selection=[('01', '01 - Enero'),
                   ('02', '02 - Febrero'),
                   ('03', '03 - Marzo'),
                   ('04', '04 - Abril'),
                   ('05', '05 - Mayo'),
                   ('06', '06 - Junio'),
                   ('07', '07 - Julio'),
                   ('08', '08 - Agosto'),
                   ('09', '09 - Septiembre'),
                   ('10', '10 - Octubre'),
                   ('11', '11 - Noviembre'),
                   ('12', '12 - Diciembre'),
                   ('13', '13 - Enero - Febrero'),
                   ('14', '14 - Marzo - Abril'),
                   ('15', '15 - Mayo - Junio'),
                   ('16', '16 - Julio - Agosto'),
                   ('17', '17 - Septiembre - Octubre'),
                   ('18', '18 - Noviembre - Diciembre'), ],
        string=_('Mes'),
    )
    fg_ano = fields.Char(string=_('Año'))
    tercero_id = fields.Many2one('res.partner', string="A cuenta de terceros")

    @api.model
    def _reverse_moves(self, default_values, cancel=True):
        values = super(AccountMove, self)._reverse_moves(default_values, cancel)
        for inv in self:
           if inv.estado_factura == 'factura_correcta':
               values['uuid_relacionado'] = inv.folio_fiscal
               values['methodo_pago'] = 'PUE'
               values['forma_pago_id'] = inv.forma_pago_id.id
               values['tipo_comprobante'] = 'E'
               values['uso_cfdi_id'] = inv.env['catalogo.uso.cfdi'].sudo().search([('code', '=', 'G02')]).id
               values['tipo_relacion'] = '01'
               values['fecha_factura'] = None
               values['qrcode_image'] = None
               values['numero_cetificado'] = None
               values['cetificaso_sat'] = None
               values['selo_digital_cdfi'] = None
               values['folio_fiscal'] = None
               values['estado_factura'] = 'factura_no_generada'
               values['factura_cfdi'] = False
        return values

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {})
        default['estado_factura'] = 'factura_no_generada'
        default['folio_fiscal'] = ''
        default['factura_cfdi'] = False
        default['fecha_factura'] = None
        default['qrcode_image'] = None
        default['numero_cetificado'] = None
        default['cetificaso_sat'] = None
        default['selo_digital_cdfi'] = None
        default['folio_fiscal'] = None
        return super(AccountMove, self).copy(default=default)

    @api.depends('name')
    def _get_number_folio(self):
        for record in self:
            if record.name:
                record.number_folio = record.name.replace('INV', '').replace('/', '')

    @api.depends('amount_total', 'currency_id')
    def _get_amount_to_text(self):
        for record in self:
            record.amount_to_text = amount_to_text_es_MX.get_amount_to_text(record, record.amount_total, 'es_cheque',
                                                                            record.currency_id.name)

    @api.model
    def _get_amount_2_text(self, amount_total):
        return amount_to_text_es_MX.get_amount_to_text(self, amount_total, 'es_cheque', self.currency_id.name)

    @api.onchange('partner_id')
    def _get_uso_cfdi(self):
        if self.partner_id:
            values = {
                'uso_cfdi_id': self.partner_id.uso_cfdi_id.id
            }
            self.update(values)

    @api.onchange('invoice_payment_term_id')
    def _get_metodo_pago(self):
        if self.invoice_payment_term_id:
            if self.invoice_payment_term_id.methodo_pago == 'PPD':
                values = {
                    'methodo_pago': self.invoice_payment_term_id.methodo_pago,
                    'forma_pago_id': self.env['catalogo.forma.pago'].sudo().search([('code', '=', '99')])
                }
            else:
                values = {
                    'methodo_pago': self.invoice_payment_term_id.methodo_pago,
                    'forma_pago_id': False
                }
        else:
            values = {
                'methodo_pago': False,
                'forma_pago_id': False
            }
        self.update(values)

    @api.model
    def to_json(self):
        self.check_cfdi_values()

        if self.partner_id.vat == 'XAXX010101000' or self.partner_id.vat == 'XEXX010101000':
            zipreceptor = self.journal_id.codigo_postal or self.company_id.zip
            if self.factura_global:
                nombre = 'PUBLICO EN GENERAL'
            else:
                nombre = self.partner_id.name.upper()
        else:
            nombre = self.partner_id.name.upper()
            zipreceptor = self.partner_id.zip

        no_decimales = self.currency_id.no_decimales
        no_decimales_prod = self.currency_id.decimal_places
        no_decimales_tc = self.currency_id.no_decimales_tc

        # corregir hora
        timezone = self._context.get('tz')
        if not timezone:
            timezone = self.journal_id.tz or self.env.user.partner_id.tz or 'America/Mexico_City'
        # timezone = tools.ustr(timezone).encode('utf-8')

        local = pytz.timezone(timezone)
        if not self.fecha_factura:
            naive_from = datetime.datetime.now()
        else:
            naive_from = self.fecha_factura
        local_dt_from = naive_from.replace(tzinfo=pytz.UTC).astimezone(local)
        date_from = local_dt_from.strftime("%Y-%m-%dT%H:%M:%S")
        if not self.fecha_factura:
            self.fecha_factura = datetime.datetime.now()

        if self.currency_id.name == 'MXN':
            tipocambio = 1
        else:
            tipocambio = self.set_decimals(1 / self.currency_id.with_context(date=self.invoice_date).rate,
                                           no_decimales_tc)

        request_params = {
            'factura': {
                'serie': self.journal_id.serie_diario or self.company_id.serie_factura,
                'folio': str(re.sub('[^0-9]','', self.name)),
                'fecha_expedicion': date_from,
                'forma_pago': self.forma_pago_id.code,
                'subtotal': self.amount_untaxed,
                'descuento': 0,
                'moneda': self.currency_id.name,
                'tipocambio': tipocambio,
                'total': self.amount_total,
                'tipocomprobante': self.tipo_comprobante,
                'metodo_pago': self.methodo_pago,
                'LugarExpedicion': self.journal_id.codigo_postal or self.company_id.zip,
                'Confirmacion': self.confirmacion,
                'Exportacion': self.exportacion,
            },
            'emisor': {
                'rfc': self.company_id.vat.upper(),
                'nombre': self.company_id.nombre_fiscal.upper(),
                'RegimenFiscal': self.company_id.regimen_fiscal_id.code,
                'FacAtrAdquirente': self.facatradquirente,
            },
            'receptor': {
                'nombre': nombre,
                'rfc': self.partner_id.vat.upper(),
                'ResidenciaFiscal': self.partner_id.residencia_fiscal,
                'NumRegIdTrib': self.partner_id.registro_tributario,
                'UsoCFDI': self.uso_cfdi_id.code,
                'RegimenFiscalReceptor': self.partner_id.regimen_fiscal_id.code,
                'DomicilioFiscalReceptor': zipreceptor,
            },
            'informacion': {
                'cfdi': '4.0',
                'sistema': 'odoo16',
                'version': '1',
                'api_key': self.company_id.proveedor_timbrado,
                'modo_prueba': self.company_id.modo_prueba,
            },
        }

        if self.factura_global:
            request_params.update({
                'InformacionGlobal': {
                    'Periodicidad': self.fg_periodicidad,
                    'Meses': self.fg_meses,
                    'Año': self.fg_ano,
                },
            })

        if self.uuid_relacionado:
            cfdi_relacionado = []
            uuids = self.uuid_relacionado.replace(' ', '').split(',')
            for uuid in uuids:
                cfdi_relacionado.append({
                    'uuid': uuid,
                })
            request_params.update({'CfdisRelacionados': {'UUID': cfdi_relacionado, 'TipoRelacion': self.tipo_relacion}})

        amount_total = 0.0
        amount_untaxed = 0.0
        self.subtotal = 0
        total = 0
        self.discount = 0
        tras_tot = 0
        ret_tot = 0
        tax_grouped_tras = {}
        tax_grouped_ret = {}
        tax_local_ret = []
        tax_local_tras = []
        tax_local_ret_tot = 0
        tax_local_tras_tot = 0
        only_exento = True
        items = {'numerodepartidas': len(self.invoice_line_ids)}
        invoice_lines = []
        for line in self.invoice_line_ids:
            if not line.product_id or line.display_type in ('line_section', 'line_note'):
                continue

            if not line.product_id.clave_producto:
                self.write({'proceso_timbrado': False})
                self.env.cr.commit()
                raise UserError(_('El producto %s no tiene clave del SAT configurado.') % (line.product_id.name))
            if not line.product_id.cat_unidad_medida.clave:
                self.write({'proceso_timbrado': False})
                self.env.cr.commit()
                raise UserError(
                    _('El producto %s no tiene unidad de medida del SAT configurado.') % (line.product_id.name))

            price_wo_discount = line.price_unit * (1 - (line.discount / 100.0))

            taxes_prod = line.tax_ids.compute_all(price_wo_discount, line.currency_id, line.quantity,
                                                  product=line.product_id, partner=line.move_id.partner_id)
            tax_ret = []
            tax_tras = []
            tax_items = {}
            tax_included = 0
            for taxes in taxes_prod['taxes']:
                tax = self.env['account.tax'].browse(taxes['id'])
                if not tax.impuesto:
                    self.write({'proceso_timbrado': False})
                    self.env.cr.commit()
                    raise UserError(_('El impuesto %s no tiene clave del SAT configurado.') % (tax.name))
                if not tax.tipo_factor:
                    self.write({'proceso_timbrado': False})
                    self.env.cr.commit()
                    raise UserError(_('El impuesto %s no tiene tipo de factor del SAT configurado.') % (tax.name))
                if tax.impuesto != '004':
                    key = taxes['id']
                    if tax.price_include or tax.amount_type == 'division':
                        tax_included += taxes['amount']

                    if taxes['amount'] >= 0.0:
                        if tax.tipo_factor == 'Exento':
                            tax_tras.append({'Base': self.set_decimals(taxes['base'], no_decimales_prod),
                                             'Impuesto': tax.impuesto,
                                             'TipoFactor': tax.tipo_factor, })
                        elif tax.tipo_factor == 'Cuota':
                            only_exento = False
                            tax_tras.append({'Base': self.set_decimals(line.quantity, no_decimales_prod),
                                             'Impuesto': tax.impuesto,
                                             'TipoFactor': tax.tipo_factor,
                                             'TasaOCuota': self.set_decimals(tax.amount, 6),
                                             'Importe': self.set_decimals(taxes['amount'], no_decimales_prod), })
                        else:
                            only_exento = False
                            tax_tras.append({'Base': self.set_decimals(taxes['base'], no_decimales_prod),
                                             'Impuesto': tax.impuesto,
                                             'TipoFactor': tax.tipo_factor,
                                             'TasaOCuota': self.set_decimals(tax.amount / 100.0, 6),
                                             'Importe': self.set_decimals(taxes['amount'], no_decimales_prod), })
                        tras_tot += taxes['amount']
                        val = {'tax_id': taxes['id'],
                               'base': taxes['base'] if tax.tipo_factor != 'Cuota' else line.quantity,
                               'amount': taxes['amount'], }
                        if key not in tax_grouped_tras:
                            tax_grouped_tras[key] = val
                        else:
                            tax_grouped_tras[key]['base'] += val[
                                'base'] if tax.tipo_factor != 'Cuota' else line.quantity
                            tax_grouped_tras[key]['amount'] += val['amount']
                    else:
                        tax_ret.append({'Base': self.set_decimals(taxes['base'], no_decimales_prod),
                                        'Impuesto': tax.impuesto,
                                        'TipoFactor': tax.tipo_factor,
                                        'TasaOCuota': self.set_decimals(tax.amount / 100.0 * -1, 6),
                                        'Importe': self.set_decimals(taxes['amount'] * -1, no_decimales_prod), })
                        ret_tot += taxes['amount'] * -1
                        val = {'tax_id': taxes['id'],
                               'base': taxes['base'],
                               'amount': taxes['amount'], }
                        if key not in tax_grouped_ret:
                            tax_grouped_ret[key] = val
                        else:
                            tax_grouped_ret[key]['base'] += val['base']
                            tax_grouped_ret[key]['amount'] += val['amount']
                else:  # impuestos locales
                    if tax.price_include or tax.amount_type == 'division':
                        tax_included += taxes['amount']
                    if taxes['amount'] >= 0.0:
                        tax_local_tras_tot += taxes['amount']
                        tax_local_tras.append({'ImpLocTrasladado': tax.impuesto_local,
                                               'TasadeTraslado': self.set_decimals(tax.amount, 2),
                                               'Importe': self.set_decimals(taxes['amount'], 2), })
                    else:
                        tax_local_ret_tot += taxes['amount']
                        tax_local_ret.append({'ImpLocRetenido': tax.impuesto_local,
                                              'TasadeRetencion': self.set_decimals(tax.amount * -1, 2),
                                              'Importe': self.set_decimals(taxes['amount'] * -1, 2), })

            if line.discount != 100:
               if tax_tras:
                   tax_items.update({'Traslados': tax_tras})
               if tax_ret:
                   tax_items.update({'Retenciones': tax_ret})
            else:
               tax_tras = []
               tax_ret = []

            total_wo_discount = round(line.price_unit * line.quantity - tax_included, no_decimales_prod)
            discount_prod = round(total_wo_discount - line.price_subtotal, no_decimales_prod) if line.discount else 0
            precio_unitario = round(total_wo_discount / line.quantity, no_decimales_prod)
            self.subtotal += total_wo_discount
            self.discount += discount_prod

            pedimentos = []
            if line.pedimento:
                pedimento_list = line.pedimento.replace(' ', '').split(',')
                for pedimento in pedimento_list:
                    if len(pedimento) != 15:
                        self.write({'proceso_timbrado': False})
                        self.env.cr.commit()
                        raise UserError(_('La longitud del pedimento debe ser de 15 dígitos.'))
                    pedimentos.append({'NumeroPedimento': pedimento[0:2] + '  ' + pedimento[2:4] + '  ' + pedimento[
                                                                                                          4:8] + '  ' + pedimento[
                                                                                                                        8:]})

            terceros = {}
            if self.tercero_id:
                terceros.update({'rfc': self.tercero_id.vat.upper(), 
                                 'nombre': self.tercero_id.name.upper(), 
                                 'regimen': self.tercero_id.regimen_fiscal_id.code,
                                 'domicilio': self.tercero_id.zip })

            components = []
            if line.product_id.product_parts_ids:
                for component in line.product_id.product_parts_ids:
                    components.append({'ClaveProdServ': component.product_id.clave_producto,
                                      'Cantidad': component.cantidad,
                                      'Descripcion': self.clean_text(component.product_id.name),
                                      })

            if line.product_id.objetoimp:
                objetoimp = line.product_id.objetoimp
            else:
                _logger.info('taxes_prod %s', taxes_prod)
                if taxes_prod['taxes']:
                  if tax_tras or tax_ret:
                     objetoimp = '02'
                  else:
                     objetoimp = '04'
                else:
                   objetoimp = '01'

            product_string = line.product_id.code and line.product_id.code[:100] or ''
            if product_string == '':
                if line.name.find(']') > 0:
                    product_string = line.name[line.name.find('[') + len('['):line.name.find(']')] or ''
            description = line.name
            if line.name.find(']') > 0:
                description = line.name[line.name.find(']') + 2:]

            if self.tipo_comprobante == 'T':
                invoice_lines.append({'cantidad': self.set_decimals(line.quantity, 6),
                                      'unidad': line.product_id.cat_unidad_medida.descripcion,
                                      'NoIdentificacion': self.clean_text(product_string),
                                      'valorunitario': self.set_decimals(precio_unitario, no_decimales_prod),
                                      'importe': self.set_decimals(total_wo_discount, no_decimales_prod),
                                      'descripcion': self.clean_text(description),
                                      'ClaveProdServ': line.product_id.clave_producto,
                                      'ObjetoImp': objetoimp,
                                      'ClaveUnidad': line.product_id.cat_unidad_medida.clave})
            else:
                invoice_lines.append({'cantidad': self.set_decimals(line.quantity, 6),
                                      'unidad': line.product_id.cat_unidad_medida.descripcion,
                                      'NoIdentificacion': self.clean_text(product_string),
                                      'valorunitario': self.set_decimals(precio_unitario, no_decimales_prod),
                                      'importe': self.set_decimals(total_wo_discount, no_decimales_prod),
                                      'descripcion': self.clean_text(description),
                                      'ClaveProdServ': line.product_id.clave_producto,
                                      'ClaveUnidad': line.product_id.cat_unidad_medida.clave,
                                      'Impuestos': tax_items and tax_items or '',
                                      'Descuento': self.set_decimals(discount_prod, no_decimales_prod),
                                      'ObjetoImp': objetoimp,
                                      'InformacionAduanera': pedimentos and pedimentos or '',
                                      'predial': line.predial and line.predial or '',
                                      'terceros': terceros and terceros or '',
                                      'parte': components and components or '',})

        self.discount = round(self.discount, no_decimales)
        self.subtotal = self.roundTraditional(self.subtotal, no_decimales)
        impuestos = {}
        #if objetoimp != '04':
        if tax_grouped_tras or tax_grouped_ret:
               tras_tot = round(tras_tot, no_decimales)
               ret_tot = round(ret_tot, no_decimales)
               retenciones = []
               traslados = []
               if tax_grouped_tras:
                   for line in tax_grouped_tras.values():
                       tax = self.env['account.tax'].browse(line['tax_id'])
                       if tax.tipo_factor == 'Exento':
                           tasa_tr = ''
                       elif tax.tipo_factor == 'Cuota':
                           tasa_tr = self.set_decimals(tax.amount, 6)
                       else:
                           tasa_tr = self.set_decimals(tax.amount / 100.0, 6)
                       traslados.append({'impuesto': tax.impuesto,
                                         'TipoFactor': tax.tipo_factor,
                                         'tasa': tasa_tr,
                                         'importe': self.roundTraditional(line['amount'],no_decimales) if tax.tipo_factor != 'Exento' else '',
                                         'base': self.roundTraditional(line['base'], no_decimales),
                                         'tax_id': line['tax_id'],
                                         })
                   impuestos.update(
                       {'translados': traslados, 'TotalImpuestosTrasladados': self.set_decimals(tras_tot, no_decimales) if not only_exento else ''})
               if tax_grouped_ret:
                   for line in tax_grouped_ret.values():
                       tax = self.env['account.tax'].browse(line['tax_id'])
                       retenciones.append({'impuesto': tax.impuesto,
                                           'TipoFactor': tax.tipo_factor,
                                           'tasa': self.set_decimals(float(tax.amount) / 100.0 * -1, 6),
                                           'importe': self.roundTraditional(line['amount'] * -1, no_decimales),
                                           'base': self.roundTraditional(line['base'], no_decimales),
                                           'tax_id': line['tax_id'],
                                           })
                   impuestos.update(
                       {'retenciones': retenciones, 'TotalImpuestosRetenidos': self.set_decimals(ret_tot, no_decimales)})
               request_params.update({'impuestos': impuestos})
        self.tax_payment = json.dumps(impuestos)

        tax_local_tras_tot = round(tax_local_tras_tot, no_decimales)
        tax_local_ret_tot = round(tax_local_ret_tot, no_decimales)
        if tax_local_ret or tax_local_tras:
            if tax_local_tras and not tax_local_ret:
                request_params.update({'implocal10': {'TotaldeTraslados': self.roundTraditional(tax_local_tras_tot, 2),
                                                      'TotaldeRetenciones': self.roundTraditional(tax_local_ret_tot, 2),
                                                      'TrasladosLocales': tax_local_tras, }})
            if tax_local_ret and not tax_local_tras:
                request_params.update({'implocal10': {'TotaldeTraslados': self.roundTraditional(tax_local_tras_tot, 2),
                                                      'TotaldeRetenciones': self.roundTraditional(tax_local_ret_tot * -1,
                                                                                              2),
                                                      'RetencionesLocales': tax_local_ret, }})
            if tax_local_ret and tax_local_tras:
                request_params.update({'implocal10': {'TotaldeTraslados': self.roundTraditional(tax_local_tras_tot, 2),
                                                      'TotaldeRetenciones': self.roundTraditional(tax_local_ret_tot * -1,
                                                                                              2),
                                                      'TrasladosLocales': tax_local_tras,
                                                      'RetencionesLocales': tax_local_ret, }})

        if self.tipo_comprobante == 'T':
            request_params['factura'].update({'descuento': '', 'subtotal': '0.00','total': '0.00'})
            self.total_factura = 0
        else:
            self.total_factura = round(
                self.subtotal + tras_tot - ret_tot - self.discount + tax_local_ret_tot + tax_local_tras_tot, 2)
            request_params['factura'].update({'descuento': self.roundTraditional(self.discount, no_decimales),
                                              'subtotal': self.roundTraditional(self.subtotal, no_decimales),
                                              'total': self.roundTraditional(self.total_factura, no_decimales)})

        request_params.update({'conceptos': invoice_lines})

        return request_params

    def set_decimals(self, amount, precision):
        if amount is None or amount is False:
            return None
        return '%.*f' % (precision, amount)

    def roundTraditional(self, val, digits):
       if val != 0:
          return round(val + 10 ** (-len(str(val)) - 1), digits)
       else:
          return 0

    def clean_text(self, text):
        clean_text = text.replace('\n', ' ').replace('\\', ' ').replace('-', ' ').replace('/', ' ').replace('|', ' ')
        clean_text = clean_text.replace(',', ' ').replace(';', ' ').replace('>', ' ').replace('<', ' ')
        return clean_text[:1000]

    def check_cfdi_values(self):
        if not self.company_id.vat:
            self.write({'proceso_timbrado': False})
            self.env.cr.commit()
            raise UserError(_('El emisor no tiene RFC configurado.'))
        if not self.company_id.name:
            self.write({'proceso_timbrado': False})
            self.env.cr.commit()
            raise UserError(_('El emisor no tiene nombre configurado.'))
        if not self.partner_id.vat:
            self.write({'proceso_timbrado': False})
            self.env.cr.commit()
            raise UserError(_('El receptor no tiene RFC configurado.'))
        if not self.partner_id.name:
            self.write({'proceso_timbrado': False})
            self.env.cr.commit()
            raise UserError(_('El receptor no tiene nombre configurado.'))
        if not self.uso_cfdi_id:
            self.write({'proceso_timbrado': False})
            self.env.cr.commit()
            raise UserError(_('La factura no tiene uso de cfdi configurado.'))
        if not self.tipo_comprobante:
            self.write({'proceso_timbrado': False})
            self.env.cr.commit()
            raise UserError(_('El emisor no tiene tipo de comprobante configurado.'))
        if self.tipo_comprobante != 'T' and not self.methodo_pago:
            self.write({'proceso_timbrado': False})
            self.env.cr.commit()
            raise UserError(_('La factura no tiene método de pago configurado.'))
        if self.tipo_comprobante != 'T' and not self.forma_pago_id:
            self.write({'proceso_timbrado': False})
            self.env.cr.commit()
            raise UserError(_('La factura no tiene forma de pago configurado.'))
        if not self.company_id.regimen_fiscal_id:
            self.write({'proceso_timbrado': False})
            self.env.cr.commit()
            raise UserError(_('El emisor no régimen fiscal configurado.'))
        if not self.journal_id.codigo_postal and not self.company_id.zip:
            self.write({'proceso_timbrado': False})
            self.env.cr.commit()
            raise UserError(_('El emisor no tiene código postal configurado.'))

    def _set_data_from_xml(self, xml_invoice):
        if not xml_invoice:
            return None
        NSMAP = {
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'cfdi': 'http://www.sat.gob.mx/cfd/4',
            'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital',
        }

        xml_data = etree.fromstring(xml_invoice)
        Complemento = xml_data.find('cfdi:Complemento', NSMAP)
        TimbreFiscalDigital = Complemento.find('tfd:TimbreFiscalDigital', NSMAP)

        self.total_factura = xml_data.attrib['Total']
        self.tipocambio = xml_data.attrib['TipoCambio']
        self.moneda = xml_data.attrib['Moneda']
        self.numero_cetificado = xml_data.attrib['NoCertificado']
        self.cetificaso_sat = TimbreFiscalDigital.attrib['NoCertificadoSAT']
        self.fecha_certificacion = TimbreFiscalDigital.attrib['FechaTimbrado']
        self.selo_digital_cdfi = TimbreFiscalDigital.attrib['SelloCFD']
        self.selo_sat = TimbreFiscalDigital.attrib['SelloSAT']
        self.folio_fiscal = TimbreFiscalDigital.attrib['UUID']
        version = TimbreFiscalDigital.attrib['Version']
        self.cadena_origenal = '||%s|%s|%s|%s|%s||' % (version, self.folio_fiscal, self.fecha_certificacion,
                                                       self.selo_digital_cdfi, self.cetificaso_sat)

        options = {'width': 275 * mm, 'height': 275 * mm}
        amount_str = str(self.amount_total).split('.')
        qr_value = 'https://verificacfdi.facturaelectronica.sat.gob.mx/default.aspx?&id=%s&re=%s&rr=%s&tt=%s.%s&fe=%s' % (
            self.folio_fiscal,
            self.company_id.vat,
            self.partner_id.vat,
            amount_str[0].zfill(10),
            amount_str[1].ljust(6, '0'),
            self.selo_digital_cdfi[-8:],
        )
        self.qr_value = qr_value
        ret_val = createBarcodeDrawing('QR', value=qr_value, **options)
        self.qrcode_image = base64.encodebytes(ret_val.asString('jpg'))

    def action_cfdi_generate(self):
        # after validate, send invoice data to external system via http post
        for invoice in self:
            if invoice.proceso_timbrado:
                raise UserError(_('El intento de timbrado previo terminó con un error, revise que todo esté correcto o envíe el código de error para su revisión. \
Si requiere timbrar la factura nuevamente deshabilite el checkbox de "Proceso de timbrado" de la pestaña CFDI.'))
            else:
                invoice.write({'proceso_timbrado': True})
                self.env.cr.commit()
            if invoice.estado_factura == 'factura_correcta':
                if invoice.folio_fiscal:
                    invoice.write({'factura_cfdi': True})
                    return True
                else:
                    invoice.write({'proceso_timbrado': False})
                    self.env.cr.commit()
                    raise UserError(_('Error para timbrar factura, Factura ya generada.'))
            if invoice.estado_factura == 'factura_cancelada':
                invoice.write({'proceso_timbrado': False})
                self.env.cr.commit()
                raise UserError(_('Error para timbrar factura, Factura ya generada y cancelada.'))

            values = invoice.to_json()
            if invoice.company_id.proveedor_timbrado == 'multifactura':
                url = '%s' % ('http://facturacion.itadmin.com.mx/api/invoice')
            elif invoice.company_id.proveedor_timbrado == 'multifactura2':
                url = '%s' % ('http://facturacion2.itadmin.com.mx/api/invoice')
            elif invoice.company_id.proveedor_timbrado == 'multifactura3':
                url = '%s' % ('http://facturacion3.itadmin.com.mx/api/invoice')
            elif invoice.company_id.proveedor_timbrado == 'gecoerp':
                if self.company_id.modo_prueba:
                    url = '%s' % ('https://itadmin.gecoerp.com/invoice/?handler=OdooHandler33')
                else:
                    url = '%s' % ('https://itadmin.gecoerp.com/invoice/?handler=OdooHandler33')
            else:
                invoice.write({'proceso_timbrado': False})
                self.env.cr.commit()
                raise UserError(
                    _('Error, falta seleccionar el servidor de timbrado en la configuración de la compañía.'))

            try:
                response = requests.post(url,
                                         auth=None, verify=False, data=json.dumps(values),
                                         headers={"Content-type": "application/json"})
            except Exception as e:
                error = str(e)
                invoice.write({'proceso_timbrado': False})
                self.env.cr.commit()
                if "Name or service not known" in error or "Failed to establish a new connection" in error:
                    raise UserError(_("No se pudo conectar con el servidor."))
                else:
                    raise UserError(_(error))

            if "Whoops, looks like something went wrong." in response.text:
                invoice.write({'proceso_timbrado': False})
                self.env.cr.commit()
                raise UserError(_(
                    "Error en el proceso de timbrado, espere un minuto y vuelva a intentar timbrar nuevamente. \nSi el error aparece varias veces reportarlo con la persona de sistemas."))
            else:
                json_response = response.json()
            estado_factura = json_response['estado_factura']
            if estado_factura == 'problemas_factura':
                invoice.write({'proceso_timbrado': False})
                self.env.cr.commit()
                raise UserError(_(json_response['problemas_message']))
            # Receive and stroe XML invoice
            if json_response.get('factura_xml'):
                invoice._set_data_from_xml(base64.b64decode(json_response['factura_xml']))
                file_name = invoice.name.replace('/', '_') + '.xml'
                self.env['ir.attachment'].sudo().create(
                    {
                        'name': file_name,
                        'datas': json_response['factura_xml'],
                        # 'datas_fname': file_name,
                        'res_model': self._name,
                        'res_id': invoice.id,
                        'type': 'binary'
                    })

            invoice.write({'estado_factura': estado_factura,
                           'factura_cfdi': True,
                           'proceso_timbrado': False})
            invoice.message_post(body="CFDI emitido")
        return True

    def action_cfdi_cancel(self):
        for invoice in self:
            if invoice.factura_cfdi:
                if invoice.estado_factura == 'factura_cancelada':
                    pass
                    # raise UserError(_('La factura ya fue cancelada, no puede volver a cancelarse.'))
                if not invoice.company_id.contrasena:
                    raise UserError(_('El campo de contraseña de los certificados está vacío.'))
                domain = [
                    ('res_id', '=', invoice.id),
                    ('res_model', '=', invoice._name),
                    ('name', '=', invoice.name.replace('/', '_') + '.xml')]
                xml_file = self.env['ir.attachment'].search(domain)
                if not xml_file:
                    raise UserError(_('No se encontró el archivo XML para enviar a cancelar.'))
                values = {
                    'rfc': invoice.company_id.vat,
                    'api_key': invoice.company_id.proveedor_timbrado,
                    'uuid': invoice.folio_fiscal,
                    'folio': invoice.name.replace('INV', '').replace('/', ''),
                    'serie_factura': invoice.journal_id.serie_diario or invoice.company_id.serie_factura,
                    'modo_prueba': invoice.company_id.modo_prueba,
                    'certificados': {
                        #    'archivo_cer': archivo_cer.decode("utf-8"),
                        #    'archivo_key': archivo_key.decode("utf-8"),
                        'contrasena': invoice.company_id.contrasena,
                    },
                    'xml': xml_file[0].datas.decode("utf-8"),
                    'motivo': self.env.context.get('motivo_cancelacion', '02'),
                    'foliosustitucion': self.env.context.get('foliosustitucion', ''),
                }
                if self.company_id.proveedor_timbrado == 'multifactura':
                    url = '%s' % ('http://facturacion.itadmin.com.mx/api/refund')
                elif invoice.company_id.proveedor_timbrado == 'multifactura2':
                    url = '%s' % ('http://facturacion2.itadmin.com.mx/api/refund')
                elif invoice.company_id.proveedor_timbrado == 'multifactura3':
                    url = '%s' % ('http://facturacion3.itadmin.com.mx/api/refund')
                elif self.company_id.proveedor_timbrado == 'gecoerp':
                    if self.company_id.modo_prueba:
                        url = '%s' % ('https://itadmin.gecoerp.com/refund/?handler=OdooHandler33')
                    else:
                        url = '%s' % ('https://itadmin.gecoerp.com/refund/?handler=OdooHandler33')
                else:
                    raise UserError(
                        _('Error, falta seleccionar el servidor de timbrado en la configuración de la compañía.'))

                try:
                    response = requests.post(url,
                                             auth=None, verify=False, data=json.dumps(values),
                                             headers={"Content-type": "application/json"})
                except Exception as e:
                    error = str(e)
                    if "Name or service not known" in error or "Failed to establish a new connection" in error:
                        raise UserError(_("No se pudo conectar con el servidor."))
                    else:
                        raise UserError(_(error))

                if "Whoops, looks like something went wrong." in response.text:
                    raise UserError(_(
                        "Error en el proceso de timbrado, espere un minuto y vuelva a intentar timbrar nuevamente. \nSi el error aparece varias veces reportarlo con la persona de sistemas."))

                json_response = response.json()

                log_msg = ''
                if json_response['estado_factura'] == 'problemas_factura':
                    raise UserError(_(json_response['problemas_message']))
                elif json_response['estado_factura'] == 'solicitud_cancelar':
                    log_msg = "Se solicitó cancelación de CFDI"
                elif json_response.get('factura_xml', False):
                    file_name = 'CANCEL_' + invoice.name.replace('/', '_') + '.xml'
                    self.env['ir.attachment'].sudo().create(
                        {
                            'name': file_name,
                            'datas': json_response['factura_xml'],
                            # 'datas_fname': file_name,
                            'res_model': self._name,
                            'res_id': invoice.id,
                            'type': 'binary'
                        })
                    log_msg = "CFDI Cancelado"
                invoice.write({'estado_factura': json_response['estado_factura']})
                invoice.message_post(body=log_msg)

    def force_invoice_send(self):
        for inv in self:
            email_act = inv.action_invoice_sent()
            if email_act and email_act.get('context'):
                email_ctx = email_act['context']
                email_ctx.update(default_email_from=inv.company_id.email)
                inv.with_context(email_ctx).message_post_with_template(email_ctx.get('default_template_id'))
        return True

    @api.model
    def check_cancel_status_by_cron(self):
        domain = [('move_type', 'in', ('out_invoice', 'out_refund')), ('estado_factura', '=', 'solicitud_cancelar')]
        invoices = self.search(domain, order='id')
        for invoice in invoices:
            _logger.info('Solicitando estado de factura %s', invoice.folio_fiscal)
            domain = [
                ('res_id', '=', invoice.id),
                ('res_model', '=', invoice._name),
                ('name', '=', invoice.name.replace('/', '_') + '.xml')]
            xml_file = self.env['ir.attachment'].search(domain, limit=1)
            if not xml_file:
                _logger.info('No se encontró XML de la factura %s', invoice.folio_fiscal)
                continue
            values = {
                'rfc': invoice.company_id.vat,
                'api_key': invoice.company_id.proveedor_timbrado,
                'modo_prueba': invoice.company_id.modo_prueba,
                'uuid': invoice.folio_fiscal,
                'xml': xml_file.datas.decode("utf-8"),
            }

            if invoice.company_id.proveedor_timbrado == 'multifactura':
                url = '%s' % ('http://facturacion.itadmin.com.mx/api/consulta-cacelar')
            elif invoice.company_id.proveedor_timbrado == 'multifactura2':
                url = '%s' % ('http://facturacion2.itadmin.com.mx/api/consulta-cacelar')
            elif invoice.company_id.proveedor_timbrado == 'multifactura3':
                url = '%s' % ('http://facturacion3.itadmin.com.mx/api/consulta-cacelar')
            elif invoice.company_id.proveedor_timbrado == 'gecoerp':
                url = '%s' % ('http://facturacion.itadmin.com.mx/api/consulta-cacelar')
            else:
                raise UserError(
                    _('Error, falta seleccionar el servidor de timbrado en la configuración de la compañía.'))

            try:
                response = requests.post(url,
                                         auth=None, verify=False, data=json.dumps(values),
                                         headers={"Content-type": "application/json"})

                if "Whoops, looks like something went wrong." in response.text:
                    _logger.info(
                        "Error con el servidor de facturación, favor de reportar el error a su persona de soporte.")
                    return

                json_response = response.json()
                # _logger.info('something ... %s', response.text)
            except Exception as e:
                _logger.info('log de la exception ... %s', response.text)
                json_response = {}
            if not json_response:
                return
            estado_factura = json_response['estado_consulta']
            if estado_factura == 'problemas_consulta':
                _logger.info('Error en la consulta %s', json_response['problemas_message'])
            elif estado_factura == 'consulta_correcta':
                if json_response['factura_xml'] == 'Cancelado':
#                    _logger.info('Factura cancelada')
#                    _logger.info('EsCancelable: %s', json_response['escancelable'])
#                    _logger.info('EstatusCancelacion: %s', json_response['estatuscancelacion'])
                    invoice.action_cfdi_cancel()
                elif json_response['factura_xml'] == 'Vigente':
#                    _logger.info('Factura vigente')
#                    _logger.info('EsCancelable: %s', json_response['escancelable'])
#                    _logger.info('EstatusCancelacion: %s', json_response['estatuscancelacion'])
                    if json_response['estatuscancelacion'] == 'Solicitud rechazada':
                        invoice.estado_factura = 'solicitud_rechazada'
                    if not json_response['estatuscancelacion']:
                        invoice.estado_factura = 'solicitud_rechazada'
            else:
                _logger.info('Error... %s', response.text)
            self.env.cr.commit()
        return True

    def action_cfdi_rechazada(self):
        for invoice in self:
            if invoice.factura_cfdi:
                if invoice.estado_factura == 'solicitud_rechazada' or invoice.estado_factura == 'solicitud_cancelar':
                    invoice.estado_factura = 'factura_correcta'
                    # raise UserError(_('La factura ya fue cancelada, no puede volver a cancelarse.'))

    def liberar_cfdi(self):
        for invoice in self:
            values = {
                'command': 'liberar_cfdi',
                'rfc': invoice.company_id.vat,
                'folio': str(re.sub('[^0-9]','', invoice.name)),
                'serie_factura': invoice.journal_id.serie_diario or invoice.company_id.serie_factura,
                'archivo_cer': invoice.company_id.archivo_cer.decode("utf-8"),
                'archivo_key': invoice.company_id.archivo_key.decode("utf-8"),
                'contrasena': invoice.company_id.contrasena,
            }
            url = ''
            if invoice.company_id.proveedor_timbrado == 'multifactura':
                url = '%s' % ('http://facturacion.itadmin.com.mx/api/command')
            elif invoice.company_id.proveedor_timbrado == 'multifactura2':
                url = '%s' % ('http://facturacion2.itadmin.com.mx/api/command')
            elif invoice.company_id.proveedor_timbrado == 'multifactura3':
                url = '%s' % ('http://facturacion3.itadmin.com.mx/api/command')
            if not url:
                return
            try:
                response = requests.post(url, auth=None, verify=False, data=json.dumps(values),
                                         headers={"Content-type": "application/json"})

                if "Whoops, looks like something went wrong." in response.text:
                    raise UserError(_(
                        "Error con el servidor de facturación, favor de reportar el error a su persona de soporte."))

                json_response = response.json()
            except Exception as e:
                print(e)
                json_response = {}

            if not json_response:
                return
            # _logger.info('something ... %s', response.text)

            respuesta = json_response['respuesta']
            message_id = self.env['mymodule.message.wizard'].create({'message': respuesta})
            return {
                'name': 'Respuesta',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard',
                'res_id': message_id.id,
                'target': 'new'
            }

class MailTemplate(models.Model):
    "Templates for sending email"
    _inherit = 'mail.template'

    def generate_email(self, res_ids, fields=None):
        multi_mode = True
        if isinstance(res_ids, (int)):
            res_ids = [res_ids]
            multi_mode = False
        results = super(MailTemplate, self).generate_email(res_ids, fields=fields)

        for lang, (template, template_res_ids) in self._classify_per_lang(res_ids).items():
            if template.report_template and template.report_template.report_name == 'account.report_invoice_with_payments' or template.report_template.report_name == 'account.report_invoice':
                for res_id in template_res_ids:
                    invoice = self.env[template.model].browse(res_id)
                    if not invoice.factura_cfdi:
                        continue
                    if invoice.estado_factura == 'factura_correcta' or invoice.estado_factura == 'solicitud_cancelar':
                        domain = [
                            ('res_id', '=', invoice.id),
                            ('res_model', '=', invoice._name),
                            ('name', '=', invoice.name.replace('/', '_') + '.xml')]
                        xml_file = self.env['ir.attachment'].search(domain, limit=1)
                        attachments = results[res_id]['attachments'] or []
                        if xml_file:
                            attachments.append(('CFDI_' + invoice.name.replace('/', '_') + '.xml', xml_file.datas))
                    else:
                        domain = [
                            ('res_id', '=', invoice.id),
                            ('res_model', '=', invoice._name),
                            ('name', '=', 'CANCEL_' + invoice.name.replace('/', '_') + '.xml')]
                        xml_file = self.env['ir.attachment'].search(domain, limit=1)
                        attachments = []
                        if xml_file:
                            attachments.append(
                                ('CFDI_CANCEL_' + invoice.name.replace('/', '_') + '.xml', xml_file.datas))
                    results[res_id]['attachments'] = attachments
        return multi_mode and results or results[res_ids[0]]


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    pedimento = fields.Char('Pedimento')
    predial = fields.Char('No. Predial')


class MyModuleMessageWizard(models.TransientModel):
    _name = 'mymodule.message.wizard'
    _description = "Show Message"

    message = fields.Text('Message', required=True)

    #    @api.multi
    def action_close(self):
        return {'type': 'ir.actions.act_window_close'}

