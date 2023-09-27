# -*- coding: utf-8 -*-
import logging
from datetime import date
from statistics import mode
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class ComplianceVersion(models.Model):
    _name = 'compliance.version'
    _description = 'Compliance Version'

    name = fields.Char(string='Compliance Version', required=True)
    description  = fields.Text(string='Description')
    compliance_control_objective_ids = fields.One2many('compliance.control.objective', 'compliance_version_id', string='Objective'  )
    _sql_constraints = [('name_uniq', 'unique(name)', "The compliance version name already exists.")]

    def action_print_report_version(self):
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
                #r.append(rr)
                for iii in ii.compliance_control_ids:
                    d = []
                    compliance_detail = self.env['compliance.iso.control'].search([('compliance_control_id','=',iii.id)])
                    for iiii in compliance_detail:
                        rrr=[]
                        s = ''
                        p = ''
                        rrr.append(iiii.compliance_control_id.name)
                        rrr.append(iiii.compliance_control_id.description)
                        for iiiii in iiii.iso_control_id:
                            s = s + ' - ' + str(iiiii.display_name)
                        rrr.append(s)

                        for iiiii in iiii.document_page_id:
                            p = p + ' - ' + str(iiiii.display_name)
                        rrr.append(p)

                        c_records.append(rrr)
                        d.append(rrr)
                    rr.append(d)
                r.append(rr)
            record.append(r)
        data['compliance'] = record
        data['c_records'] = c_records
        return self.env.ref('grcbit.print_compliance').report_action(self, data=data)
    
class ComplianceControlObjective(models.Model):
    _name = 'compliance.control.objective'
    _description = 'Compliance Objective'
    _rec_name = 'display_name'

    name = fields.Char(string='Compliance Objective', required=True)
    display_name = fields.Char(string='Compliance Objective', compute='_compute_display_name')
    compliance_version_id = fields.Many2one('compliance.version', string='Compliance Version', required=True)
    description  = fields.Text(string='Description')
    compliance_control_ids = fields.One2many('compliance.control','compliance_control_objective_id', string='Requirement')
    _sql_constraints = [('name_uniq', 'unique(name)', "The compliance objective name already exists.")]

    @api.depends('compliance_version_id','name')
    def _compute_display_name(self):
        for i in self:
            i.display_name = str(i.compliance_version_id.name) + ' - ' + i.name

class ComplianceControl(models.Model):
    _name = 'compliance.control'
    _description = 'Compliance Requirement'
    _rec_name = 'display_name'

    name = fields.Char(string='Compliance Requirement', required=True)
    display_name = fields.Char(string='Compliance Requirement', compute='_compute_display_name')
    compliance_control_objective_id = fields.Many2one('compliance.control.objective', string='Compliance Objective', required=True)
    description  = fields.Text(string='Description')
    _sql_constraints = [('name_uniq', 'unique(name)', "The compliance requirement name already exists.")]

    @api.depends('compliance_control_objective_id','name')
    def _compute_display_name(self):
        for i in self:
            i.display_name = str(i.compliance_control_objective_id.compliance_version_id.name) + ' - ' + str(i.compliance_control_objective_id.name) + ' - ' + i.name

class ComplianceIsoControl(models.Model):
    _name = 'compliance.iso.control'
    _description = 'Compliance - ISMS'

    compliance_control_id = fields.Many2one('compliance.control', string='Compliance Requirement', required=True)
    iso_control_id     = fields.Many2many('iso.control', string='ISMS Control')
    document_page_id   = fields.Many2many('document.page', string='Policy / Process')
    description  = fields.Text(string='Compliance Description')