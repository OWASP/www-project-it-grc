# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class MitreGroups(models.Model):
    _name = 'mitre.groups'

    name = fields.Char()
    description = fields.Text()

class MitreMetadata(models.Model):
    _name = 'mitre.metadata'

    name = fields.Char()
    description = fields.Text()

class MitreMitigations(models.Model):
    _name = 'mitre.mitigations'

    name = fields.Char()
    description = fields.Text()

class MitreReferences(models.Model):
    _name = 'mitre.references'

    name = fields.Char()
    description = fields.Text()

class MitreSoftware(models.Model):
    _name = 'mitre.software'

    name = fields.Char()
    description = fields.Text()

class MitreTactic(models.Model):
    _name = 'mitre.tactic'

    name = fields.Char()
    description = fields.Text()

class MitreTechniques(models.Model):
    _name = 'mitre.techniques'

    name = fields.Char()
    description = fields.Text()