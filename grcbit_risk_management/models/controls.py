# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging
from datetime import date
from statistics import mode

_logger = logging.getLogger(__name__)

class ControlType(models.Model):
    _name = 'control.type'
    _description = 'Data Inventory'
    name = fields.Char(string='Control Type', required=True)
    description = fields.Html(string='Description', required=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The control type name already exists.")]

class SecurityProperty(models.Model):
    _name = 'security.property'
    _description = 'Data Inventory'
    name = fields.Char(string='Security Property', required=True)
    description = fields.Html(string='Description', required=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The security property name already exists.")]

class CybersecurityConcept(models.Model):
    _name = 'cybersecurity.concept'
    _description = 'Data Inventory'

    name = fields.Char(string='Cybersecurity Concept', required=True)
    description = fields.Html(string='Description', required=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The cybersecurty concept name already exists.")]

class ControlDesignCriteria(models.Model):
    _name = 'control.design.criteria'
    _description = 'Design Criteria'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description', required=True)
    active = fields.Boolean(default=True)

class ControlEvaluationCriteria(models.Model):
    _name = 'control.evaluation.criteria'
    _description = 'Implementation Criteria'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description', required=True)
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
    
class ControlEvidence(models.Model):
    _name = 'control.evidence'
    _description = 'Control Evidence'
    
    name = fields.Char(string='Name', required=True)
    attachment = fields.Many2many('ir.attachment', string="Attachment")
    comment = fields.Html(string='Comment/Description')
    control_design_id = fields.Many2one('control.design')
    active = fields.Boolean(default=True)

class SecurityDomain(models.Model):
    _name = 'security.domain'
    _description = 'Data Inventory'
    name = fields.Char(string='Security Domain', required=True)
    description = fields.Html(string='Description', required=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', "The security domain name already exists.")]

class OperationalCapability(models.Model):
    _name = 'operational.capability'
    _description = 'Data Inventory'

    name = fields.Char(string=_('Operational Capability'), required=True)
    description = fields.Html(string=_('Description'), required=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('name_uniq', 'unique(name)', _("The operational capability name already exists."))]

class ControlDesing(models.Model):
    _name = 'control.design'
    _inherit = 'mail.thread'

    _description = 'Control Design'
    _order = 'control_id'
    _rec_name = 'display_name'

    state = fields.Selection([
        ('draft','Draft'),                             #25 %
        ('designed','Designed'),                       #50 %
        ('implemented','Implemented'),                 #75 %
        ('approved','Approved')],                      #100%
        string='Status', 
        default='draft', 
        readonly=True, 
        copy=False, 
        tracking=True, 
        track_visibility='always'
    )
    control_id = fields.Char(
        string='Control ID', 
        required=True, 
        index=True, 
        copy=False, 
        default='New'
    )
    risk_factor_id = fields.Many2many('risk.factor', string='Risk Factor', track_visibility='always')
    display_name = fields.Char(string='Control', compute='_compute_display_name')
    name = fields.Char(string='Control Title', required=True, help="Short name of the control")
    control_line_ids = fields.One2many('control.line', 'control_design_id', string='Control Guide')
    estimated_date = fields.Date(string='Estimated Implementation Date')
    description = fields.Html(string='Purpose', required=True, help="Why the control should be implemented")
    control = fields.Char(string="Control", help="What the control is")
    evidence_guide = fields.Text(string='Evidence Guide')
    responsible = fields.Many2one('res.users', string='Responsible', required=True, track_visibility='always')
    responsible_id = fields.Many2one('hr.employee', string='Responsible', required=True, track_visibility='always')
    is_key_control = fields.Boolean(string='Key Control', track_visibility='always')
    control_type_id = fields.Many2many('control.type', string='Control Type', required=True)
    security_property_id = fields.Many2many('security.property', string='Security Property', required=True)
    cybersecurity_concept_id = fields.Many2many('cybersecurity.concept', string='Cybersecurity Concept', required=True)
    operational_capability_id = fields.Many2many('operational.capability', string='Operational Capability', required=True)
    security_domain_id = fields.Many2many('security.domain', string='Security Domain', required=True)
    comment = fields.Text(string='Comment')
    evidence_pending = fields.Text(string='Evidence Pending')
    active = fields.Boolean(default=True)
    control_evidence_ids = fields.One2many('control.evidence', 'control_design_id')
    control_evaluation_criteria_id = fields.Many2one('control.evaluation.criteria', string='Effectiveness Evaluation')
    control_design_criteria_id = fields.Many2one('control.design.criteria', string='Design Evaluation')
    design_date = fields.Date(string='Design Date', readonly=True)
    implementation_date = fields.Date(string='Implementation Date', readonly=True)
    approve_date  = fields.Date(string='Approve Date', readonly=True)
    rejected_date = fields.Date(string='Rejected Date', readonly=True)

    draft_comment = fields.Html(string="Draft Comment")
    design_comment = fields.Html(string="Design Comment")
    implemented_comment = fields.Html(string="Implemented Comment")
    approved_comment = fields.Html(string="Approved Comment")

    @api.model
    def create(self, vals):
        vals['control_id'] = self.env['ir.sequence'].next_by_code('control.id.sequence')
        return super(ControlDesing, self).create(vals)

    @api.depends('control_id','name')
    def _compute_display_name(self):
        for i in self:
            i.display_name = i.control_id 

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

    def action_implemented(self):
        if not self.control_design_criteria_id:
            raise ValidationError("You should evaluate Design Criteria")
        else:
            self.sudo().state = 'implemented'
            self.sudo().implementation_date = date.today()
            self.sudo()._status_control(self.id)

    def action_approved(self):
        if not self.control_evaluation_criteria_id:
            raise ValidationError("You should evaluate Implementation Criteria")
        else:
            self.state = 'approved'
            self.approve_date = date.today()
            self._status_control(self.id)
            # self.sudo()._residual_risk(self.id, self.control_evaluation_criteria_id)
            self.sudo().set_residual_risk()

    def action_rejected(self):
        self.state = 'implemented'
        self.rejected_date = date.today()

    def set_residual_risk(self):
        for rec in self:
            for risk in rec.risk_factor_id:
                risk_level_id = self.env['risk.level'].search([('name','=', risk.inherent_risk)])
                residual_level = self.env['residual.risk.level'].search([
                    ('control_evaluation_criteria_id','=', rec.control_evaluation_criteria_id.id),
                    ('inherent_risk_level_id','=',risk_level_id.id)
                ])
                if residual_level:
                    risk.residual_risk = residual_level[0].residual_risk_level_name



    def _residual_risk(self, control_id, control_eval):
        risk_factor_ids    = self.env['control.design'].search([('id','=',control_id)]).risk_factor_id
        num_criteria = len( self.env['control.evaluation.criteria'].search([])  )

        for i in risk_factor_ids:
            control_eval_ids = self.env['control.design'].search([('risk_factor_id','in',i.id), '|', ('state','=','implemented'), ('state','=','approved') ]).control_evaluation_criteria_id
            if control_eval_ids:
                m=[]
                for c in control_eval_ids:
                    m.append(c.id)

                if int(len(m)) > int(num_criteria):
                    control_eval_mode = mode(m)
                    _logger.info('grcbit_160423_ctrl: ' + str(control_eval_mode) )
                else:
                    control_eval_mode = control_eval.id
                    _logger.info('grcbit_160423_mode: ' + str(control_eval_mode) )

                for r in self.env['risk.factor'].search([('id','=',i.id)]):
                    ir = self.env['risk.level'].search([('name','=',r.inherent_risk)]).id
                    residual_risk = self.env['residual.risk.level'].search([('control_evaluation_criteria_id','=',control_eval_mode), ('inherent_risk_level_id','=',ir)]).residual_risk_level_name
                    r.write({'residual_risk':residual_risk})
            else:
                self.env['risk.factor'].search([('id','=',i.id)]).write({'residual_risk':''})

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
                if state == 'implemented':
                    status += 75
                if state == 'approved':
                    status += 100
            s.sudo().write({'control_status':status / len(s.control_design_id)})