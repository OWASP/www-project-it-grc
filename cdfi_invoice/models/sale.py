# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from  . import amount_to_text_es_MX
import pytz
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    forma_pago_id  =  fields.Many2one('catalogo.forma.pago', string='Forma de pago')
    #num_cta_pago = fields.Char(string=_('Núm. Cta. Pago'))
    methodo_pago = fields.Selection(
        selection=[('PUE', _('Pago en una sola exhibición')),
                   ('PPD', _('Pago en parcialidades o diferido')),],
        string=_('Método de pago'), 
    )
    uso_cfdi_id  =  fields.Many2one('catalogo.uso.cfdi', string='Uso CFDI (cliente)')
    fecha_corregida = fields.Datetime(string=_('Fecha Cotizacion'), compute='_get_fecha_corregida')

    @api.onchange('partner_id')
    def _get_uso_cfdi(self):
        if self.partner_id:
            values = {
                'uso_cfdi_id': self.partner_id.uso_cfdi_id.id
                }
            self.update(values)

    @api.onchange('payment_term_id')
    def _get_metodo_pago(self):
        if self.payment_term_id:
            if self.payment_term_id.methodo_pago == 'PPD':
                values = {
                 'methodo_pago': self.payment_term_id.methodo_pago,
                 'forma_pago_id': self.env['catalogo.forma.pago'].sudo().search([('code','=','99')])
             }
            else:
                values = {
                 'methodo_pago': self.payment_term_id.methodo_pago,
                 'forma_pago_id': False
             }
        else:
            values = {
                'methodo_pago': False,
                'forma_pago_id': False
                }
        self.update(values)

    @api.depends('amount_total', 'currency_id')
    def _get_amount_to_text(self):
        for record in self:
            record.amount_to_text = amount_to_text_es_MX.get_amount_to_text(record, record.amount_total, 'es_cheque', record.currency_id.name)
        
    @api.model
    def _get_amount_2_text(self, amount_total):
        return amount_to_text_es_MX.get_amount_to_text(self, amount_total, 'es_cheque', self.currency_id.name)
        
    
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update({'forma_pago_id': self.forma_pago_id.id,
                    'methodo_pago': self.methodo_pago,
                    'uso_cfdi_id': self.uso_cfdi_id.id,
                    'tipo_comprobante': 'I'
                    })
        return invoice_vals

    
    def _get_fecha_corregida(self):
        for sale in self:
           if sale.date_order:
              #corregir hora
              timezone = sale._context.get('tz')
              if not timezone:
                  timezone = sale.env.user.partner_id.tz or 'America/Mexico_City'
              #timezone = tools.ustr(timezone).encode('utf-8')

              local = pytz.timezone(timezone)
              naive_from = sale.date_order
              local_dt_from = naive_from.replace(tzinfo=pytz.UTC).astimezone(local)
              sale.fecha_corregida = local_dt_from.strftime ("%Y-%m-%d %H:%M:%S")
              #_logger.info('fecha ... %s', sale.fecha_corregida)
