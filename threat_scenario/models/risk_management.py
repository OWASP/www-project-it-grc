# -*- coding: utf-8 -*-

from odoo import fields, models

class RiskFactorThreats(models.Model):
    _inherit = 'risk.factor'

    taxonomy_threat_ids = fields.Many2many('taxonomy.threat.resource', string="Taxonomy Threat Sources")
    adversary_cap_ids = fields.Many2many('characteristics.adversary.capability', string="Characteristics Adversary Capability")
    adversary_intent_ids = fields.Many2many('characteristics.adversary.intent', string="Characteristics Adversary Intent")
    adversary_target_ids = fields.Many2many('characteristics.adversary.targeting', string="Characteristics Adversary Targeting")
    range_effect_ids = fields.Many2many('range.effect.non.adversarial', string="Range Effect non Adversarial")
    adversial_theat_ids = fields.Many2many('adversarial.threat.events', string="Adversarial Threat Events")
    non_adversarial_ids = fields.Many2many('non.adversarial.threat.events', string="Non Adversarial Threat Events")
    relevenace_event_ids = fields.Many2many('relevance.threat.events', string="Relevance Threat Events")