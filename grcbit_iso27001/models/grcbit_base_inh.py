# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
from datetime import date
from statistics import mode

_logger = logging.getLogger(__name__)

class ResPartnerIsoInh(models.Model):
    _inherit = 'hr.employee'

    isms_roles_ids = fields.Many2many('isms.role', string=_("ISMS Role"))

class ItInventoryInh(models.Model):
    _inherit = 'it.inventory'

    responsible = fields.Many2one('hr.employee', string="IT Admin")

class DataInventoryInh(models.Model):
    _inherit = 'data.inventory'

    owner = fields.Many2one('hr.employee', string="Asset Owner")
