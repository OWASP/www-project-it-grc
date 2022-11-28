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
    it_file = fields.Binary(string='Diagram')
    #ii_id = fields.Many2one('data.inventory')
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
    data_file = fields.Binary(string='Data Flow')
    _sql_constraints = [('name_uniq', 'unique(name)', "The data inventory name already exists.")]

class ThirdParty(models.Model):
    _name = 'third.party'
    _decription = 'Third-Party'
    name = fields.Char(string='Third Party Vendor', required=True)
    description = fields.Text(string='Description', required=True)
    third_party_file = fields.Binary(string='Contract')
    _sql_constraints = [('name_uniq', 'unique(name)', "The third party name already exists.")]

class BusinessProcess(models.Model):
    _name = 'business.process'
    _decription = 'Business Process'
    name = fields.Char(string='Business Process', required=True)
    description = fields.Text(string='Description', required=True)
    process_file = fields.Binary(string='Process File')
    _sql_constraints = [('name_uniq', 'unique(name)', "The business process name already exists.")]

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
    name = fields.Char(string='Control Category', required=True)
    description = fields.Text(string='Description', required=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The control category name already exists.")]

class IsoControl(models.Model):
    _name = 'iso.control'
    _description = 'ISO Control'
    name = fields.Char(string='Control Title', required=True)
    control_category_id = fields.Many2one('control.category', string='Control Category', required=True)
    control_type_id = fields.Many2many('control.type', string='Control Type', required=True)
    security_property_id = fields.Many2many('security.property', string='Security Property', required=True)
    cybersecurity_concept_id = fields.Many2many('cybersecurty.concept', string='Cybersecurity Concept', required=True)
    operational_capability_id = fields.Many2many('operational.capability', string='Operational Capability', required=True)
    security_domain_id = fields.Many2many('security.domain', string='Security Domain', required=True)
    control = fields.Text(string='Control', required=True)
    purpose = fields.Text(string='Purpose', required=True)
    guidance = fields.Text(string='Guidance', required=True)
    other_information = fields.Text(string='Other Information', required=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The ISO control name already exists.")]

class StatementApplicability(models.Model):
    _name = 'statement.applicability'
    _description = 'Statement Applicability'

    name = fields.Many2one('iso.control', string='ISO Control', required=True)
    is_applicable = fields.Boolean(string='Control Applicable?', required=True)
    is_implemented = fields.Boolean(string='Control Implemented?', required=True)
    reason_selection = fields.Text(string='Reason for Selection')
    #risk reference
    business_process_id = fields.Many2many('business.process',string='Business Process')
    #evidence
    #control desing reference
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
    name = fields.Text(string='Risk Factor', required=True)
    risk_classification_id = fields.Many2many('risk.classification',string='Risk Classification', required=True)
    it_inventory_id = fields.Many2many('it.inventory',string='IT System')
    business_process_id = fields.Many2many('business.process',string='Business Process')

    cause = fields.Text(string='Cause', required=True)
    consequence = fields.Text(string='Consequence', required=True)
    impact_level_id = fields.Many2one('impact.level', string='Impact Level', required=True)
    probability_level_id = fields.Many2one('probability.level', string='Probability Level', required=True)
    responsible = fields.Many2one('res.users', string='IT Admin', required=True)
    quantification = fields.Float(string='Quantification')
    comment = fields.Text(string='Comment')
    risk_factor_file = fields.Binary(string='Upload File')
    risk_factor_file_name = fields.Char(string='File Name')

#--------------
# Control
#--------------
class ControlDesing(models.Model):
    _name = 'control.design'
    _description = 'Control Design'
    name = fields.Text(string='Control', required=True)
    responsible = fields.Many2one('res.users', string='Responsible', required=True)
    control_file = fields.Binary(string='Upload Evidence')
    control_file_name = fields.Char(string='Evidence Name')
    control_type_id = fields.Many2many('control.type', string='Control Type', required=True)
    security_property_id = fields.Many2many('security.property', string='Security Property', required=True)
    cybersecurity_concept_id = fields.Many2many('cybersecurty.concept', string='Cybersecurity Concept', required=True)
    operational_capability_id = fields.Many2many('operational.capability', string='Operational Capability', required=True)
    security_domain_id = fields.Many2many('security.domain', string='Security Domain', required=True)
    comment = fields.Text(string='Comment', required=True)


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
