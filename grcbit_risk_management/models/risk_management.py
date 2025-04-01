# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
from datetime import date
from statistics import mode

_logger = logging.getLogger(__name__)

class ImpactLevel(models.Model):
    _name = 'impact.level'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Impact Level'

    name = fields.Char(string=_('Impact Level'), required=True, help="Classification system that categorizes the potential impact of a security breach on the confidentiality, integrity, or availability of information.")
    description = fields.Text(string=_('Description'), required=True, help="Classification system that categorizes the potential impact of a security breach on the confidentiality, integrity, or availability of information.")
    value = fields.Integer(string=_('Value'), required=True, help="Classification system that categorizes the potential impact of a security breach on the confidentiality, integrity, or availability of information.")
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', _("The impact level name already exists.")),('level_uniq', 'unique(value)', _("The impact level value already exists."))]

class ProbabilityLevel(models.Model):
    _name = 'probability.level'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Probability Level'

    name = fields.Char(string=_('Probability Level'), required=True, help="Likelihood that a threat will be able to exploit a vulnerability in a given period of time.")
    description = fields.Text(string=_('Description'), required=True, help="Likelihood that a threat will be able to exploit a vulnerability in a given period of time.")
    value = fields.Integer(string=_('Value'), required=True, help="Likelihood that a threat will be able to exploit a vulnerability in a given period of time.")
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', _("The probability level name already exists.")),('level_uniq', 'unique(value)', _("The probability level value already exists."))]

class RiskLevel(models.Model):
    _name = 'risk.level'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Risk Level'

    name = fields.Char(string=_('Risk Level'), required=True, help="Measure of how much risk someone is willing to take on in order to achieve a certain reward.")
    description = fields.Text(string=_('Description'), required=True, help="Measure of how much risk someone is willing to take on in order to achieve a certain reward.")
    value = fields.Integer(string=_('Value'), required=True, help="Measure of how much risk someone is willing to take on in order to achieve a certain reward.")
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', _("The risk level name already exists.")),('level_uniq', 'unique(value)', _("The risk level value already exists."))]

class InherentRiskLevel(models.Model):
    _name = 'inherent.risk.level'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Inherent Risk Level'
    _rec_name = 'risk_level_name'

    impact_level_id      = fields.Many2one('impact.level', string=_('Impact Level'), required=True, help="Classification system that categorizes the potential impact of a security breach on the confidentiality, integrity, or availability of information.")
    probability_level_id = fields.Many2one('probability.level', string=_('Probability Level'), required=True, help="Likelihood that a threat will be able to exploit a vulnerability in a given period of time.")
    risk_level_id        = fields.Many2one('risk.level', string=_('Risk Level'), required=True, help="Measure of how much risk someone is willing to take on in order to achieve a certain reward.")
    risk_level_name      = fields.Char(related='risk_level_id.name', string=_('Risk Level'), required=True)
    description = fields.Text(string=_('Description'), required=True)
    color = fields.Integer(string=_('Color'))
    active = fields.Boolean(default=True)

class RiskClassification(models.Model):
    _name = 'risk.classification'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Risk Classification'

    name = fields.Char(string=_('Risk Classification'), required=True, help="Way to classify risks based on different activities an organization or business may perform.")
    description = fields.Text(string=_('Description'), required=True, help="Way to classify risks based on different activities an organization or business may perform.")
    active = fields.Boolean(default=True)
    company_risk_count = fields.Integer(string=_("Company Risk Count"))
    _sql_constraints = [('name_uniq', 'unique(name)', _("The risk classification name already exists."))]

    @api.model
    def web_read_group(self, domain, fields, groupby, limit=None, offset=0, orderby=False,lazy=True, expand=False, expand_limit=None, expand_orderby=False):
        res = super().web_read_group(domain, fields, groupby, limit, offset, orderby, lazy, expand, expand_limit, expand_orderby)
        for i in self.env['risk.classification'].search([]):
            _logger.info('grcbitdebug:' + str(i))
            company_risk = self.env['company.risk'].search([('risk_classification', 'in', [i.id] )])
            self.env['risk.classification'].sudo().search([('id','=',i.id)]).sudo().write({'company_risk_count':len(company_risk)})
        return res

