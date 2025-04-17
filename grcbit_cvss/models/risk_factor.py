# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class RiskFactorInh(models.Model):
    _inherit = 'risk.factor'

    score = fields.Float(string="Score", digits=(1,1))
    vector = fields.Char(string="Vector")