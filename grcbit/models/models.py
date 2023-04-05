# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
from datetime import date
from statistics import mode

_logger = logging.getLogger(__name__)

#-------------------------------------
# Asset Management
#-------------------------------------

class DataClassification(models.Model):
    _name = 'data.classification'
    _description = 'Data Classification'
    name = fields.Char(string='Data Classification', required=True)
    description = fields.Text(string='Description')
    data_inventory_count = fields.Integer(string="Data Asset Count" )
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The data classification name already exists.")]

    @api.model
    def web_read_group(self, domain, fields, groupby, limit=None, offset=0, orderby=False,lazy=True, expand=False, expand_limit=None, expand_orderby=False):
        res = super().web_read_group(domain, fields, groupby, limit, offset, orderby, lazy, expand, expand_limit, expand_orderby)
        for i in self.env['data.classification'].search([]):
            data_assets = self.env['data.inventory'].search([('data_classification_id', 'in', [i.id] )])
            self.env['data.classification'].sudo().search([('id','=',i.id)]).sudo().write({'data_inventory_count':len(data_assets)})
        return res

class ItInventory(models.Model):
    _name = 'it.inventory'
    _description = 'IT Inventory'
    name = fields.Char(string='System Name', required=True)
    description = fields.Text(string='Description', required=True)
    ip = fields.Char(string='IP')
    url = fields.Char(string='URL')
    responsible = fields.Many2one('res.users', string='IT Admin', required=True)
    environment = fields.Selection([('prod', 'Production'), ('dev', 'Development'), ('stg','Staging')], string='Enviroment', required=True)
    is_cloud = fields.Boolean(string='Cloud Hosted?', required=True)
    #cloud_provider = fields.Char(string='Cloud Provider')
    cloud_provider = fields.Many2many('third.party',string='Third Party')
    is_internet_exposed = fields.Boolean(string='Internet Exposed?', required=True)
    users_qty = fields.Integer(string='User Quantity', required=True)
    os_version = fields.Char(string='OS Version')
    db_version = fields.Char(string='DB Version')
    attachment = fields.Many2many('ir.attachment', string="Attachment")
    #it_file = fields.Binary(string='Diagram')
    #it_file = fields.Many2many('ir.attachment', string="File")
    #it_file_name = fields.Char(string="File Name")
    #ii_id = fields.Many2one('data.inventory')
    #color = fields.Integer()
    data_inventory_count = fields.Integer(string="Data Asset Count")
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The IT system name already exists.")]

    @api.model
    def web_read_group(self, domain, fields, groupby, limit=None, offset=0, orderby=False,lazy=True, expand=False, expand_limit=None, expand_orderby=False):
        res = super().web_read_group(domain, fields, groupby, limit, offset, orderby, lazy, expand, expand_limit, expand_orderby)
        for i in self.env['it.inventory'].search([]):
            data_assets = self.env['data.inventory'].search([('it_inventory_id', 'in', [i.id] )])
            self.env['it.inventory'].sudo().search([('id','=',i.id)]).sudo().write({'data_inventory_count':len(data_assets)})
        return res


class DataInventory(models.Model):
    _name = 'data.inventory'
    _description = 'Data Inventory'
    name = fields.Char(string='Asset Name', required=True)
    description = fields.Text(string='Description', required=True)
    data_classification_id = fields.Many2one('data.classification', string='Data Classification', required=True)
    location = fields.Char(string='Location', required=True)
    owner = fields.Many2one('res.users', string='Asset Owner', required=True)
    #ii_id   = fields.One2many('it.inventory','ii_id', string='IT System')
    it_inventory_id = fields.Many2many('it.inventory',string='IT System')
    third_party_id = fields.Many2many('third.party',string='Third Party')
    #business_process_id = fields.Many2many('business.process',string='Business Process')
    document_page_id   = fields.Many2many('document.page', string='Business Process')
    security_requirement = fields.Text(string='Security Requirement', required=True)
    retention_period = fields.Selection([
        ('1m','1 month'),
        ('2m','2 months'),
        ('3m','3 months'),
        ('4m','4 months'),
        ('5m','5 months'),
        ('6m','6 months'),
        ('7m','7 months'),
        ('8m','8 months'),
        ('9m','9 months'),
        ('10m','10 months'),
        ('11m','11 months'),
        ('1y','1 year'),
        ('2y','2 years'),
        ('3y','3 years'),
        ('4y','4 years'),
        ('5y','5 years'),
        ])
    attachment = fields.Many2many('ir.attachment', string="Attachment")
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The data inventory name already exists.")]

    #@api.onchange('third_party_id')
    #def on_change_third_party(self):
    #    for i in self.env['third.party'].search([]):
    #        data_assets = self.env['data.inventory'].search([('third_party_id', 'in', [i.id] )])
    #        self.env['third.party'].search([('id','=',i.id)]).write({'data_count':len(data_assets)})


