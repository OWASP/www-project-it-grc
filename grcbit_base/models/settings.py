# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
import random as r
from datetime import date
from statistics import mode

_logger = logging.getLogger(__name__)

class ItComponents(models.Model):
    _name ='it.components'

    name = fields.Char(string="Name")
    description = fields.Html(string="Description")
    color = fields.Integer(string="Color", default=lambda x: x.default_color())

    def default_color(self):
        x = r.randrange(11)
        if x <= 11 or x > 0:
            return x