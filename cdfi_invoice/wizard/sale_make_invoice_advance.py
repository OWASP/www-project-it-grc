# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time

from odoo import models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"
    _description = "Sales Advance Payment Invoice"
    
    
    def create_invoices(self):
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))

        if self.advance_payment_method == 'delivered':
            sale_orders._create_invoices(final=self.deduct_down_payments)
        else:
            # Create deposit product if necessary
            if not self.product_id:
                vals = self._prepare_deposit_product()
                self.product_id = self.env['product.product'].create(vals)
                self.env['ir.config_parameter'].sudo().set_param('sale.default_deposit_product_id', self.product_id.id)

            sale_line_obj = self.env['sale.order.line']
            for order in sale_orders:
                if self.advance_payment_method == 'percentage':
                    amount = order.amount_untaxed * self.amount / 100
                    moves = order._create_invoices(final=True)
                    for line in order.order_line:
                        invoice_lines = line.invoice_lines
                        if invoice_lines:
                            sol_qty = line.product_uom_qty
                            qty = sol_qty * (self.amount / 100.0)
                            invoice_lines.write({'quantity': qty}) 
                            
                    #moves.compute_taxes()
                else:
                    amount = self.fixed_amount
                if self.product_id.invoice_policy != 'order':
                    raise UserError(_('The product used to invoice a down payment should have an invoice policy set to "Ordered quantities". Please update your deposit product to be able to create a deposit invoice.'))
                if self.product_id.type != 'service':
                    raise UserError(_("The product used to invoice a down payment should be of type 'Service'. Please use another product or update this product."))
                taxes = self.product_id.taxes_id.filtered(lambda r: not order.company_id or r.company_id == order.company_id)
                if order.fiscal_position_id and taxes:
                    tax_ids = order.fiscal_position_id.map_tax(taxes, self.product_id, order.partner_shipping_id).ids
                else:
                    tax_ids = taxes.ids
                context = {'lang': order.partner_id.lang}
                analytic_tag_ids = []
                for line in order.order_line:
                    analytic_tag_ids = [(4, analytic_tag.id, None) for analytic_tag in line.analytic_tag_ids]
                so_line = sale_line_obj.create({
                    'name': _('Down Payment: %s') % (time.strftime('%m %Y'),),
                    'price_unit': amount,
                    'product_uom_qty': 0.0,
                    'order_id': order.id,
                    'discount': 0.0,
                    'product_uom': self.product_id.uom_id.id,
                    'product_id': self.product_id.id,
                    'analytic_tag_ids': analytic_tag_ids,
                    'tax_id': [(6, 0, tax_ids)],
                    'is_downpayment': True,
                })
                del context
                if self.advance_payment_method != 'percentage':
                    self._create_invoice(order, so_line, amount)
        if self._context.get('open_invoices', False):
            return sale_orders.action_view_invoice()
        return {'type': 'ir.actions.act_window_close'}
    
    