# -*- coding: utf-8 -*-

from odoo import fields, models

class TaxonomyThreatResource(models.Model):
    _name = 'taxonomy.threat.resource'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    type_threat_source = fields.Char(string="Type")
    description = fields.Html(string="Description")
    characteristics = fields.Char(string="Characteristics")

class CharacteristicsAdversaryCapability(models.Model):
    _name = 'characteristics.adversary.capability'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    qualitative_value = fields.Char(string="Qualitative Value")
    semiquantitative_values = fields.Float(string="Semi-Quantitative Values")
    
    description = fields.Text(string="Description")

class CharacteristicsAdversaryIntent(models.Model):
    _name = 'characteristics.adversary.intent'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    qualitative_value = fields.Char(string="Qualitative Value")
    semiquantitative_values = fields.Float(string="Semi-Quantitative Values")
    description = fields.Text(string="Description")

class CharacteristicsAdversaryTargeting(models.Model):
    _name = 'characteristics.adversary.targeting'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    qualitative_value = fields.Char(string="Qualitative Value")
    semiquantitative_values = fields.Float(string="Semi-Quantitative Values")
    description = fields.Text(string="Description")

class RangeEffectsNonAdversarial(models.Model):
    _name = 'range.effect.non.adversarial'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    qualitative_value = fields.Char(string="Qualitative Value")
    semiquantitative_values = fields.Float(string="Semi-Quantitative Values")
    description = fields.Text(string="Description")

class AdversarialThreatEvents(models.Model):
    _name = 'adversarial.threat.events'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    threat_event = fields.Char(string="Thread Event")
    description = fields.Text(string="Description")

class NonAdversarialThreatEvents(models.Model):
    _name = 'non.adversarial.threat.events'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    threat_event = fields.Char(string="Thread Event")
    description = fields.Text(string="Description")

class RelevanceThreatEvents(models.Model):
    _name = 'relevance.threat.events'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    value = fields.Text(string="Value")
    description = fields.Text(string="Description")