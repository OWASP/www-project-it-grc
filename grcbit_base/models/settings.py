# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
from datetime import date
from statistics import mode

_logger = logging.getLogger(__name__)

class ItComponents(models.Model):
    _name ='it.components'

    name = fields.Char(string="Name")
    description = fields.Html(string="Description")
    color = fields.Integer(string="Color")