class ThirdParty(models.Model):
    _name = 'third.party'
    _decription = 'Third-Party'
    name = fields.Char(string='Third Party Vendor', required=True)
    description = fields.Text(string='Description', required=True)
    attachment = fields.Many2many('ir.attachment', string="Attachment")
    data_inventory_count = fields.Integer(string="Data Asset Count")
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The third party name already exists.")]

    @api.model
    def web_read_group(self, domain, fields, groupby, limit=None, offset=0, orderby=False,lazy=True, expand=False, expand_limit=None, expand_orderby=False):
        res = super().web_read_group(domain, fields, groupby, limit, offset, orderby, lazy, expand, expand_limit, expand_orderby)
        for i in self.env['third.party'].search([]):
            _logger.info('grcbitdebug:' + str(i))
            data_assets = self.env['data.inventory'].search([('third_party_id', 'in', [i.id] )])
            self.env['third.party'].sudo().search([('id','=',i.id)]).sudo().write({'data_inventory_count':len(data_assets)})
        return res


class BusinessProcess(models.Model):
    _name = 'business.process'
    _decription = 'Business Process'
    _order = 'process_id'
    #_rec_name = 'process_id'
    _rec_name = 'display_name'

    display_name = fields.Char(string='Business Process', compute='_compute_display_name')
    name = fields.Char(string='Business Process', required=True)
    process_id = fields.Char(string='ID', required=True, index=True, copy=False, default='New')
    description = fields.Text(string='Description', required=True)
    attachment      = fields.Many2many('ir.attachment', string="Attachment")
    #attachment_name = fields.Char(string='Attachment')
    data_inventory_count = fields.Integer(string="Data Asset Count")
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The business process name already exists.")]

    @api.model
    def web_read_group(self, domain, fields, groupby, limit=None, offset=0, orderby=False,lazy=True, expand=False, expand_limit=None, expand_orderby=False):
        res = super().web_read_group(domain, fields, groupby, limit, offset, orderby, lazy, expand, expand_limit, expand_orderby)
        #for i in self.env['business.process'].search([]):
        for i in self.env['document.page'].search([]):
            data_assets = self.env['data.inventory'].search([('document_page_id', 'in', [i.id] )])
            self.env['document_page'].sudo().search([('id','=',i.id)]).sudo().write({'data_inventory_count':len(data_assets)})
        return res

    @api.model
    def create(self, vals):
        vals['process_id'] = self.env['ir.sequence'].next_by_code('process.id.sequence')
        return super(BusinessProcess, self).create(vals)

    @api.depends('process_id','name')
    def _compute_display_name(self):
        for i in self:
            i.display_name = i.process_id + ' ' + i.name

class SecurityPolicy(models.Model):
    _name = 'security.policy'
    _decription = 'Security Policy'
    _order = 'security_policy_id'
    _rec_name = 'display_name'

    display_name = fields.Char(string='Security Policy', compute='_compute_display_name')
    name = fields.Char(string='Security Policy', required=True)
    security_policy_id = fields.Char(string='ID', required=True, index=True, copy=False, default='New')
    description = fields.Text(string='Description', required=True)
    attachment      = fields.Many2many('ir.attachment', string="Attachment")
    #attachment_name = fields.Char(string='Attachment')
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The security policy name already exists.")]

    @api.model
    def create(self, vals):
        vals['security_policy_id'] = self.env['ir.sequence'].next_by_code('security.policy.id.sequence')
        return super(SecurityPolicy, self).create(vals)

    @api.depends('security_policy_id','name')
    def _compute_display_name(self):
        for i in self:
            i.display_name = i.security_policy_id + ' ' + i.name

