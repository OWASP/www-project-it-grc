# -*- coding: utf-8 -*-

from odoo import fields, models


class ChatGPTModel(models.Model):
    _name = 'chatgpt.model'
    _description = "ChatGPT Model"

    name = fields.Char(string='ChatGPT Model', required=True)
