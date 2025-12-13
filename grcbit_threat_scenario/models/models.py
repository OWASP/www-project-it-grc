# -*- coding: utf-8 -*-

from odoo import fields, models

class TaxonomyThreatResource(models.Model):
    _name = 'taxonomy.threat.resource'
    _description = 'NIST Taxonomy Threat Source'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = 'type_threat_source'

    type_threat_source = fields.Char(string="Type")
    description = fields.Html(string="Description")
    characteristics = fields.Char(string="Characteristics")
    active = fields.Boolean(default=True)

class CharacteristicsAdversaryCapability(models.Model):
    _name = 'characteristics.adversary.capability'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = 'qualitative_value'

    qualitative_value = fields.Char(string="Qualitative Value")
    semiquantitative_values = fields.Float(string="Semi-Quantitative Values")    
    description = fields.Text(string="Description")
    active = fields.Boolean(default=True)

class CharacteristicsAdversaryIntent(models.Model):
    _name = 'characteristics.adversary.intent'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = 'qualitative_value'

    qualitative_value = fields.Char(string="Qualitative Value")
    semiquantitative_values = fields.Float(string="Semi-Quantitative Values")
    description = fields.Text(string="Description")
    active = fields.Boolean(default=True)

class CharacteristicsAdversaryTargeting(models.Model):
    _name = 'characteristics.adversary.targeting'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = 'qualitative_value'

    qualitative_value = fields.Char(string="Qualitative Value")
    semiquantitative_values = fields.Float(string="Semi-Quantitative Values")
    description = fields.Text(string="Description")
    active = fields.Boolean(default=True)

class RangeEffectsNonAdversarial(models.Model):
    _name = 'range.effect.non.adversarial'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = 'qualitative_value'

    qualitative_value = fields.Char(string="Qualitative Value")
    semiquantitative_values = fields.Float(string="Semi-Quantitative Values")
    description = fields.Text(string="Description")
    active = fields.Boolean(default=True)

class AdversarialThreatEvents(models.Model):
    _name = 'adversarial.threat.events'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = 'threat_event'

    threat_event = fields.Char(string="Thread Event")
    description = fields.Text(string="Description")
    active = fields.Boolean(default=True)

class NonAdversarialThreatEvents(models.Model):
    _name = 'non.adversarial.threat.events'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = 'threat_event'

    threat_event = fields.Char(string="Thread Event")
    description = fields.Text(string="Description")
    #threat_source = fields.Text(string="Threat Source")
    active = fields.Boolean(default=True)

class RelevanceThreatEvents(models.Model):
    _name = 'relevance.threat.events'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = 'value'

    value = fields.Text(string="Value")
    description = fields.Text(string="Description")
    active = fields.Boolean(default=True)
