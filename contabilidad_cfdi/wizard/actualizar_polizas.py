# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class ActualizarPolizas(models.TransientModel):
    _name = 'actualizar.polizas'
    _description = "Actualizar polizas"
    
    fecha_inicio = fields.Date('Fecha inicio')
    fecha_fin = fields.Date('Fecha fin')
    polizas_de_facturas_de_cliente = fields.Boolean('Facturas / NC de cliente')
    polizas_de_facturas_de_proveedor = fields.Boolean('Facturas / NC de proveedor')
    polizas_de_facturas_de_pagos = fields.Boolean('Polizas de pagos')

    def action_validar_actualizar_polizas(self):
        if self.polizas_de_facturas_de_cliente:
            invoices = self.env['account.move'].search([('invoice_date','>=',self.fecha_inicio),
                                                           ('invoice_date','<=', self.fecha_fin),
                                                           ('estado_factura','=','factura_correcta'),
                                                           ('state','in', ['open', 'paid']),
                                                           ('type', 'in', ['out_invoice', 'out_refund'])])
            cfdi_obj = self.env['account.move.cfdi33']
            for inv in invoices:
                move_lines = inv.move_id.line_ids.filtered(lambda x:x.name=='/')
                for line in move_lines:
                    cfdi_data = {'fecha': inv.date_invoice, 
                                 'folio': inv.folio, 
                                 'uuid': inv.folio_fiscal, 
                                 'partner_id': inv.partner_id.id, 
                                 'monto': inv.amount_total, 
                                 'moneda': inv.moneda, 
                                'tipocamb': inv.tipocambio, 
                                'rfc_cliente': inv.partner_id.vat
                                }
                    if line.account_cfdi_ids: # overwrite existing data
                        line.account_cfdi_ids[0].write(cfdi_data)
                    else:
                        cfdi_data['move_line_id'] = line.id
                        cfdi_obj.create(cfdi_data)

        if self.polizas_de_facturas_de_proveedor:
            invoices = self.env['account.move'].search([('invoice_date','>=',self.fecha_inicio),
                                                           ('invoice_date','<=', self.fecha_fin),
                                                           ('estado_factura','=','factura_correcta'),
                                                           ('state','in', ['open', 'paid']),
                                                           ('type', 'in', ['in_invoice', 'in_refund'])])
            cfdi_obj = self.env['account.move.cfdi33']
            for inv in invoices:
                move_lines = inv.move_id.line_ids.filtered(lambda x:x.name=='/')
                for line in move_lines:
                    cfdi_data = {'fecha': inv.date_invoice, 
                                 'folio': inv.folio, 
                                 'uuid': inv.folio_fiscal, 
                                 'partner_id': inv.partner_id.id, 
                                 'monto': inv.amount_total, 
                                 'moneda': inv.moneda, 
                                 'tipocamb': inv.tipocambio, 
                                 'rfc_cliente': inv.partner_id.vat
                                 }
                    if line.account_cfdi_ids: # overwrite existing data
                        line.account_cfdi_ids[0].write(cfdi_data)
                    else:
                        cfdi_data['move_line_id'] = line.id
                        cfdi_obj.create(cfdi_data)

        if self.polizas_de_facturas_de_pagos:
            payments = self.env['account.payment'].search([('payment_date','>=',self.fecha_inicio),
                                                            ('payment_date','<=', self.fecha_fin),
                                                            ('estado_pago','=','pago_correcto'),
                                                            ('state','not in', ['draft', 'cancelled'])
                                                            ])
             #effectively paid
            cfdi_obj = self.env['account.move.cfdi33']
            for payment in payments:
                effective_pay = self.env['account.move'].search([('name','=',payment.move_name)],limit=1)
                if effective_pay:
                      move_lines = effective_pay.line_ids[0]
                      cfdi_data = {'fecha': payment.payment_date, 
                                 'folio': payment.folio, 
                                 'uuid': payment.folio_fiscal, 
                                 'partner_id': payment.partner_id.id, 
                                 'monto': payment.amount, 
                                 'moneda': payment.monedap, 
                                 'tipocamb': payment.tipocambiop, 
                                 'rfc_cliente': payment.partner_id.vat
                                 }
                      if move_lines.account_cfdi_ids: # overwrite existing data
                          move_lines.account_cfdi_ids[0].write(cfdi_data)
                      else:
                          cfdi_data['move_line_id'] = move_lines.id
                          cfdi_obj.create(cfdi_data)

        return True
