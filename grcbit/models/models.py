# -*- coding: utf-8 -*-

from odoo import models, fields, api

#-------------------------------------
# Asset Management
#-------------------------------------

class DataClassification(models.Model):
    _name = 'data.classification'
    _description = 'Data Classification'
    name = fields.Char(string='Data Classification', required=True)
    description = fields.Text(string='Description')
    _sql_constraints = [('name_uniq', 'unique(name)', "The data classification name already exists.")]

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
    _sql_constraints = [('name_uniq', 'unique(name)', "The IT system name already exists.")]

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
    business_process_id = fields.Many2many('business.process',string='Business Process')
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
    #data_file = fields.Binary(string='Data Flow')
    #data_file = fields.Many2many('ir.attachment', string="File")
    #data_file_name = fields.Char(string="File Name")
    attachment = fields.Many2many('ir.attachment', string="Attachment")
    _sql_constraints = [('name_uniq', 'unique(name)', "The data inventory name already exists.")]

'''
class DataInventoryTags(models.Model):
    _name = 'data.inventory.tags'
    color = fields.Integer()

class ItInventoryTags(models.Model):
    _name = 'it.inventory.tags'
    color = fields.Integer()
'''

class ThirdParty(models.Model):
    _name = 'third.party'
    _decription = 'Third-Party'
    name = fields.Char(string='Third Party Vendor', required=True)
    description = fields.Text(string='Description', required=True)
    #third_party_file = fields.Binary(string='Contract')
    #third_party_file = fields.Many2many('ir.attachment', string="File")
    #third_party_file_name = fields.Char(string="File Name")
    attachment = fields.Many2many('ir.attachment', string="Attachment")
    _sql_constraints = [('name_uniq', 'unique(name)', "The third party name already exists.")]

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
    _sql_constraints = [('name_uniq', 'unique(name)', "The business process name already exists.")]

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
    _sql_constraints = [('name_uniq', 'unique(name)', "The control type name already exists.")]

