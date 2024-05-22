# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ViaticosNomina(models.Model):
    _name = 'viaticos.nomina'
    _description = 'ViaticosNomina'

    
    @api.depends('entregas_ids.importe')
    def _compute_entregas(self):
        for record in self:
            record.entregas = sum([entregas.importe for entregas in record.entregas_ids])
    
    
    @api.depends('comprobaciones_ids.importe')
    def _compute_comprobaciones(self):
        for record in self:
            record.comprobaciones = sum([comprobaciones.importe for comprobaciones in record.comprobaciones_ids])
    
    
    @api.depends('comprobaciones', 'entregas')
    def _compute_por_comprobar(self):
        for record in self:
            record.por_comprobar = record.entregas - record.comprobaciones
                    
    name = fields.Char("Name", default=lambda self: _('New')) 
    fecha = fields.Date("Fecha")
    employee_id = fields.Many2one("hr.employee", 'Empleado')
    description = fields.Char("Description")
    entregas = fields.Float("Total entregas",compute="_compute_entregas", store=True)
    comprobaciones = fields.Float("Total comprobaciones",compute="_compute_comprobaciones", store=True)
    por_comprobar = fields.Float("Por comprobar",compute="_compute_por_comprobar", store=True)
    observaciones = fields.Text("Observaciones")
    state = fields.Selection([('draft','Generar entregas'), ('open','Generar comprobaciones'), ('closed','Cerrado')],string='Estado',default='draft')
    
    entregas_ids = fields.One2many('entregas.viaticos.nomina', 'viaticos_id', 'Entregas')
    comprobaciones_ids = fields.One2many('comprobaciones.viaticos.nomina', 'viaticos_id', 'Comprobaciones')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)
    
    @api.model
    def init(self):
        company_id = self.env['res.company'].search([])
        for company in company_id:
            viaticos_nomina_sequence = self.env['ir.sequence'].search([('code', '=', 'viaticos.nomina'), ('company_id', '=', company.id)])
            if not viaticos_nomina_sequence:
                viaticos_nomina_sequence.create({
                        'name': 'Viaticos nomina',
                        'code': 'viaticos.nomina',
                        'padding': 4,
                        'company_id': company.id,
                    })
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_company(vals['company_id']).next_by_code(
                    'viaticos.nomina') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('viaticos.nomina') or _('New')
        return super(ViaticosNomina, self).create(vals)
    
    
    def action_validar(self):
        payslip_obj = self.env['hr.payslip']
        
        structure_rec = self.env['hr.payroll.structure'].search([('name', '=', 'Entrega Viaticos')], limit=1)
        amount = sum([r.importe for r in self.entregas_ids.filtered(lambda x:x.cfdi)])
        if amount > 0:
           employee = self.employee_id
           vals = {
               'employee_id' : employee.id,
               'date_from' : self.fecha,
               'date_to' : self.fecha,
               'name' : self.description,
               'struct_id' : structure_rec and structure_rec.id,
               'tipo_nomina' : 'E',
               'contract_id': employee.contract_id.id,
               'dias_pagar': 1,
               }
           if employee.contract_id:
               vals.update({
                   'input_line_ids' : [(0, 0, {
                                    'name': 'Viaticos',
                                    'code': 'VIAT',
                                    'amount' : amount,
                                    'contract_id': employee.contract_id.id 
                                })],
                })
           payslip_obj.create(vals)
        self.write({'state': 'open'})
        return True

    
    def action_cerrar(self):
        payslip_obj = self.env['hr.payslip']
        structure_rec = self.env['hr.payroll.structure'].search([('name', '=', 'Comprobación Viaticos')], limit=1)
        amount = sum([r.importe for r in self.comprobaciones_ids.filtered(lambda x:x.cfdi and not x.generado)])
        if amount > 0:
                employee = self.employee_id
                vals = {
                    'employee_id' : employee.id,
                    'date_from' : self.fecha,
                    'date_to' : self.fecha,
                    'name' : self.description,
                    'struct_id' : structure_rec and structure_rec.id,
                    'tipo_nomina' : 'E',
                    'contract_id' : employee.contract_id.id,
                    'dias_pagar': 1,
                    }
                if employee.contract_id:
                    vals.update({
                        'input_line_ids' : [(0, 0, {
                                            'name': 'Viaticos',
                                            'code': 'PVIAT',
                                            'amount' : amount,
                                            'contract_id': employee.contract_id.id
                                            }),
                                            (0, 0, {
                                            'name': 'Ajuste en viáticos entregados al trabajador',
                                            'code': 'DVIAT',
                                            'amount' : amount,
                                            'contract_id': employee.contract_id.id
                                            }),
                                            ],
                        })
                payslip_obj.create(vals)

        for comp_line in self.comprobaciones_ids:
            if comp_line.cfdi and not comp_line.generado:
               comp_line.write({'generado': True})

        if self.por_comprobar == 0:
            self.write({'state': 'closed'})

        return True

class EntregasViaticosNomina(models.Model):
    _name = 'entregas.viaticos.nomina'
    _description = 'EntregasViaticosNomina'

    fecha = fields.Date("Fecha")
    referencia = fields.Char("Referencia")
    cfdi = fields.Boolean("CFDI")
    importe = fields.Float("Importe")
    viaticos_id = fields.Many2one("viaticos.nomina",'Viaticos')

class ComprobacionesViaticosNomina(models.Model):
    _name = 'comprobaciones.viaticos.nomina'
    _description = 'ComprobacionesViaticosNomina'

    fecha = fields.Date("Fecha")
    referencia = fields.Selection([('01','CFDI'), ('02','Documentos no fiscales'), ('03','Efectivo')], string='Tipo') #, ('04','Retención de nómina')
    cfdi = fields.Boolean("CFDI")
    generado = fields.Boolean("Generado")
    importe = fields.Float("Importe")
    viaticos_id = fields.Many2one("viaticos.nomina",'Viaticos')