class RiskFactor(models.Model):
    _name = 'risk.factor'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Risk Factor'
    _order = 'risk_id'
    _rec_name = 'display_name'

    display_name = fields.Char(string=_('Control Category'), compute='_compute_display_name', required=True)
    name = fields.Text(string=_('Risk Factor'), required=True, help="Collective name for circumstances affecting the likelihood or impact of a security risk.")
    risk_id = fields.Char(string=_('Risk ID'), required=True, index=True, copy=False, default='New')
    # risk_classification_id = fields.Many2many('risk.classification',string=_('Risk Classification'), required=True)
    data_inventory_id = fields.Many2many('data.inventory',string=_('Data Asset'), track_visibility='always')
    it_inventory_id = fields.Many2one('it.inventory',string=_('IT Inventory'), track_visibility='always')
    company_risk_ids = fields.Many2many('company.risk', string=_("Company Risk"), track_visibility="always")
    # cause = fields.Html(string=_('Cause'), required=True)
    consequence = fields.Html(string=_('Consequence'), required=True, help="Effect (change or non-change), usually associated with an event or condition or with the system and usually allowed, facilitated, caused, prevented, changed, or contributed to by the event, condition, or system.")
    impact_level_id = fields.Many2one('impact.level', string=_('Impact Level'), required=True, track_visibility='always', help="Classification system that categorizes the potential impact of a security breach on the confidentiality, integrity, or availability of information.")
    probability_level_id = fields.Many2one('probability.level', string=_('Probability Level'), required=True, track_visibility='always', help="Likelihood that a threat will be able to exploit a vulnerability in a given period of time.")
    responsible = fields.Many2one('hr.employee', string=_('Risk Owner'), required=True, track_visibility='always')
    quantification = fields.Float(string=_('Quantification'), track_visibility='always', required=True, help="Process that measures and evaluates the potential impact of a risk on a business, often in terms of dollars.")
    inherent_risk  = fields.Char(string=_('Inherent Risk'), track_visibility='always')
    residual_risk  = fields.Char(string=_('Residual Risk'), track_visibility='always')
    attachment = fields.Many2many('ir.attachment', string=_("Attachment"))
    active = fields.Boolean(default=True)
    inherent_factor_low = fields.Integer(string=_("Inherent Count"))
    inherent_factor_medium = fields.Integer(string=_("Inherent Count"))
    inherent_factor_high = fields.Integer(string=_("Inherent Count"))
    residual_risk_count = fields.Integer(string=_("Residual count"))
    risk_factor_company_risk_ids = fields.One2many('risk.factor.company.risk','risk_factor_id', auto_join=True, string='Company Risk')

    @api.model
    def create(self, vals):
        vals['risk_id'] = self.env['ir.sequence'].next_by_code('risk.id.sequence')
        return super(RiskFactor, self).create(vals)

    @api.depends('risk_id', 'name')
    def _compute_display_name(self):
        for i in self:
            i.display_name = i.risk_id + ' ' + i.name

    @api.onchange('probability_level_id','impact_level_id')
    def _compute_inherent_risk(self):
        self.sudo().write({
            'inherent_risk': self.env['inherent.risk.level'].search([('probability_level_id','=',self.probability_level_id.id), ('impact_level_id','=',self.impact_level_id.id)]).risk_level_name,
            'residual_risk': self.set_residual_risk(),
        })

    def set_residual_risk(self):
        for risk in self:
            if risk.ids:
                design = self.env['control.design'].search([('risk_factor_id','in',risk.ids[0])],limit=1)
                risk_level_id = self.env['risk.level'].search([('name','=', risk.inherent_risk)])
                residual_level = self.env['residual.risk.level'].search([
                    ('control_evaluation_criteria_id','=', design.control_evaluation_criteria_id.id),
                    ('inherent_risk_level_id','=',risk_level_id.id)
                ])
                if residual_level:
                    return residual_level[0].residual_risk_level_name
                else:
                    return ''
            else:
                return ''

    @api.model
    def web_read_group(self, domain, fields, groupby, limit=None, offset=0, orderby=False,lazy=True, expand=False, expand_limit=None, expand_orderby=False):
        res = super().web_read_group(domain, fields, groupby, limit, offset, orderby, lazy, expand, expand_limit, expand_orderby)
        
        low_inh = 0
        medium_inh = 0
        high_inh = 0
        valdos = []
        user_lang = self.env.user.lang
        if user_lang == 'en_US':
            txt_l = 'Low'
            txt_m = 'Medium'
            txt_h = 'High'
        else:
            txt_l = 'Bajo'
            txt_m = 'Medio'
            txt_h = 'Alto'
        for i in self.env['risk.factor'].search([]):
            if i.inherent_risk:
                if i.inherent_risk == txt_l:
                    low_inh += 1
                if i.inherent_risk == txt_m:
                    medium_inh += 1
                if i.inherent_risk == txt_h:
                    high_inh += 1

                # val.append(i.inherent_risk)
            if i.residual_risk:
                valdos.append(i.residual_risk)
            # data_assets = self.env['inherent.risk.level'].search([('risk_level_name', '=', i.inherent_risk)])
            _logger.info('grcbitdebug222:' + str(medium_inh))

            self.env['risk.factor'].sudo().search([('id','=',i.id)]).sudo().write({
                'inherent_factor_low': low_inh,
                'inherent_factor_medium': medium_inh,
                'inherent_factor_high': high_inh,
                # 'inherent_factor_count':(len(dict_c)),
                'residual_risk_count':(len(valdos))
            })
        return res

