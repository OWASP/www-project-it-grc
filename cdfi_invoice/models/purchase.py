# -*- coding: utf-8 -*-

from odoo import fields, api, models,_
import ast
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    factura_cfdi = fields.Boolean('Factura CFDI')
    tipo_comprobante = fields.Selection(
        selection=[('I', 'Ingreso'), 
                   ('E', 'Egreso'),
                    ('T', 'Traslado'),],
        string=_('Tipo de comprobante'),
    )
    forma_pago_id  =  fields.Many2one('catalogo.forma.pago', string='Forma de pago')
    methodo_pago = fields.Selection(
        selection=[('PUE', _('Pago en una sola exhibición')),
                   ('PPD', _('Pago en parcialidades o diferido')),],
        string=_('Método de pago'), 
    )
    uso_cfdi_id  =  fields.Many2one('catalogo.uso.cfdi', string='Uso CFDI (cliente)')
    estado_factura = fields.Selection(
        selection=[('factura_no_generada', 'Factura no generada'), ('factura_correcta', 'Factura correcta'), 
                   ('problemas_factura', 'Problemas con la factura'), ('factura_cancelada', 'Factura cancelada'), ],
        string=_('Estado de factura'),
        default='factura_no_generada',
        readonly=True
    )	
    numero_cetificado = fields.Char(string=_('Numero de certificado'))
#    cetificaso_sat = fields.Char(string=_('Certificado SAT'))
    folio_fiscal = fields.Char(string=_('Folio Fiscal'))
    fecha_certificacion = fields.Datetime(string=_('Fecha y Hora Certificación'))
#    cadena_origenal = fields.Char(string=_('Cadena Original del Complemento digital de SAT'))
    selo_digital_cdfi = fields.Char(string=_('Sello Digital del CDFI'))
    selo_sat = fields.Char(string=_('Sello del SAT'))
    moneda = fields.Char(string=_('Moneda'))
    tipocambio = fields.Char(string=_('Tipo de cambio'))
#    folio = fields.Char(string=_('Folio'))
#    version = fields.Char(string=_('Version'))   
#    invoice_datetime = fields.Char(string=_('11/12/17 12:34:12'))
    tipo_relacion = fields.Selection(
        selection=[('01', 'Nota de crédito de los documentos relacionados'), 
                   ('02', 'Nota de débito de los documentos relacionados'), 
                   ('03', 'Devolución de mercancía sobre facturas o traslados previos'),
                   ('04', 'Sustitución de los CFDI previos'), 
                   ('05', 'Traslados de mercancías facturados previamente'),
                   ('06', 'Factura generada por los traslados previos'), 
                   ('07', 'CFDI por aplicación de anticipo'),],
        string=_('Tipo relación'),
    )
    uuid_relacionado = fields.Char(string=_('CFDI Relacionado'))

    def action_view_invoice(self, invoices=False):
        res = super(PurchaseOrder,self).action_view_invoice(invoices=invoices)
        if res:
            if res.get('context')==None:
                res['context']={}
            if res['context']:    
                context=ast.literal_eval(res['context'])
            order = self[0] 
            context.update({
                'default_factura_cfdi' : order.factura_cfdi,
                'default_tipo_comprobante' : order.tipo_comprobante,
                'default_forma_pago_id' : order.forma_pago_id.id,
                'default_methodo_pago' : order.methodo_pago,
                'default_uso_cfdi_id' : order.uso_cfdi_id.id,
                'default_estado_factura' : order.estado_factura,
                'default_numero_cetificado' : order.numero_cetificado,
                'default_folio_fiscal' : order.folio_fiscal,
                'default_fecha_certificacion' : order.fecha_certificacion,
                'default_selo_digital_cdfi' : order.selo_digital_cdfi,
                'default_selo_sat' : order.selo_sat,
                'default_moneda' : order.moneda,
                'default_tipocambio' : order.tipocambio,
                'default_tipo_relacion' : order.tipo_relacion,
                'default_uuid_relacionado' : order.uuid_relacionado 
                })
            res['context'] = context
        return res


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:            			
