# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    def _get_default_chatgpt_model(self):
        return self.env.ref('chatgpt_hackdoo.chatgpt_model_gpt_3_5_turbo').id

    openapi_api_key = fields.Char(string="API Key", help="Provide the API key here", config_parameter="chatgpt_hackdoo.openapi_api_key")
    chatgpt_model_id = fields.Many2one('chatgpt.model', 'ChatGPT Model', ondelete='cascade', default=_get_default_chatgpt_model,  config_parameter="chatgpt_hackdoo.chatgp_model")
    assistant_id = fields.Char(string="Assistant ID", config_parameter="chatgpt_hackdoo.assistant_id")