class RiskFactorCompanyRisk(models.Model):
    _name = 'risk.factor.company.risk'
    _rec_name = 'risk_factor_id'
    risk_factor_id = fields.Many2one('risk.factor', string='Risk Factor')
    company_risk_id= fields.Many2one('company.risk', string='Company Risk')
    description = fields.Text(string='Description')

class ResidualRiskLevel(models.Model):
    _name = 'residual.risk.level'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Residual Risk Level'

    inherent_risk_level_id = fields.Many2one('risk.level', string=_('Inherent Risk'), required=True, help="Level of risk an entity faces before taking actions to change its likelihood or impact.")
    control_evaluation_criteria_id = fields.Many2one('control.evaluation.criteria', string=_('Control Implementation Criteria'), required=True)
    residual_risk_level_id = fields.Many2one('risk.level', string=_('Residual Risk'), required=True, help="Amount of risk that remains after actions have been taken to reduce or eliminate it.")
    residual_risk_level_name = fields.Char(related='residual_risk_level_id.name', string=_('Residual Risk'), required=True)
    active = fields.Boolean(default=True)

class CompanyObjective(models.Model):
    _name = 'company.objective'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name ='objective_name'

    objective_name = fields.Char(string="Name")
    objective_description = fields.Text(string="Description")
    active = fields.Boolean(default=True)

class CompanyRisk(models.Model):
    _name = 'company.risk'
    _description = 'Strategic Risk'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name ='risk_name'

    risk_name = fields.Char(string="Name")
    risk_description = fields.Html(string="Description")
    company_objective_id = fields.Many2many('company.objective', string="Company Objective")
    risk_classification = fields.Many2many('risk.classification', string="Risk Category")
    active = fields.Boolean(default=True)

class OrganizationalProfile(models.Model):
    _name = 'organizational.profile'
    _description = 'Organizational Profile'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = 'description'

    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    active = fields.Boolean(default=True)
