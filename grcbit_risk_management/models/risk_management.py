# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
from datetime import date
from statistics import mode

_logger = logging.getLogger(__name__)

class ImpactLevel(models.Model):
    _name = 'impact.level'
    _description = 'Impact Level'

    name = fields.Char(string=_('Impact Level'), required=True)
    description = fields.Text(string=_('Description'), required=True)
    value = fields.Integer(string=_('Value'), required=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', _("The impact level name already exists.")),('level_uniq', 'unique(value)', _("The impact level value already exists."))]

class ProbabilityLevel(models.Model):
    _name = 'probability.level'
    _description = 'Probability Level'

    name = fields.Char(string=_('Probability Level'), required=True)
    description = fields.Text(string=_('Description'), required=True)
    value = fields.Integer(string=_('Value'), required=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', _("The probability level name already exists.")),('level_uniq', 'unique(value)', _("The probability level value already exists."))]

class RiskLevel(models.Model):
    _name = 'risk.level'
    _description = 'Risk Level'

    name = fields.Char(string=_('Risk Level'), required=True)
    description = fields.Text(string=_('Description'))
    value = fields.Integer(string=_('Value'), required=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', _("The risk level name already exists.")),('level_uniq', 'unique(value)', _("The risk level value already exists."))]

class InherentRiskLevel(models.Model):
    _name = 'inherent.risk.level'
    _description = 'Inherent Risk Level'
    _rec_name = 'risk_level_name'

    impact_level_id      = fields.Many2one('impact.level', string=_('Impact Level'))
    probability_level_id = fields.Many2one('probability.level', string=_('Probability Level'))
    risk_level_id        = fields.Many2one('risk.level', string=_('Risk Level'))
    risk_level_name      = fields.Char(related='risk_level_id.name', string=_('Risk Level'))
    description = fields.Text(string=_('Description'), required=True)
    color = fields.Integer(string=_('Color'))
    active = fields.Boolean(default=True)

class RiskClassification(models.Model):
    _name = 'risk.classification'
    _description = 'Risk Classification'

    name = fields.Char(string=_('Risk Classification'), required=True)
    description = fields.Text(string=_('Description'), required=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', _("The risk classification name already exists."))]

class RiskFactor(models.Model):
    _name = 'risk.factor'
    _inherit = 'mail.thread'
    _description = 'Risk Factor'
    _order = 'risk_id'
    _rec_name = 'display_name'

    display_name = fields.Char(string=_('Control Category'), compute='_compute_display_name')
    name = fields.Text(string=_('Risk Factor'), required=True)
    risk_id = fields.Char(string=_('Risk ID'), required=True, index=True, copy=False, default='New')
    risk_classification_id = fields.Many2many('risk.classification',string=_('Risk Classification'), required=True)
    data_inventory_id = fields.Many2many('data.inventory',string=_('Data Asset'), track_visibility='always')
    cause = fields.Text(string=_('Cause'), required=True)
    consequence = fields.Text(string=_('Consequence'), required=True)
    impact_level_id = fields.Many2one('impact.level', string=_('Impact Level'), required=True, track_visibility='always')
    probability_level_id = fields.Many2one('probability.level', string=_('Probability Level'), required=True, track_visibility='always')
    responsible = fields.Many2one('res.users', string=_('Risk Owner'), required=True, track_visibility='always')
    quantification = fields.Float(string=_('Quantification'), track_visibility='always')
    inherent_risk  = fields.Char(string=_('Inherent Risk'), track_visibility='always')
    residual_risk  = fields.Char(string=_('Residual Risk'), track_visibility='always')
    attachment = fields.Many2many('ir.attachment', string=_("Attachment"))
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

class ResidualRiskLevel(models.Model):
    _name = 'residual.risk.level'
    _description = 'Residual Risk Level'

    inherent_risk_level_id = fields.Many2one('inherent.risk.level', string=_('Inherent Risk'), required=True)
    control_evaluation_criteria_id = fields.Many2one('control.evaluation.criteria', string=_('Implementation Criteria'), required=True)
    residual_risk_level_id = fields.Many2one('risk.level', string=_('Residual Risk'), required=True)
    residual_risk_level_name = fields.Char(related='residual_risk_level_id.name', string=_('Residual Risk'), required=True)
    active = fields.Boolean(default=True)
