# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _
from cvss import CVSS2, CVSS3

_logger = logging.getLogger(__name__)

class CVSSCalculator(models.TransientModel):
    _name = 'cvss.calculator'

    attack_vector = fields.Selection([
        ('network','Network (N)'),
        ('adjacent','Adjacent (A)'),
        ('local','Local (L)'),
        ('physical','Physical (P)'),
    ], string="Attack Vector (AV)", default="network")
    attack_complexity = fields.Selection([
        ('low','Low (L)'),
        ('high','High (H)'),
    ], string="Attack Complexity (AC)", default="low")
    privileges_required = fields.Selection([
        ('none','None (N)'),
        ('low','Low (L)'),
        ('high','High (H)'),
    ], string="Privileges Required (PR)", default="none")
    user_interaction = fields.Selection([
        ('none','None (N)'),
        ('required','Required (R)'),
    ], string="User Interaction (UI)", default="none")
    scope = fields.Selection([
        ('unchanged','Unchanged (U)'),
        ('changed','Changed (C)'),
    ], string="Scope (S)", default="unchanged")
    confidentiality = fields.Selection([
        ('none','None (N)'),
        ('low','Low (L)'),
        ('high','High (H)'),
    ], string="Confidentiality (C)", default="none")
    integrity = fields.Selection([
        ('none','None (N)'),
        ('low','Low (L)'),
        ('high','High (H)'),
    ], string="Integrity (I)", default="none")
    availability = fields.Selection([
        ('none','None (N)'),
        ('low','Low (L)'),
        ('high','High (H)'),
    ], string="Availability (A)", default="none")

    score = fields.Float(string="Score", digits=(1,1), compute="get_vector", store=True)
    vector = fields.Char(string="Vector", compute="get_vector", store=True)

    risk_factor_id = fields.Many2one('risk.factor', string="Risk Factor", default=lambda x: x.env.context.get('active_id'))
    #cve_id = fields.Many2one('risk.factor.vulnerability.management', string="Vulnerability", default=lambda x: x.env.context.get('active_id'))
    cve_id = fields.Many2one(
        'risk.factor.vulnerability.management',
        string="Vulnerability",
        default=lambda self: self.env.context.get('active_id')
        if self.env.context.get('active_model') == 'risk.factor.vulnerability.management'
        else False
    )

    @api.depends('attack_vector','attack_complexity','privileges_required','user_interaction','scope','confidentiality','integrity','availability')
    def get_vector(self):
        for rec in self:
            base = 'CVSS:3.1'
            av = ''
            ac = ''
            pr = ''
            ui = ''
            s = ''
            c = ''
            i = ''
            a = ''
            if rec.attack_vector:
                if rec.attack_vector == 'network':
                    av = '/AV:N'
                elif rec.attack_vector == 'adjacent':
                    av = '/AV:A'
                elif rec.attack_vector == 'local':
                    av = '/AV:L'
                elif rec.attack_vector == 'physical':
                    av = '/AV:P'
            if rec.attack_complexity:
                if rec.attack_complexity == 'low':
                    ac = '/AC:L'
                elif rec.attack_complexity == 'high':
                    ac = '/AC:H'
            if rec.privileges_required:
                if rec.privileges_required == 'none':
                    pr = '/PR:N'
                elif rec.privileges_required == 'low':
                    pr = '/PR:L'
                elif rec.privileges_required == 'high':
                    pr = '/PR:H'
            if rec.user_interaction:
                if rec.user_interaction == 'none':
                    ui = '/UI:N'
                elif rec.user_interaction == 'required':
                    ui = '/UI:R'
            if rec.scope:
                if rec.scope == 'unchanged':
                    s = '/S:U'
                elif rec.scope == 'changed':
                    s = '/S:C'
            if rec.confidentiality:
                if rec.confidentiality == 'none':
                    c = '/C:N'
                elif rec.confidentiality == 'low':
                    c = '/C:L'
                elif rec.confidentiality == 'high':
                    c = '/C:H'
            if rec.integrity:
                if rec.integrity == 'none':
                    i = '/I:N'
                elif rec.integrity == 'low':
                    i = '/I:L'
                elif rec.integrity == 'high':
                    i = '/I:H'
            if rec.availability:
                if rec.availability == 'none':
                    a = '/A:N'
                elif rec.availability == 'low':
                    a = '/A:L'
                elif rec.availability == 'high':
                    a = '/A:H'
            final = '/MAV:A'
            rec.vector = base + av + ac + pr + ui + s + c + i + a + final
            vector = rec.vector
            val = CVSS3(vector)
            rec.score = float(val.scores()[0])

    def accept_done(self):
        for rec in self:
            is_risk_factor = rec.env.context.get('active_model')
            _logger.info('is_risk_factor: '+ str(is_risk_factor))
            if is_risk_factor == 'risk.factor':
                rec.risk_factor_id.vector = rec.vector
                rec.risk_factor_id.score = rec.score
            else:
                rec.cve_id.cvss_score_3 = rec.score
                rec.cve_id.cvss_string_3 = rec.vector