class SecurityProperty(models.Model):
    _name = 'security.property'
    _description = 'Data Inventory'
    name = fields.Char(string='Security Property', required=True)
    description = fields.Text(string='Description', required=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The security property name already exists.")]

class CybersecurityConcept(models.Model):
    _name = 'cybersecurity.concept'
    _description = 'Data Inventory'
    name = fields.Char(string='Cybersecurity Concept', required=True)
    description = fields.Text(string='Description', required=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The cybersecurty concept name already exists.")]

class OperationalCapability(models.Model):
    _name = 'operational.capability'
    _description = 'Data Inventory'
    name = fields.Char(string='Operational Capability', required=True)
    description = fields.Text(string='Description', required=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The operational capability name already exists.")]

class SecurityDomain(models.Model):
    _name = 'security.domain'
    _description = 'Data Inventory'
    name = fields.Char(string='Security Domain', required=True)
    description = fields.Text(string='Description', required=True)
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
    _sql_constraints = [('name_uniq', 'unique(name)', "The control category name already exists."), ('id_control_category_uniq', 'unique(id_control_category)', "The control category ID already exists.")]

    @api.depends('id_control_category','name')
    def _compute_display_name(self):
        for i in self:
            i.display_name = i.id_control_category + ' ' + i.name

class IsoControl(models.Model):
    _name = 'iso.control'
    _description = 'ISO Control'
    _order = 'id_iso_control'
    _rec_name = 'display_name'
    id_iso_control = fields.Char(string='ID ISO Control', required=True)
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
    other_information = fields.Text(string='Other Information', required=True)
    attachment = fields.Many2many('ir.attachment', string="Attachment")
    consultant = fields.Many2one('res.users', string='Consultant')

    _sql_constraints = [('name_uniq', 'unique(name)', "The ISO control name already exists."), ('id_iso_control_uniq', 'unique(id_iso_control)', "The ISO control ID already exists.")]

    @api.depends('id_iso_control','name')
    def _compute_display_name(self):
        for i in self:
            i.display_name = i.id_iso_control + ' ' + i.name


class StatementApplicability(models.Model):
    _name = 'statement.applicability'
    _description = 'Statement Applicability'
    _order = 'name'

    name = fields.Many2one('iso.control', string='ISO Control', required=True)
    is_applicable = fields.Boolean(string='Control Applicable?', required=True)
    is_implemented = fields.Boolean(string='Control Implemented?', required=True)
    reason_selection = fields.Text(string='Reason for Selection')
    #risk reference
    #business_process_id = fields.Many2many('business.process',string='Policy / Process')
    security_policy_id = fields.Many2many('security.policy',string='Security Policy')
    control_design_id = fields.Many2many('control.design',string='Control Design')
    #risk_factor_id = fields.Many2many('risk.factor', string='Factor Riesgo') 
    #evidence_file = fields.Binary(string='Upload Evidence')
    #evidence_file = fields.Many2many('ir.attachment', string="File")
    #evidence_file_name = fields.Char(string='Evidence Name')
    attachment = fields.Many2many('ir.attachment', string="Attachment")
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
    _sql_constraints = [('name_uniq', 'unique(name)', "The impact level name already exists."),('level_uniq', 'unique(value)', "The impact level value already exists.")]

class ProbabilityLevel(models.Model):
    _name = 'probability.level'
    _description = 'Probability Level'
    name = fields.Char(string='Probability Level', required=True)
    description = fields.Text(string='Description', required=True)
    value = fields.Integer(string='Value', required=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The probability level name already exists."),('level_uniq', 'unique(value)', "The probability level value already exists.")]

class RiskClassification(models.Model):
    _name = 'risk.classification'
    _description = 'Risk Classification'
    name = fields.Char(string='Risk Classification', required=True)
    description = fields.Text(string='Description', required=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The risk classification name already exists.")]

class RiskFactor(models.Model):
    _name = 'risk.factor'
    _description = 'Risk Factor'
    _order = 'risk_id'
    _rec_name = 'display_name'

    display_name = fields.Char(string='Control Category', compute='_compute_display_name')
    name = fields.Text(string='Risk Factor', required=True)
    risk_id = fields.Char(string='Risk ID', required=True, index=True, copy=False, default='New')
    risk_classification_id = fields.Many2many('risk.classification',string='Risk Classification', required=True)
    #it_inventory_id = fields.Many2many('it.inventory',string='IT System')
    #business_process_id = fields.Many2many('business.process',string='Policy / Process')
    data_inventory_id = fields.Many2many('data.inventory',string='Data Asset')

    cause = fields.Text(string='Cause', required=True)
    consequence = fields.Text(string='Consequence', required=True)
    impact_level_id = fields.Many2one('impact.level', string='Impact Level', required=True)
    probability_level_id = fields.Many2one('probability.level', string='Probability Level', required=True)
    responsible = fields.Many2one('res.users', string='Risk Owner', required=True)
    quantification = fields.Float(string='Quantification')
    comment = fields.Text(string='Comment')
    #risk_factor_file = fields.Many2many('ir.attachment', string="File")
    #risk_factor_file = fields.Binary(string='Upload File')
    #risk_factor_file_name = fields.Char(string='File Name')
    attachment = fields.Many2many('ir.attachment', string="Attachment")
    #control_design_id = fields.Many2many('control.design',string='Control Design')

    @api.model
    def create(self, vals):
        vals['risk_id'] = self.env['ir.sequence'].next_by_code('risk.id.sequence')
        return super(RiskFactor, self).create(vals)

    @api.depends('risk_id','name')
    def _compute_display_name(self):
        for i in self:
            i.display_name = i.risk_id + ' ' + i.name

#--------------
# Control
#--------------
class ControlDesing(models.Model):
    _name = 'control.design'
    _description = 'Control Design'
    _order = 'control_id'
    #_rec_name = 'control_id'
    _rec_name = 'display_name'

    risk_factor_id = fields.Many2many('risk.factor',string='Risk Factor')
    display_name = fields.Char(string='Control Category', compute='_compute_display_name')
    name = fields.Text(string='Control', required=True)
    control_id = fields.Char(string='Control ID', required=True, index=True, copy=False, default='New')
    description = fields.Text(string='Description', required=True)
    evidence_guide = fields.Text(string='Evidence Guide', required=True)
    responsible = fields.Many2one('res.users', string='Responsible', required=True)
    #control_file = fields.Binary(string='Upload Evidence')
    #control_file = fields.Many2many('ir.attachment', string="File")
    #control_file_name = fields.Char(string='Evidence Name')
    control_type_id = fields.Many2many('control.type', string='Control Type', required=True)
    security_property_id = fields.Many2many('security.property', string='Security Property', required=True)
    cybersecurity_concept_id = fields.Many2many('cybersecurity.concept', string='Cybersecurity Concept', required=True)
    operational_capability_id = fields.Many2many('operational.capability', string='Operational Capability', required=True)
    security_domain_id = fields.Many2many('security.domain', string='Security Domain', required=True)
    comment = fields.Text(string='Comment')
    evidence_pending = fields.Text(string='Evidence Pending')
    attachment = fields.Many2many('ir.attachment', string="Attachment")

    @api.model
    def create(self, vals):
        vals['control_id'] = self.env['ir.sequence'].next_by_code('control.id.sequence')
        return super(ControlDesing, self).create(vals)

    @api.depends('control_id','name')
    def _compute_display_name(self):
        for i in self:
            i.display_name = i.control_id + ' ' + i.name

# class grcbit(models.Model):
#     _name = 'grcbit.grcbit'
#     _description = 'grcbit.grcbit'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
