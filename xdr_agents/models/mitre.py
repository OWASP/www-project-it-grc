# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class MitreGroups(models.Model):
    _name = 'mitre.groups'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char()
    description = fields.Text()

class MitreMetadata(models.Model):
    _name = 'mitre.metadata'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char()
    description = fields.Text()

class MitreMitigations(models.Model):
    _name = 'mitre.mitigations'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char()
    description = fields.Text()

class MitreReferences(models.Model):
    _name = 'mitre.references'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char()
    description = fields.Text()

class MitreSoftware(models.Model):
    _name = 'mitre.software'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char()
    description = fields.Text()

class MitreTactic(models.Model):
    _name = 'mitre.tactic'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char()
    description = fields.Text()

class MitreTechniques(models.Model):
    _name = 'mitre.techniques'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char()
    description = fields.Text()