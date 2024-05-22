# -*- coding: utf-8 -*-
from odoo import models, fields, _, api
from odoo.exceptions import UserError
#from datetime import datetime

class HorasNomina(models.Model):
    _name = 'horas.nomina'
    _description = 'HorasNomina'

    name = fields.Char("Name", required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Empleado')
    fecha = fields.Date('Fecha')
    tipo_de_hora = fields.Selection([('1','Simple'),
                                      ('2','Doble'),
                                      ('3', 'Triple'),
                                      ('4', 'Automático'),], string='Tipo de hora extra')
    state = fields.Selection([('draft', 'Borrador'), ('done', 'Hecho'), ('cancel', 'Cancelado')], string='Estado', default='draft')
    horas = fields.Char("Horas", required=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)

    @api.model
    def init(self):
        company_id = self.env['res.company'].search([])
        for company in company_id:
            horas_nomina_sequence = self.env['ir.sequence'].search([('code', '=', 'horas.nomina'), ('company_id', '=', company.id)])
            if not horas_nomina_sequence:
                horas_nomina_sequence.create({
                        'name': 'Horas Extras nomina',
                        'code': 'horas.nomina',
                        'padding': 4,
                        'company_id': company.id,
                    })

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_company(vals['company_id']).next_by_code('horas.nomina') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('horas.nomina') or _('New')
        result = super(HorasNomina, self).create(vals)
        return result

    def action_validar(self):
        self.write({'state':'done'})
        return

    def action_cancelar(self):
        for record in self:
           self.write({'state':'cancel'})

    def action_draft(self):
        self.write({'state':'draft'})

    def unlink(self):
        raise UserError("Los registros no se pueden borrar, solo cancelar.")

    def action_change_state(self):
        for horasextras in self:
            if horasextras.state == 'draft':
                horasextras.action_validar()
