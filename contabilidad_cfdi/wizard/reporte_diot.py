# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
import calendar
import json
import logging
_logger = logging.getLogger(__name__)

class ReporteDIOTWizard(models.TransientModel):
    _name = 'reporte.diot.wizard'
    _description = 'reporte_diot_wizard'

    year = fields.Selection([('2024','2024'),('2023','2023'),('2022','2022'),('2021','2021'),('2020','2020')], string="Año", required=1)
    month = fields.Selection([('01','Enero'),('02','Febrero'),('03','Marzo'),('04','Abril'),('05','Mayo'),('06','Junio'),('07','Julio'),('08','Agosto'),('09','Septiembre'),('10','Octubre'),('11', 'Noviembre'),('12','Diciembre')], string='Mes', required=1)

    def action_view_report(self):
        date_from = self.year+'-'+self.month+'-01'
        date_to = self.year+'-'+self.month+'-'+str(calendar.monthrange(int(self.year),int(self.month))[1])

        payment_ids = self.env['account.payment'].search([#('partner_type','=','supplier'),
                                                           ('payment_type','=', 'outbound'),
                                                           ('is_internal_transfer','=', False),
                                                           ('date', '>=',date_from), 
                                                           ('date', '<=',date_to),
                                                           ('diot','=', True),
                                                           ])

        line_vals = {}
        for payment in payment_ids:
            _logger.info('factura %s', payment.name)
            partner = payment.partner_id
            partner_id = partner.id
            if partner_id not in line_vals and payment.reconciled_bill_ids:
                line_vals[partner_id] = {
                                         'tipo_proveedor' : partner.tipo_proveedor, #uno
                                         'tipo_operacion' : partner.tipo_operacion, #dos
                                         'rfc' : partner.vat,  #tres
                                         'registro_tributario' : partner.tipo_proveedor == '05' and partner.registro_tributario or '', #cuatro
                                         'partner_id' : partner.tipo_proveedor == '05' and partner_id or '',   #cinco
                                         'nacionalidad' : partner.tipo_proveedor == '05' and partner.pais_diot.nacionalidad or '', #seis
                                         'pais' : partner.tipo_proveedor == '05' and partner.pais_diot.c_pais or ''  #siete
                                         }
            if payment.reconciled_bill_ids:
                for invoice in payment.reconciled_bill_ids:
                    payment_dict = invoice.invoice_payments_widget
                    if not payment_dict:
                       continue
                    payment_content = payment_dict['content']
                    for invoice_payments in payment_content:
                        if invoice_payments['account_payment_id'] == payment.id:
                            paid_pct = invoice_payments['amount'] / invoice.amount_total
                            tax_lines={}
                            for invoice_line in invoice.invoice_line_ids:
                                price_reduce = invoice_line.price_unit * (1.0 - invoice_line.discount / 100.0)
                                if invoice_line.tax_ids:
                                    res = invoice_line.tax_ids.compute_all(price_reduce, quantity=invoice_line.quantity, product=invoice_line.product_id, partner=invoice.partner_id)
                                    taxes = res['taxes']
                                    for tax in taxes:
                                        if (tax['id'],tax['name']) not in tax_lines:
                                            tax_lines[(tax['id'],tax['name'])] = tax.get('base') 
                                        else:
                                            tax_lines[(tax['id'],tax['name'])] = tax_lines[(tax['id'],tax['name'])] + tax.get('base')

                            for tax_line,values in tax_lines.items():
                                if payment.payment_type == 'outbound':
                                    rate = 1
                                    if invoice.currency_id.name != 'MXN':
                                       vals = self.env['res.currency.rate'].search([('currency_id','=',invoice.currency_id.id),('name','<=',invoice_payments['date'])],order='name desc',limit=1)
                                       rate =  1  / vals.rate

                                    tax_used = self.env['account.tax'].search([('name','=', tax_line[1])],limit=1)
                                    if tax_used.amount == 16.0 and partner.vat != 'XEXX010101000' and not payment.diot_no_acreditable:      #ocho
                                        line_vals[partner_id].update({'pagado_16_15_amount': values * paid_pct * rate + line_vals[partner_id].get('pagado_16_15_amount',0)})
                                    elif tax_used.amount == 15.0 and partner.vat != 'XEXX010101000' and not payment.diot_no_acreditable:      #nueve
                                        line_vals[partner_id].update({'pagado_15_amount': values * paid_pct * rate + line_vals[partner_id].get('pagado_15_amount',0)})
                                    elif tax_used.amount == 16.0 and partner.vat != 'XEXX010101000' and payment.diot_no_acreditable:      #diez
                                        line_vals[partner_id].update({'pagado_16_amount_no_acreditable': values * paid_pct * rate + line_vals[partner_id].get('pagado_16_amount_no_acreditable',0)})
                                    elif tax_used.amount == 11.0 and partner.vat != 'XEXX010101000' and not payment.diot_no_acreditable:      #once
                                        line_vals[partner_id].update({'pagado_11_10_amount': values * paid_pct * rate + line_vals[partner_id].get('pagado_11_10_amount',0)})
                                    elif tax_used.amount == 11.0 and partner.vat != 'XEXX010101000' and not payment.diot_no_acreditable:      #doce
                                        line_vals[partner_id].update({'pagado_10_amount': values * paid_pct * rate + line_vals[partner_id].get('pagado_10_amount',0)})
                                    elif tax_used.amount == 8.0 and partner.vat != 'XEXX010101000' and not payment.diot_no_acreditable:      #trece
                                        line_vals[partner_id].update({'pagado_8_amount': values * paid_pct * rate + line_vals[partner_id].get('pagado_8_amount',0)})
                                    elif tax_used.amount == 11.0 and partner.vat != 'XEXX010101000' and payment.diot_no_acreditable:      #catorce
                                        line_vals[partner_id].update({'pagado_11_amount_no_acreditable': values * paid_pct * rate + line_vals[partner_id].get('pagado_11_amount_no_acreditable',0)})
                                    elif tax_used.amount == 8.0 and partner.vat != 'XEXX010101000' and payment.diot_no_acreditable:      #quince
                                        line_vals[partner_id].update({'pagado_8_amount_no_acreditable': values * paid_pct * rate + line_vals[partner_id].get('pagado_8_amount_no_acreditable',0)})
                                    elif tax_used.amount == 16.0 and partner.vat == 'XEXX010101000' and not payment.diot_no_acreditable:       #dieciseis
                                        line_vals[partner_id].update({'importacion_16': values * paid_pct * rate + line_vals[partner_id].get('importacion_16',0)})
                                    elif tax_used.amount == 16.0 and partner.vat == 'XEXX010101000' and payment.diot_no_acreditable:       #diecisiete
                                        line_vals[partner_id].update({'importacion_16_na': values * paid_pct * rate + line_vals[partner_id].get('importacion_16_na',0)})
                                    elif tax_used.amount == 11.0 and partner.vat == 'XEXX010101000' and not payment.diot_no_acreditable:       #dieciocho
                                        line_vals[partner_id].update({'importacion_11': values * paid_pct * rate + line_vals[partner_id].get('importacion_11',0)})
                                    elif tax_used.amount == 11.0 and partner.vat == 'XEXX010101000' and payment.diot_no_acreditable:       #diecinueve
                                        line_vals[partner_id].update({'importacion_11_na': values * paid_pct * rate + line_vals[partner_id].get('importacion_11_na',0)})
                                    elif tax_used.amount == 0.0 and partner.vat == 'XEXX010101000' and tax_used.tipo_factor == 'Exento': #veinte
                                        line_vals[partner_id].update({'importacion_exento': values * paid_pct * rate + line_vals[partner_id].get('importacion_exento',0)})
                                    elif tax_used.amount == 0.0 and partner.vat != 'XEXX010101000' and tax_used.tipo_factor != 'Exento': #veintiuno
                                        line_vals[partner_id].update({'pagado_0_amount': values * paid_pct * rate + line_vals[partner_id].get('pagado_0_amount',0)})
                                    elif tax_used.amount == 0.0 and partner.vat != 'XEXX010101000' and tax_used.tipo_factor == 'Exento': #veintidos
                                        line_vals[partner_id].update({'pagado_exento': values * paid_pct * rate + line_vals[partner_id].get('pagado_exento',0)})
                                    elif tax_used.amount < 0.0 and partner.vat != 'XEXX010101000' and not payment.diot_no_acreditable and tax_used.impuesto == '002': #veintitres
                                        line_vals[partner_id].update({'iva_retenido': values * paid_pct * rate * abs(tax_used.amount)/100 + line_vals[partner_id].get('iva_retenido',0)})
                                    else:
                                        line_vals[partner_id].update({'iva_devoluciones': values * paid_pct * rate * abs(tax_used.amount)/100 + line_vals[partner_id].get('iva_devoluciones',0)})

        ########## agregar IVA de Pedimentos
        iva_pedimentos_ids = self.env['iva.pedimentos'].search([
                                                           ('fecha', '>=',date_from), 
                                                           ('fecha', '<=',date_to),
                                                           ])
        if iva_pedimentos_ids:
            for iva_pedimentos in iva_pedimentos_ids: 
                partner = iva_pedimentos.partner_id
                if partner.id not in line_vals:
                    line_vals[partner.id] = {
                                         'tipo_proveedor' : partner.tipo_proveedor, #uno
                                         'tipo_operacion' : partner.tipo_operacion, #dos
                                         'rfc' : partner.vat,  #tres
                                         'registro_tributario' : partner.tipo_proveedor == '05' and partner.registro_tributario or '', #cuatro
                                         'partner_id' : partner.tipo_proveedor == '05' and partner_id or '',   #cinco
                                         'nacionalidad' : partner.tipo_proveedor == '05' and partner.pais_diot.nacionalidad or '', #seis
                                         'pais' : partner.tipo_proveedor == '05' and partner.pais_diot.c_pais or ''  #siete
                                         }
                line_vals[partner.id].update({'importacion_16': round(iva_pedimentos.monto_iva * 1.16,2) + line_vals[partner.id].get('importacion_16',0)})

        wizard_line_obj = self.env['reporte.diot.wizard.line']
        created_lines = []
        for partner_id,vals in line_vals.items():
            rec = wizard_line_obj.create(vals)
            created_lines.append(rec.id)
        
        try:
            tree_id = self.env['ir.model.data'].check_object_reference('contabilidad_cfdi', 'reporte_diot_wizard_line_form_view_tree_itadmin')[1]
        except ValueError:
            tree_id = False
            
        return {
            'name': 'Reporte DIOT',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'reporte.diot.wizard.line',
            'views': [(tree_id, 'tree')],
            'view_id': tree_id,
            'domain': [('id','in',created_lines)]
        }    
        