#--------------------------------------
# ISO 27001:2022 - Control Attributes
#--------------------------------------

class ControlType(models.Model):
    _name = 'control.type'
    _description = 'Data Inventory'
    name = fields.Char(string='Control Type', required=True)
    description = fields.Text(string='Description', required=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The control type name already exists.")]

class SecurityProperty(models.Model):
    _name = 'security.property'
    _description = 'Data Inventory'
    name = fields.Char(string='Security Property', required=True)
    description = fields.Text(string='Description', required=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The security property name already exists.")]

class CybersecurityConcept(models.Model):
    _name = 'cybersecurity.concept'
    _description = 'Data Inventory'
    name = fields.Char(string='Cybersecurity Concept', required=True)
    description = fields.Text(string='Description', required=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The cybersecurty concept name already exists.")]

class OperationalCapability(models.Model):
    _name = 'operational.capability'
    _description = 'Data Inventory'
    name = fields.Char(string='Operational Capability', required=True)
    description = fields.Text(string='Description', required=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The operational capability name already exists.")]

class SecurityDomain(models.Model):
    _name = 'security.domain'
    _description = 'Data Inventory'
    name = fields.Char(string='Security Domain', required=True)
    description = fields.Text(string='Description', required=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The security domain name already exists.")]

#--------------------------
# ISO 27001:2022 - Controls
#--------------------------

class ControlCategory(models.Model):
    _name = 'control.category'
    _description = 'Control Category'
    _rec_name = 'display_name'

    display_name = fields.Char(string='Control Category', compute='_compute_display_name')
    id_control_category = fields.Char(string='ID Control Category', required=True)
    name = fields.Char(string='Control Category', required=True)
    description = fields.Text(string='Description' )
    statement_applicability_count = fields.Integer(string='Statement Applicability Acount')
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The control category name already exists."), ('id_control_category_uniq', 'unique(id_control_category)', "The control category ID already exists.")]

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
    _order = 'id_iso_control'

    _rec_name = 'display_name'
    id_iso_control      = fields.Char(string='ID ISO Control', required=True)
    #id_iso_control_num = fields.Float(string='ID ISO Control', compute='_compute_id_iso_control_num')
    name = fields.Char(string='Control Title', required=True)
    display_name = fields.Char(string='Control Title', compute='_compute_display_name')
    control_category_id = fields.Many2one('control.category', string='Control Category', required=True)
    control_type_id = fields.Many2many('control.type', string='Control Type', required=True)
    security_property_id = fields.Many2many('security.property', string='Security Property', required=True)
    cybersecurity_concept_id = fields.Many2many('cybersecurity.concept', string='Cybersecurity Concept', required=True)
    operational_capability_id = fields.Many2many('operational.capability', string='Operational Capability', required=True)
    security_domain_id = fields.Many2many('security.domain', string='Security Domain', required=True)
    control = fields.Text(string='Control', required=True)
    purpose = fields.Text(string='Purpose', required=True)
    guidance = fields.Text(string='Guidance', required=True)
    other_information = fields.Text(string='Other Information')
    attachment = fields.Many2many('ir.attachment', string="Attachment")
    #consultant = fields.Many2one('res.users', string='Consultant')
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The ISO control name already exists."), ('id_iso_control_uniq', 'unique(id_iso_control)', "The ISO control ID already exists.")]

    @api.depends('id_iso_control','name')
    def _compute_display_name(self):
        for i in self:
            i.display_name = str(i.id_iso_control) + ' ' + i.name
   
    '''
    @api.depends('id_iso_control')
    def _compute_id_iso_control_num(self):
        _logger.info('grcbit_info ' + str(self))
        for r in self:
            #_logger.info('grcbit_info ' + str(r.id_iso_control))
            r.id_iso_control_num = float(r.id_iso_control) #.write({'': r.id_iso_control})  #r.id_iso_control
            #self.env['iso.control'].search([('id','=',r.id)]).write({'id_iso_control_num':1.11})
            #self.write({'id_iso_control_num':1.11})
    '''

class StatementApplicability(models.Model):
    _name = 'statement.applicability'
    _description = 'Statement Applicability'
    _order = 'name'

    name = fields.Many2one('iso.control', string='ISO Control', required=True)
    is_applicable = fields.Boolean(string='Is Applicable?', required=True)
    #is_implemented = fields.Boolean(string='Control Implemented?', required=True)
    reason_selection = fields.Text(string='Reason for Selection')
    #risk reference
    #business_process_id = fields.Many2many('business.process',string='Policy / Process')
    #security_policy_id = fields.Many2many('security.policy',string='Policy')
    document_page_id   = fields.Many2many('document.page', string='Policy')
    control_design_id  = fields.Many2many('control.design',string='Control')
    control_status     = fields.Integer(string='Status', readonly=True) #(related='control_design_id.state', store=True)
    #risk_factor_id = fields.Many2many('risk.factor', string='Factor Riesgo') 
    #evidence_file = fields.Binary(string='Upload Evidence')
    #evidence_file = fields.Many2many('ir.attachment', string="File")
    #evidence_file_name = fields.Char(string='Evidence Name')
    attachment = fields.Many2many('ir.attachment', string="Attachment")
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The control name already exists.")]

#------------------------
# Risk Management
#------------------------

class ImpactLevel(models.Model):
    _name = 'impact.level'
    _description = 'Impact Level'
    name = fields.Char(string='Impact Level', required=True)
    description = fields.Text(string='Description', required=True)
    value = fields.Integer(string='Value', required=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The impact level name already exists."),('level_uniq', 'unique(value)', "The impact level value already exists.")]

class ProbabilityLevel(models.Model):
    _name = 'probability.level'
    _description = 'Probability Level'
    name = fields.Char(string='Probability Level', required=True)
    description = fields.Text(string='Description', required=True)
    value = fields.Integer(string='Value', required=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The probability level name already exists."),('level_uniq', 'unique(value)', "The probability level value already exists.")]

class RiskLevel(models.Model):
    _name = 'risk.level'
    _description = 'Risk Level'
    name = fields.Char(string='Risk Level', required=True)
    description = fields.Text(string='Description')
    value = fields.Integer(string='Value', required=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The risk level name already exists."),('level_uniq', 'unique(value)', "The risk level value already exists.")]

class InherentRiskLevel(models.Model):
    _name = 'inherent.risk.level'
    _description = 'Inherent Risk Level'
    #name = fields.Char(string='Risk Level', required=True)
    #description = fields.Text(string='Description', required=True)
    impact_level_id      = fields.Many2one('impact.level', string='Impact Level')
    probability_level_id = fields.Many2one('probability.level', string='Probability Level')
    risk_level_id        = fields.Many2one('risk.level', string='Risk Level')
    risk_level_name      = fields.Char(related='risk_level_id.name', string='Risk Level')
    description = fields.Text(string='Description', required=True)
    color = fields.Integer(string='Color')
    active = fields.Boolean(default=True)

class RiskClassification(models.Model):
    _name = 'risk.classification'
    _description = 'Risk Classification'
    name = fields.Char(string='Risk Classification', required=True)
    description = fields.Text(string='Description', required=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The risk classification name already exists.")]

class RiskFactor(models.Model):
    _name = 'risk.factor'
    _inherit = 'mail.thread'
    _description = 'Risk Factor'
    _order = 'risk_id'
    _rec_name = 'display_name'

    display_name = fields.Char(string='Control Category', compute='_compute_display_name')
    name = fields.Text(string='Risk Factor', required=True)
    risk_id = fields.Char(string='Risk ID', required=True, index=True, copy=False, default='New')
    risk_classification_id = fields.Many2many('risk.classification',string='Risk Classification', required=True)
    #it_inventory_id = fields.Many2many('it.inventory',string='IT System')
    #business_process_id = fields.Many2many('business.process',string='Policy / Process')
    data_inventory_id = fields.Many2many('data.inventory',string='Data Asset', track_visibility='always')

    cause = fields.Text(string='Cause', required=True)
    consequence = fields.Text(string='Consequence', required=True)
    impact_level_id = fields.Many2one('impact.level', string='Impact Level', required=True, track_visibility='always')
    probability_level_id = fields.Many2one('probability.level', string='Probability Level', required=True, track_visibility='always')
    responsible = fields.Many2one('res.users', string='Risk Owner', required=True, track_visibility='always')
    quantification = fields.Float(string='Quantification', track_visibility='always')
    inherent_risk  = fields.Char(string='Inherent Risk', track_visibility='always')
    residual_risk  = fields.Char(string='Residual Risk', track_visibility='always')
    #comment = fields.Text(string='Comment')
    #risk_factor_file = fields.Many2many('ir.attachment', string="File")
    #risk_factor_file = fields.Binary(string='Upload File')
    #risk_factor_file_name = fields.Char(string='File Name')
    attachment = fields.Many2many('ir.attachment', string="Attachment")
    #control_design_id = fields.Many2many('control.design',string='Control Design')
    active = fields.Boolean(default=True)

    @api.model
    def create(self, vals):
        vals['risk_id'] = self.env['ir.sequence'].next_by_code('risk.id.sequence')
        return super(RiskFactor, self).create(vals)

    @api.depends('risk_id','name')
    def _compute_display_name(self):
        for i in self:
            i.display_name = i.risk_id + ' ' + i.name

    @api.onchange('probability_level_id','impact_level_id')
    def _compute_inherent_risk(self):
        self.sudo().write({'inherent_risk': self.env['inherent.risk.level'].search([('probability_level_id','=',self.probability_level_id.id), ('impact_level_id','=',self.impact_level_id.id)]).risk_level_name})
        #for i in self:
        #    ir = self.env['risk.level'].search([('probability_level_id','=',i.probability_level_id.id), ('impact_level_id','=',i.impact_level_id.id)]).name
        #    i.sudo().write({'inherent_risk': str(ir)}) 

#--------------
# Control
#--------------
class ControlDesing(models.Model):
    _name = 'control.design'
    _inherit = 'mail.thread'

    _description = 'Control Design'
    _order = 'control_id'
    #_rec_name = 'control_id'
    _rec_name = 'display_name'

    state = fields.Selection([
        ('draft','Draft'),                             #25 %
        ('designed','Designed'),                       #50 %
        ('implemented','Implemented'),                 #75 %
        ('approved','Approved'),],                       #100%
        string='Status', default='draft', readonly=True, copy=False, tracking=True, track_visibility='always')
        #('in_progress','Implementation in Progress'), 
        #('audited','Audited'),],
    
    #evaluation_design = fields.Selection([
    #    ('',''),
    #    ('',''),
    #    ('',''),
    #    ('',''),
    #    ],
    #    string='Evaluation Design', )
 
    control_id = fields.Char(string='Control ID', required=True, index=True, copy=False, default='New')
    risk_factor_id = fields.Many2many('risk.factor',string='Risk Factor', track_visibility='always')
    display_name = fields.Char(string='Control Category', compute='_compute_display_name')
    name = fields.Char(string='Nombre', required=True)
    #control_id = fields.Char(string='Control ID', required=True, index=True, copy=False, default='New')
    #control = fields.Text(string='Control', required=True)
    control_line_ids = fields.One2many('control.line', 'control_design_id', string='Control Guide')
    estimated_date = fields.Date(string='Estimated Date')
    description = fields.Text(string='Description/Objective', required=True)
    evidence_guide = fields.Text(string='Evidence Guide')
    #control_id = fields.Char(string='Control ID', required=True, index=True, copy=False, default='New')
    #evidence_guide = fields.Text(string='Evidence Guide', required=True)
    responsible = fields.Many2one('res.users', string='Responsible', required=True, track_visibility='always')
    #control_file = fields.Binary(string='Upload Evidence')
    #control_file = fields.Many2many('ir.attachment', string="File")
    #control_file_name = fields.Char(string='Evidence Name')
    is_key_control = fields.Boolean(string='Key Control', track_visibility='always')
    control_type_id = fields.Many2many('control.type', string='Control Type', required=True)
    security_property_id = fields.Many2many('security.property', string='Security Property', required=True)
    cybersecurity_concept_id = fields.Many2many('cybersecurity.concept', string='Cybersecurity Concept', required=True)
    operational_capability_id = fields.Many2many('operational.capability', string='Operational Capability', required=True)
    security_domain_id = fields.Many2many('security.domain', string='Security Domain', required=True)
    comment = fields.Text(string='Comment')
    evidence_pending = fields.Text(string='Evidence Pending')
    #attachment = fields.Many2many('ir.attachment', string="Attachment")
    active = fields.Boolean(default=True)
    control_evidence_ids = fields.One2many('control.evidence', 'control_design_id')
    control_evaluation_criteria_id = fields.Many2one('control.evaluation.criteria', string='Implementation Criteria')
    control_design_criteria_id = fields.Many2one('control.design.criteria', string='Design Criteria')
    design_date = fields.Date(string='Design Date', readonly=True)
    implementation_date = fields.Date(string='Implementation Date', readonly=True)
    approve_date = fields.Date(string='Approve Date', readonly=True)

    #@api.onchange('state')
    #def _set_status_control_statement_applicability(self):
    #    _logger.info('grcbit_debug: ' + str(self))
    #    for i in self:
    #        statement = self.env['statement.applicability'].search([('control_design_id','=',i.id)]) #.write({'control_status':i.state})
    #        _logger.info('grcbit_debug: ' + str(statement))

    @api.model
    def create(self, vals):
        vals['control_id'] = self.env['ir.sequence'].next_by_code('control.id.sequence')
        return super(ControlDesing, self).create(vals)

    @api.depends('control_id','name')
    def _compute_display_name(self):
        for i in self:
            i.display_name = i.control_id + ' ' + i.name

    def action_draft(self):
        self.state = 'draft'
        self.design_date = '' #date.today()
        self.implementation_date = '' #date.today()
        self.approve_date = '' #date.today()
        self._status_control(self.id)
        self.sudo()._residual_risk(self.id, self.control_evaluation_criteria_id)
    def action_design(self):
        self.state = 'designed'
        self.design_date = date.today()
        self._status_control(self.id)
    #def action_in_progress(self):
    #    self.state = 'in_progress'
    #    self._status_control(self.id)
    def action_implemented(self):
        self.sudo().state = 'implemented'
        self.sudo().implementation_date = date.today()
        self.sudo()._status_control(self.id)
        #self.sudo()._residual_risk(self.id)
    #def action_not_approved(self):
        #self.sudo().state = 'implemented'
        #self.sudo().implementation_date = date.today()
        #self.sudo()._status_control(self.id)
    def action_approved(self):
        self.state = 'approved'
        self.approve_date = date.today()
        self._status_control(self.id)
        self.sudo()._residual_risk(self.id, self.control_evaluation_criteria_id)
    #def action_audited(self):
    #    self.state = 'audited'

    def _residual_risk(self, control_id, control_eval):
        risk_factor_ids    = self.env['control.design'].search([('id','=',control_id)]).risk_factor_id

        for i in risk_factor_ids:
            control_eval_ids = self.env['control.design'].search([('risk_factor_id','in',i.id), ('state','=','implemented') ]).control_evaluation_criteria_id
            #control_eval_ids = self.env['control.design'].search([('risk_factor_id','in',risk_factor_ids.ids), ('state','=','implemented') ]).control_evaluation_criteria_id
            if control_eval_ids:
                _logger.info('grcbit_040423: ' + str(control_eval_ids))
                m=[]
                for c in control_eval_ids:
                    m.append(c.id)
                control_eval_mode=mode(m)
                _logger.info('grcbit_040423_m: ' + str(m))
                _logger.info('grcbit_040423_mode: ' + str(control_eval_mode))

        #for i in risk_factor_ids:
                for r in self.env['risk.factor'].search([('id','=',i.id)]):
                    ir = self.env['risk.level'].search([('name','=',r.inherent_risk)]).id
                #residual_risk = self.env['residual.risk.level'].search([('control_evaluation_criteria_id','=',control_eval.id), ('inherent_risk_level_id','=',ir)]).residual_risk_level_name
                    residual_risk = self.env['residual.risk.level'].search([('control_evaluation_criteria_id','=',control_eval_mode), ('inherent_risk_level_id','=',ir)]).residual_risk_level_name
                    r.write({'residual_risk':residual_risk})
            else:
                self.env['risk.factor'].search([('id','=',i.id)]).write({'residual_risk':''})
                #r.write({'residual_risk':''})

    def _status_control(self, statement):
        statement_record = self.env['statement.applicability'].search([('control_design_id','=',statement)]) 
        for s in statement_record:
            status = 0
            for i in s.control_design_id:
                state = self.env['control.design'].search([('id','=',i.id)]).state
                if state == 'draft':
                    status += 25
                if state == 'designed':
                    status += 50
                #if state == 'in_progress':
                #    status += 50
                if state == 'implemented':
                    status += 75
                if state == 'approved':
                    status += 100
            s.write({'control_status':status / len(s.control_design_id)})

class ControlEvidence(models.Model):
    _name = 'control.evidence'
    _description = 'Control Evidence'
    #_order = 'control_evidence_id'
    #_rec_name = 'display_name'

    #display_name = fields.Char(string='Control Category', compute='_compute_display_name')
    name = fields.Char(string='Name', required=True)
    attachment = fields.Many2many('ir.attachment', string="Attachment")
    comment = fields.Html(string='Comment/Description')
    control_design_id = fields.Many2one('control.design')
    active = fields.Boolean(default=True)

class ControlLine(models.Model):
    _name = 'control.line'
    _description = 'Control Line'

    name = fields.Char(string='Name', required=True)
    description = fields.Html(string='Description')
    attachment = fields.Many2many('ir.attachment', string="Attachment")
    is_implemented = fields.Boolean(string="Is Implemented?")
    control_design_id = fields.Many2one('control.design')
    active = fields.Boolean(default=True)
    control_periodicity = fields.Selection([
        ('1m','1 month'),
        ('2m','2 months'),
        ('3m','3 months'),
        ('4m','4 months'),
        ('5m','5 months'),
        ('6m','6 months'),
        ('7m','7 months'),
        ('8m','8 months'),
        ('9m','9 months'),
        ('10m','10 months'),
        ('11m','11 months'),
        ('1y','1 year'),
        ('pe','Per event'),
        ], required=True)

class ControlEvaluationCriteria(models.Model):
    _name = 'control.evaluation.criteria'
    _description = 'Implementation Criteria'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(default=True)

class ControlDesignCriteria(models.Model):
    _name = 'control.design.criteria'
    _description = 'Design Criteria'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(default=True)

class ResidualRiskLevel(models.Model):
    _name = 'residual.risk.level'
    _description = 'Residual Risk Level'

    inherent_risk_level_id   = fields.Many2one('risk.level',   string='Inherent Risk', required=True)
    control_evaluation_criteria_id          = fields.Many2one('control.evaluation.criteria', string='Implementation Criteria', required=True)
    residual_risk_level_id   = fields.Many2one('risk.level',   string='Residual Risk', required=True)
    residual_risk_level_name = fields.Char(related='residual_risk_level_id.name', string='Residual Risk', required=True)
    active = fields.Boolean(default=True)

#-------------
# Compliance
#-------------
class ComplianceVersion(models.Model):
    _name = 'compliance.version'
    _description = 'Compliance Version'

    name = fields.Char(string='Compliance Version', required=True)
    description  = fields.Text(string='Description')
    _sql_constraints = [('name_uniq', 'unique(name)', "The compliance version name already exists.")]

class ComplianceControlObjective(models.Model):
    _name = 'compliance.control.objective'
    _description = 'Compliance Objective'
    _rec_name = 'display_name'

    name = fields.Char(string='Compliance Objective', required=True)
    display_name = fields.Char(string='Compliance Objective', compute='_compute_display_name')
    compliance_version_id = fields.Many2one('compliance.version', string='Compliance Version', required=True)
    description  = fields.Text(string='Description')
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
            #i.display_name = str(i.compliance_control_objective_id.name) + ' - ' + str(i.compliance_control_objective_id.compliance_version_id.name) + ' - ' + i.name

class ComplianceIsoControl(models.Model):
    _name = 'compliance.iso.control'
    _description = 'Conompliance - ISO 27001'

    compliance_control_id = fields.Many2one('compliance.control', string='Compliance Requirement', required=True)
    iso_control_id = fields.Many2one('iso.control', string='ISO 27001', required=True)
    description  = fields.Text(string='Description')
    

#class ControlDesignEvaluation(models.Model):
#    _name = 'control.design.evaluation'
#    _description = 'Control Design Evaluation'
#    _
# class grcbit(models.Model):
#     _name = 'grcbit.grcbit'
#     _description = 'grcbit.grcbit'
#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
