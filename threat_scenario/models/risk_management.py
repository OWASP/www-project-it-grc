# -*- coding: utf-8 -*-

from odoo import fields, models

class RiskFactorThreats(models.Model):
    _inherit = 'risk.factor'

    taxonomy_threat_ids = fields.Many2one('taxonomy.threat.resource', string="Taxonomy Threat Sources", help="Threat sources that can be considered by organizations in identifying assumptions for risk assessments")
    adversary_cap_ids = fields.Many2one('characteristics.adversary.capability', string="Characteristics Adversary Capability")
    adversary_intent_ids = fields.Many2one('characteristics.adversary.intent', string="Characteristics Adversary Intent")
    adversary_target_ids = fields.Many2one('characteristics.adversary.targeting', string="Characteristics Adversary Targeting")
    range_effect_ids = fields.Many2one('range.effect.non.adversarial', string="Range Effect non Adversarial")
    adversial_theat_ids = fields.Many2one('adversarial.threat.events', string="Adversarial Threat Events")
    non_adversarial_ids = fields.Many2one('non.adversarial.threat.events', string="Non Adversarial Threat Events")
    relevenace_event_ids = fields.Many2one('relevance.threat.events', string="Relevance Threat Events")
    threat_source_type = fields.Selection([('adversarial','Adversarial'),('non_adversarial','Non-Adversarial')])
