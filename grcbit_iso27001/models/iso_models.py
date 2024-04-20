# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
from datetime import date
from statistics import mode

_logger = logging.getLogger(__name__)

class ControlType(models.Model):
    _name = 'control.type'
    _description = 'Data Inventory'

    name = fields.Char(string=_('Control Type'), required=True)
    description = fields.Html(string=_('Description'), required=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', _("The control type name already exists."))]

class SecurityProperty(models.Model):
    _name = 'security.property'
    _description = 'Data Inventory'

    name = fields.Char(string=_('Security Property'), required=True)
    description = fields.Html(string=_('Description'), required=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', _("The security property name already exists."))]

class CybersecurityConcept(models.Model):
    _name = 'cybersecurity.concept'
    _description = 'Data Inventory'

    name = fields.Char(string=_('Cybersecurity Concept'), required=True)
    description = fields.Html(string=_('Description'), required=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', _("The cybersecurty concept name already exists."))]

class OperationalCapability(models.Model):
    _name = 'operational.capability'
    _description = 'Data Inventory'

    name = fields.Char(string=_('Operational Capability'), required=True)
    description = fields.Html(string=_('Description'), required=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', _("The operational capability name already exists."))]

class SecurityDomain(models.Model):
    _name = 'security.domain'
    _description = 'Data Inventory'
    name = fields.Char(string=_('Security Domain'), required=True)
    description = fields.Html(string=_('Description'), required=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', _("The security domain name already exists."))]

#--------------------------
# ISO 27001:2022 - Controls
#--------------------------

class ControlCategory(models.Model):
    _name = 'control.category'
    _description = 'Control Category'
    _rec_name = 'display_name'

    display_name = fields.Char(string=_('Control Category'), compute='_compute_display_name')
    id_control_category = fields.Char(string=_('ID Control Category'), required=True)
    name = fields.Char(string=_('Control Category'), required=True)
    description = fields.Html(string=_('Description'))
    statement_applicability_count = fields.Integer(string=_('Statement Applicability Acount'))
    active = fields.Boolean(default=True)
    _sql_constraints = [
        ('name_uniq', 'unique(name)', _("The control category name already exists.")),
        ('id_control_category_uniq', 'unique(id_control_category)', _("The control category ID already exists."))
    ]

    @api.depends('id_control_category','name')
    def _compute_display_name(self):
        for i in self:
            i.display_name = i.id_control_category + ' ' + i.name

    @api.model
    def web_read_group(self, domain, fields, groupby, limit=None, offset=0, orderby=False,lazy=True, expand=False, expand_limit=None, expand_orderby=False):
        res = super().web_read_group(domain, fields, groupby, limit, offset, orderby, lazy, expand, expand_limit, expand_orderby)
        for i in self.env['control.category'].search([]):
            data_assets = self.env['statement.applicability'].search([('name.control_category_id', '=', i.id )])
            self.env['control.category'].sudo().search([('id','=',i.id)]).sudo().write({'statement_applicability_count':len(data_assets)})
        return res

class IsoControl(models.Model):
    _name = 'iso.control'
    _description = 'ISO Control'
    _order = 'id ASC'

    _rec_name = 'display_name'
    id_iso_control      = fields.Char(string=_('ID ISO Control'), required=True)
    name = fields.Char(string=_('Control Title'), required=True)
    display_name = fields.Char(string=_('Control Title'), compute='_compute_display_name')
    control_category_id = fields.Many2one('control.category', string=_('Control Category'), required=True)
    control_type_id = fields.Many2many('control.type', string=_('Control Type'), required=True)
    security_property_id = fields.Many2many('security.property', string=_('Security Property'), required=True)
    cybersecurity_concept_id = fields.Many2many('cybersecurity.concept', string=_('Cybersecurity Concept'), required=True)
    operational_capability_id = fields.Many2many('operational.capability', string=_('Operational Capability'), required=True)
    security_domain_id = fields.Many2many('security.domain', string=_('Security Domain'), required=True)
    control = fields.Html(string=_('Control'), required=True)
    purpose = fields.Html(string=_('Purpose'), required=True)
    guidance = fields.Html(string=_('Guidance'), required=True)
    other_information = fields.Html(string=_('Other Information'))
    attachment = fields.Many2many('ir.attachment', string=_("Attachment"))
    active = fields.Boolean(default=True)
    _sql_constraints = [
        ('name_uniq', 'unique(name)', _("The ISO control name already exists.")),
        ('id_iso_control_uniq', 'unique(id_iso_control)', _("The ISO control ID already exists."))
    ]

    @api.depends('id_iso_control','name')
    def _compute_display_name(self):
        for i in self:
            i.display_name = str(i.id_iso_control) + ' ' + i.name

class StatementApplicability(models.Model):
    _name = 'statement.applicability'
    _description = 'Statement Applicability'
    _order = 'name'

    name = fields.Many2one('iso.control', string=_('ISO Control'), required=True)
    is_applicable = fields.Boolean(string=_('Is Applicable?'), required=True)
    reason_selection = fields.Text(string=_('Reason for Selection'))
    # document_page_id = fields.Many2many('document.page', string=_('Policy'))
    control_design_id = fields.Many2many('control.design',string=_('Control'))
    control_status = fields.Integer(string=_('Status'), readonly=True, group_operator='avg')
    control_category_id = fields.Many2one('control.category', string=_("Control Category"), related="name.control_category_id", store=True)

    attachment = fields.Many2many('ir.attachment', string=_("Attachment"))
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', _("The control name already exists."))]

    @api.onchange('control_design_id','control_design_id.state')
    def _status_control(self):
        status = 0
        for i in self.control_design_id:
            if i.state == 'draft':
                status += 25
            if i.state == 'designed':
                status += 50
            if i.state == 'implemented':
                status += 75
            if i.state == 'approved':
                status += 100
        if len(self.control_design_id) > 0:
            self.sudo().control_status = status / len(self.control_design_id)
        else:
            self.sudo().control_status = 0

    def get_iso_contol(self, category_id):
        iso_control = self.env['iso.control'].search([])
        data = []
        for cat in iso_control.filtered(lambda x: x.control_category_id.id_control_category == str(category_id)):
            data.append(cat.id)
        return len(data)
    
    def get_is_applicable(self, category_id):
        statement_applicability = self.env['statement.applicability'].search([('is_applicable','=',True)])
        data = []
        for cat in statement_applicability.filtered(lambda x: x.name.control_category_id.id_control_category == str(category_id)):
            data.append(cat.id)
        return len(data)
    
    def get_is_status_avg(self, category_id):
        statement_applicability = self.env['statement.applicability'].search([])
        data = []
        percentage = 0
        total = 0
        for cat in statement_applicability.filtered(lambda x: x.name.control_category_id.id_control_category == str(category_id)):
            data.append(cat.id)
            percentage += cat.control_status
        if len(data) > 0:
            total = percentage / len(data)
        else:
            total = 0
        return int(total)

class IsmsRole(models.Model):
    _name = 'isms.role'
    _rec_name = 'isms_role_name'

    isms_role_name = fields.Char(string=_("Role Name"))
    isms_role_description = fields.Html(string=_("Role Description"))

class IsmsPeople(models.Model):
    _name = 'isms.people'
    _rec_name = 'isms_people_name'

    isms_people_name = fields.Char(string=_("People Name"))
    state = fields.Selection([
        ('draft','Draft'),
        ('approve','Approve')
    ], string="Status", default="draft")
    isms_people_description = fields.Html(string=_("ISMS Responsibilities"))
    isms_roles_ids = fields.Many2many('isms.role', string=_("ISMS Role"))
    isms_people_job_position = fields.Char(string=_("Job Position"))
    isms_people_email = fields.Char(string=_("Email"))

    def action_approve(self):
        for rec in self:
            rec.state = 'approve'
    
    def action_draft(self):
        for rec in self:
            rec.state = 'draft'