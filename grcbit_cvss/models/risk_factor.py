# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class RiskFactorInh(models.Model):
    _inherit = 'risk.factor'

    risk_assessment_type = fields.Selection(
        [
            ('it', 'IT'),
            ('process', 'Process'),
            ('vendor', 'Vendor'),
        ],
        string="Risk Assessment Type",
    )
    business_process_id = fields.Many2one('business.process', string='Business Process')
    third_party_id = fields.Many2one('third.party', string='Third Party')
    score = fields.Float(string="Score", digits=(1,1))
    vector = fields.Char(string="Vector")