class ReporteDIOTWizardLine(models.TransientModel):
    _name = 'reporte.diot.wizard.line'
    _description = 'reporte_diot_line'

    tipo_proveedor = fields.Selection(
        selection=[('04', _('04 - Proveedor nacional')),
                   ('05', _('05 - Proveedor extranjero')),
                   ('15', _('15 - Proveedor global')),],string=_('Tipo de tercero'),) #uno
    
    tipo_operacion = fields.Selection(
        selection=[('03', _('03 - Provisión de servicios profesionales')), #dos
                   ('06', _('06 - Arrendamientos')),
                   ('85', _('85 - Otros')),],
        string=_('Tipo de opreacion'),
    )
    rfc = fields.Char("RFC") #tres
    registro_tributario = fields.Char(string='No. ID fiscal') #cuatro
    partner_id = fields.Many2one('res.partner',string='Nombre') #cinco
    pais = fields.Char(string='Pais') # seis
    nacionalidad = fields.Char(string='Nacionalidad') # siete
    pagado_16_15_amount = fields.Float('Pagado 16%') #ocho
    pagado_15_amount = fields.Float('Pagado 15%')  # nueve
    pagado_16_amount_no_acreditable = fields.Float('Pagado 16% NA') #diez
    pagado_11_10_amount = fields.Float('Pagado 11%') #once
    pagado_10_amount = fields.Float('Pagado 10%') #doce
    pagado_8_amount = fields.Float('Pagado 8%') #trece
    pagado_11_amount_no_acreditable = fields.Float('Pagado 11% NA') #catorce
    pagado_8_amount_no_acreditable = fields.Float('Pagado 8% NA') #quince
    importacion_16 = fields.Float('Importacion 16%') #dieciseis
    importacion_16_na = fields.Float('Importacion 16% NA') #diecisiete
    importacion_11 = fields.Float('Importacion 11%') #dieciocho
    importacion_11_na = fields.Float('Importacion 11 NA%') #diecinueve
    importacion_exento = fields.Float('Importacion Exento%') #veinte
    pagado_0_amount = fields.Float('Pagado 0%')#veintiuno
    pagado_exento = fields.Float('Pagado exento')#veintidos
    iva_retenido = fields.Float('IVA Retenido')#veintitres
    iva_devoluciones = fields.Float('IVA devoluciones')#veinticuatro
