# -*- coding: utf-8 -*-
import logging
from datetime import date
from statistics import mode
from odoo import models, fields, api, _
from odoo.osv import expression
from odoo import SUPERUSER_ID

_logger = logging.getLogger(__name__)

class ComplianceVersion(models.Model):
    _name = 'compliance.version'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Compliance Version'

    name = fields.Char(string='Compliance Version', required=True)
    active = fields.Boolean(default=True)
    description  = fields.Text(string='Description')
    compliance_control_objective_ids = fields.One2many('compliance.control.objective', 'compliance_version_id', string=' ', required=True  )
    attachment_file = fields.Binary(string="Attachment")
    _sql_constraints = [('name_uniq', 'unique(name)', "The compliance version name already exists.")]


    def get_data_records(self):
        data = {}
        record = []
        c_records = []
        for i in self:
            r = []
            r.append(i.display_name)
            r.append(i.description)
            for ii in i.compliance_control_objective_ids:
                rr=[]
                rr.append(ii.display_name)
                rr.append(ii.description) 
                for iii in ii.compliance_control_ids:
                    d = []
                    compliance_detail = self.env['compliance.iso.control'].search([('compliance_control_id','=',iii.id)])
                    for iiii in compliance_detail:
                        rrr=[]
                        
                        rrr.append(iiii.compliance_control_id.display_name)
                        rrr.append(iiii.description)
                        rrr.append([x.display_name for x in iiii.control_id])

                        c_records.append(rrr)
                        d.append(rrr)
                    rr.append(d)
                r.append(rr)
            record.append(r)
        data['compliance'] = record
        data['c_records'] = c_records
        return data['c_records']
    
class ComplianceControlObjective(models.Model):
    _name = 'compliance.control.objective'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Compliance Objective'

    name = fields.Char(string='Compliance Objective', required=True)
    active = fields.Boolean(default=True)
    compliance_version_id = fields.Many2one('compliance.version', string='Compliance Version')
    description  = fields.Html(string='Description')
    compliance_control_ids = fields.One2many('compliance.control','compliance_control_objective_id', string=' ')
    _sql_constraints = [('name_uniq', 'unique(name)', "The compliance objective name already exists.")]

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '%s - %s' % (rec.compliance_version_id.name, rec.name)))
        return result

class ComplianceControl(models.Model):
    _name = 'compliance.control'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Compliance Requirement'

    name = fields.Char(string='Compliance Requirement', required=True)
    active = fields.Boolean(default=True)
    compliance_control_objective_id = fields.Many2one('compliance.control.objective', string='Compliance Objective', required=True)
    description  = fields.Html(string='Description')
    _sql_constraints = [('name_uniq', 'unique(name)', "The compliance requirement name already exists.")]

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '%s - %s - %s' % (rec.compliance_control_objective_id.compliance_version_id.name, rec.compliance_control_objective_id.name, rec.name)))
        return result

class ComplianceIsoControl(models.Model):
    _name = 'compliance.iso.control'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Compliance - ISMS'

    compliance_control_id = fields.Many2one('compliance.control', string='Compliance Requirement', required=True) #requerimiento NIST - AC-1 POLICY AND PROCEDURES
    iso_control_id     = fields.Many2many('iso.control', string='ISMS Control', required=True) #ISO
    active = fields.Boolean(default=True)
    compliance_version = fields.Many2one(
        'compliance.version', 
        string="Compliance Version", 
        compute="get_version",
        store=True)
    control_id = fields.Many2many('control.design', string="Control", required=True)
    description  = fields.Html(string='Compliance Description', required=True) #Cumplimiento
    control_status = fields.Integer(string="Status")
    is_applicable = fields.Boolean(string="Is Applicable")
    is_implemented = fields.Boolean(string="Is Implemented")
    is_compensatory_control = fields.Boolean(string="Is Compensatory Control")

    _sql_constraints = [('compliance_control_id_uniq', 'unique(compliance_control_id)', "The Compliance Control it is already being used.")]

    @api.depends('compliance_control_id')
    def get_version(self):
        for rec in self:
            if rec.compliance_control_id:
                rec.compliance_version = rec.compliance_control_id.compliance_control_objective_id.compliance_version_id.id

    @api.onchange('control_id','control_id.state')
    def _status_control(self):
        status = 0
        for i in self.control_id:
            if i.state == 'draft':
                status += 25
            if i.state == 'designed':
                status += 50
            if i.state == 'implemented':
                status += 75
            if i.state == 'approved':
                status += 100
        if len(self.control_id) > 0:
            self.sudo().control_status = status / len(self.control_id)
        else:
            self.sudo().control_status = 0