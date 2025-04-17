# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class ResPartnerInh(models.Model):
    _inherit = 'res.partner'

    signup_expiration = fields.Datetime(groups="base.group_erp_manager,grcbit_base.group_grc_admin")
    signup_token = fields.Char(groups="base.group_erp_manager,grcbit_base.group_grc_admin")
    signup_type = fields.Char(groups="base.group_erp_manager,grcbit_base.group_grc_admin")