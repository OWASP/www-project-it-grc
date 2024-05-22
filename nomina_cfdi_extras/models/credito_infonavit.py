# -*- coding: utf-8 -*-
from odoo import models, fields, _, api
from datetime import date, datetime, timedelta
from odoo.exceptions import UserError

class CreditoInfonavit(models.Model):
    _name = 'credito.infonavit'
    _description = 'CreditoInfonavit'

    name = fields.Char("Name", required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Empleado', required=True)
    no_credito = fields.Char(string="Número de crédito")
    tipo_de_movimiento = fields.Selection([('15', 'Inicio de crédito vivienda'), 
                                          ('16', 'Fecha de suspensión de descuento'),
                                          ('17', 'Reinicio de descuento'),
                                          ('18', 'Modificación de tipo de descuento'),
                                          ('19', 'Modificación de valor de descuento'),
                                          ('20', 'Modificación de número de crédito'),],
                                            string='Tipo de movimiento')

    tipo_de_descuento = fields.Selection([('1', 'Porcentaje %'), 
                                          ('2', 'Cuota fija'),
                                          ('3', 'Veces SMGV'),],
                                            string='Tipo de descuento', default='1')

    aplica_tabla = fields.Selection([('N', 'No'), 
                                     ('S', 'Si')],
                                     string='Aplica tabla disminución')
    fecha = fields.Date(string="Fecha", required=True)
    valor_descuento = fields.Float(string="Valor descuento", digits = (12,4))
    state = fields.Selection([('draft', 'Borrador'), ('done', 'Hecho'), ('cancel', 'Cancelado')], string='Estado', default='draft')
    contract_id = fields.Many2one('hr.contract', string='Contrato')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)
    valor_infonavit_ant = fields.Float(string="Valor Infonavit anterior", digits = (12,4))

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_company(vals['company_id']).next_by_code('credito.infonavit') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('credito.infonavit') or _('New')
        result = super(CreditoInfonavit, self).create(vals)
        return result

    def action_validar(self):
        for rec in self:
            if rec.contract_id and rec.state == 'draft':
               if rec.tipo_de_descuento == '1':
                  rec.valor_infonavit_ant = rec.contract_id.infonavit_porc
                  rec.contract_id.infonavit_porc = rec.valor_descuento
                  rec.contract_id.infonavit_fijo = 0
                  rec.contract_id.infonavit_vsm = 0
               elif rec.tipo_de_descuento == '2':
                  rec.valor_infonavit_ant = rec.contract_id.infonavit_fijo
                  rec.contract_id.infonavit_fijo = rec.valor_descuento
                  rec.contract_id.infonavit_vsm = 0
                  rec.contract_id.infonavit_porc = 0
               else:
                  rec.valor_infonavit_ant = rec.contract_id.infonavit_vsm
                  rec.contract_id.infonavit_vsm = rec.valor_descuento
                  rec.contract_id.infonavit_porc = 0
                  rec.contract_id.infonavit_fijo = 0
            rec.write({'state':'done'})
        return

    def action_cancelar(self):
        for rec in self:
            if rec.contract_id and rec.state == 'done':
               if rec.tipo_de_descuento == '1':
                  rec.contract_id.infonavit_porc = rec.valor_infonavit_ant
                  rec.contract_id.infonavit_fijo = 0
                  rec.contract_id.infonavit_vsm = 0
               elif rec.tipo_de_descuento == '2':
                  rec.contract_id.infonavit_fijo = rec.valor_infonavit_ant
                  rec.contract_id.infonavit_vsm = 0
                  rec.contract_id.infonavit_porc = 0
               else:
                  rec.contract_id.infonavit_vsm = rec.valor_infonavit_ant
                  rec.contract_id.infonavit_porc = 0
                  rec.contract_id.infonavit_fijo = 0
            rec.write({'state':'cancel'})

    def action_draft(self):
        self.write({'state':'draft'})

    def unlink(self):
        raise UserError("Los registros no se pueden borrar, solo cancelar.")

    def action_change_state(self):
        for creditoinfonavit in self:
            if creditoinfonavit.state == 'draft':
                creditoinfonavit.action_validar()
