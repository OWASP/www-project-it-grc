# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

from openai import OpenAI
import time

import logging


_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    enable_chatgpt_assistant_response = fields.Boolean(
        string="Enable ChatGPT Assistant Response",
        help="Check this box to enable ChatGPT Assistant to respond to messages on Discuss app and website livechat",
        config_parameter="chatgpt_assistant_discuss_integration.enable_chatgpt_assistant_response",
        default=False
    )
    chatgpt_api_key = fields.Char(
        string="API Key",
        help="Provide ChatGPT API key here",
        config_parameter="chatgpt_assistant_discuss_integration.chatgpt_api_key"
    )
    assistant_id = fields.Char(
        string="Assistant ID",
        help="Provide Assistant ID here",
        config_parameter="chatgpt_assistant_discuss_integration.assistant_id"
    )


class Channel(models.Model):
    _inherit = 'mail.channel'

    # These field will not store in the database, it is only used to store some temporary value
    # to send notification correctly to the livechat and admin panel
    chatgpt_message_text = fields.Char(default=None, store=False)
    should_generate_chatgpt_response = fields.Boolean(default=False, store=False)

    # enable/disable ChatGPT assistant response in specific channel
    enable_chatgpt_assistant_response = fields.Boolean(
        string="Enable ChatGPT assistant response in this channel",
        help="Check this box to enable ChatGPT assistant to respond to messages this channel",
        default=True,
    )

    def _message_post_after_hook(self, message, msg_vals):
        result = super(Channel, self)._message_post_after_hook(message, msg_vals=msg_vals)

        self.chatgpt_message_text = None
        self.should_generate_chatgpt_response = False

        config_parameter = self.env['ir.config_parameter'].sudo()
        enable_chatgpt_assistant_response = config_parameter.get_param(
            'chatgpt_assistant_discuss_integration.enable_chatgpt_assistant_response'
        )
        if not enable_chatgpt_assistant_response or not self.enable_chatgpt_assistant_response:
            self.should_generate_chatgpt_response = False
            return result

        prompt = msg_vals.get('body')
        if not prompt:
            self.should_generate_chatgpt_response = False
            return result

        chatgpt_channel_id = self.env.ref('chatgpt_assistant_discuss_integration.channel_chatgpt')
        partner_chatgpt = self.env.ref("chatgpt_assistant_discuss_integration.partner_chatgpt")
        author_id = msg_vals.get('author_id')
        chatgpt_name = str(partner_chatgpt.name or '') + ', '

        is_chatgpt_private_channel = (
            author_id != partner_chatgpt.id
            and (chatgpt_name in msg_vals.get('record_name', '') or 'ChatGPT,' in msg_vals.get('record_name', ''))
            and self.channel_type == 'chat'
        )

        is_chatgpt_public_channel = (
            author_id != partner_chatgpt.id
            and msg_vals.get('model', '') == 'mail.channel'
            and msg_vals.get('res_id', 0) == chatgpt_channel_id.id
        )

        should_chatgpt_respond_livechat = (
            author_id != partner_chatgpt.id
            and (not self.env.user
                 or (
                     not self.env.user.has_group('im_livechat.im_livechat_group_user')
                     and not self.env.user.has_group('im_livechat.im_livechat_group_manager')
                 )
                 )
            and self.channel_type == 'livechat'
        )

        self.should_generate_chatgpt_response = (
            is_chatgpt_private_channel
            or is_chatgpt_public_channel
            or should_chatgpt_respond_livechat
        )

        try:
            if self.should_generate_chatgpt_response:
                self.chatgpt_message_text = self._get_chatgpt_response(prompt=prompt)
        except Exception as e:
            _logger.error(e)
            raise ValidationError(e)

        return result

    def _notify_thread(self, message, msg_vals, **kwargs):
        rdata = super(Channel, self)._notify_thread(message, msg_vals=msg_vals, **kwargs)

        if not self.should_generate_chatgpt_response or not self.chatgpt_message_text:
            return rdata

        author_id = msg_vals.get('author_id')
        partner_chatgpt = self.env.ref("chatgpt_assistant_discuss_integration.partner_chatgpt")
        chatgpt_name = str(partner_chatgpt.name or '') + ', '
        chatgpt_channel_id = self.env.ref('chatgpt_assistant_discuss_integration.channel_chatgpt')

        is_chatgpt_private_channel = (
            author_id != partner_chatgpt.id
            and (chatgpt_name in msg_vals.get('record_name', '') or 'ChatGPT,' in msg_vals.get('record_name', ''))
            and self.channel_type == 'chat'
        )

        is_chatgpt_public_channel = (
            author_id != partner_chatgpt.id
            and msg_vals.get('model', '') == 'mail.channel'
            and msg_vals.get('res_id', 0) == chatgpt_channel_id.id
        )

        should_chatgpt_respond_livechat = (
            author_id != partner_chatgpt.id
            and (not self.env.user
                 or (
                     not self.env.user.has_group('im_livechat.im_livechat_group_user')
                     and not self.env.user.has_group('im_livechat.im_livechat_group_manager')
                 )
                 )
            and self.channel_type == 'livechat'
        )

        user_chatgpt = self.env.ref("chatgpt_assistant_discuss_integration.user_chatgpt")

        if (
            is_chatgpt_private_channel
        ):
            self.with_user(user_chatgpt).message_post(
                body=self.chatgpt_message_text,
                message_type='comment',
                subtype_xmlid='mail.mt_comment'
            )
        elif (
            is_chatgpt_public_channel
        ):
            chatgpt_channel_id.with_user(user_chatgpt).message_post(
                body=self.chatgpt_message_text,
                message_type='comment',
                subtype_xmlid='mail.mt_comment'
            )
        elif (
            should_chatgpt_respond_livechat
        ):
            self.with_user(user_chatgpt).sudo().message_post(
                body=self.chatgpt_message_text,
                message_type='comment',
                subtype_xmlid='mail.mt_comment'
            )

        return rdata

    def _get_chatgpt_response(self, prompt):
        config_parameter = self.env['ir.config_parameter'].sudo()
        chatgpt_api_key = config_parameter.get_param('chatgpt_assistant_discuss_integration.chatgpt_api_key')
        assistant_id = config_parameter.get_param('chatgpt_assistant_discuss_integration.assistant_id')
        try:
            client = OpenAI(api_key=chatgpt_api_key)
            thread = client.beta.threads.create()
            message = client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=prompt,
            )
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant_id,
            )
            while run.status in ['queued', 'in_progress', 'cancelling']:
                time.sleep(1)  # Wait for 1 second
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )
            if run.status == 'completed':
                messages = client.beta.threads.messages.list(
                    thread_id=thread.id
                )
                return messages.data[0].content[0].text.value
            else:
                _logger.error(run.status)
                raise RuntimeError(run.status)
        except Exception as e:
            _logger.error(e)
            raise RuntimeError(_(e))
