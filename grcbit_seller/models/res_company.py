# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, AccessError

_logger = logging.getLogger(__name__)

class ResPartnerGRC(models.Model):
    _inherit = 'res.company'

    dns_domain = fields.Char(string="DNS Domain")