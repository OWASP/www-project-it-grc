# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
from datetime import date
from statistics import mode

_logger = logging.getLogger(__name__)

class ItInventoryInh(models.Model):
    _inherit = 'it.inventory'

    responsible = fields.Many2one('isms.people', string="IT Admin")

class DataInventoryInh(models.Model):
    _inherit = 'data.inventory'

    owner = fields.Many2one('isms.people', string="Asset Owner")