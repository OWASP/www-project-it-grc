# -*- coding: utf-8 -*-

from odoo import fields, models

class TaxonomyThreadresource(models.Model):
    _name = 'taxonomy.thread.resource'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    type_threat_source = fields.Char(string="Type")
    description = fields.Html(string="Description")
    characteristics = fields.Char(string="Characteristics")

class CharacteristicsAdversaryCapability(models.Model):
    _name = 'characteristics.adversary.capability'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    semiquantitative_values = fields.Float(string="Semi-Quantitative Values 1")
    semiquantitative_values2 = fields.Float(string="Semi-Quantitative Values 2")
    description = fields.Text(string="Description")

class CharacteristicsAdversaryIntent(models.Model):
    _name = 'characteristics.adversary.intent'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    semiquantitative_values = fields.Float(string="Semi-Quantitative Values 1")
    semiquantitative_values2 = fields.Float(string="Semi-Quantitative Values 2")
    description = fields.Text(string="Description")

class CharacteristicsAdversaryTargeting(models.Model):
    _name = 'characteristics.adversary.targeting'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    semiquantitative_values = fields.Float(string="Semi-Quantitative Values 1")
    semiquantitative_values2 = fields.Float(string="Semi-Quantitative Values 2")
    description = fields.Text(string="Description")

class RangeEffectsNonAdversarial(models.Model):
    _name = 'range.effect.non.adversarial'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    semiquantitative_values = fields.Float(string="Semi-Quantitative Values 1")
    semiquantitative_values2 = fields.Float(string="Semi-Quantitative Values 2")
    description = fields.Text(string="Description")

class AdversarialthreatEvents(models.Model):
    _name = 'adversarial.thread.events'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    thread_event = fields.Char(string="Thread Event")
    description = fields.Text(string="Description")

class NonAdversarialthreatEvents(models.Model):
    _name = 'non.adversarial.thread.events'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    thread_event = fields.Char(string="Thread Event")
    description = fields.Text(string="Description")

class RelevancethreatEvents(models.Model):
    _name = 'relevance.thread.events'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    value = fields.Text(string="Value")
    description = fields.Text(string="Description")