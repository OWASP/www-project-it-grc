# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

from openai import OpenAI
import time
import re
import json
import markdown2

import logging


_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    enable_chatgpt_assistant_response = fields.Boolean(
        string="Enable ChatGPT Assistant Response",
        help="Check this box to enable ChatGPT Assistant to respond to messages on Discuss app and website livechat",
        config_parameter="grcbit_gpt.enable_chatgpt_assistant_response",
        default=False
    )
    chatgpt_api_key = fields.Char(
        string="API Key",
        help="Provide ChatGPT API key here",
        config_parameter="grcbit_gpt.chatgpt_api_key"
    )
    assistant_id = fields.Char(
        string="Assistant ID",
        help="Provide Assistant ID here",
        config_parameter="grcbit_gpt.assistant_id"
    )

    xdr_api_host = fields.Char(
        string="XDR API Host",
        config_parameter="grcbit_gpt.xdr_api_host"
    )
    xdr_api_port = fields.Char(
        string="XDR API Port",
        config_parameter="grcbit_gpt.xdr_api_port"
    )
    xdr_api_pass = fields.Char(
        string="XDR API Pass",
        config_parameter="grcbit_gpt.xdr_api_pass"
    )


class Channel(models.Model):
    _inherit = 'mail.channel'

    chatgpt_message_text = fields.Char(default=None, store=False)
    should_generate_chatgpt_response = fields.Boolean(default=False, store=False)

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
            'grcbit_gpt.enable_chatgpt_assistant_response'
        )
        if not enable_chatgpt_assistant_response or not self.enable_chatgpt_assistant_response:
            self.should_generate_chatgpt_response = False
            return result

        prompt = msg_vals.get('body')
        if not prompt:
            self.should_generate_chatgpt_response = False
            return result

        chatgpt_channel_id = self.env.ref('grcbit_gpt.channel_chatgpt')
        partner_chatgpt = self.env.ref("grcbit_gpt.partner_chatgpt")
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
        partner_chatgpt = self.env.ref("grcbit_gpt.partner_chatgpt")
        chatgpt_name = str(partner_chatgpt.name or '') + ', '
        chatgpt_channel_id = self.env.ref('grcbit_gpt.channel_chatgpt')

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

        user_chatgpt = self.env.ref("grcbit_gpt.user_chatgpt")

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
        chatgpt_api_key = config_parameter.get_param('grcbit_gpt.chatgpt_api_key')
        assistant_id = config_parameter.get_param('grcbit_gpt.assistant_id')
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
           
            if run.required_action and run.required_action.submit_tool_outputs and run.required_action.submit_tool_outputs.tool_calls:
                tool_calls = run.required_action.submit_tool_outputs.tool_calls
                for tool in tool_calls:
                    func_args = json.loads(tool.function.arguments)
                    #--------------------------------------------------------------
                    # This functions are only available for the enterprise version
                    #--------------------------------------------------------------

                    # XDR
                    if tool.function.name == 'xdr_list_agents':
                        result = self.env['gpt.function'].xdr_list_agents()
                    elif tool.function.name == 'xdr_get_active_configuration_agent_client':
                        result = self.env['gpt.function'].xdr_get_active_configuration_agent_client(func_args['agent_id'])
                    #elif tool.function.name == 'xdr_get_agent_key':
                    #    result = self.env['gpt.function'].xdr_get_agent_key(func_args['agent_id'])
                    #elif tool.function.name == 'xdr_restart_agent':
                    #    result = self.env['gpt.function'].xdr_restart_agent(func_args['agent_id'])
                    #elif tool.function.name == 'xdr_summarize_agents_os':
                    #    result = self.env['gpt.function'].xdr_summarize_agents_os()
                    #elif tool.function.name == 'xdr_summarize_agents_status':
                    #    result = self.env['gpt.function'].xdr_summarize_agents_status()
                    #elif tool.function.name == 'xdr_get_ciscat_scan_results':
                    #    result = self.env['gpt.function'].xdr_get_ciscat_scan_results(func_args['agent_id'])
                    elif tool.function.name == 'xdr_get_agent_ports':
                        result = self.env['gpt.function'].xdr_get_agent_ports(func_args['agent_id'])
                    #elif tool.function.name == 'xdr_get_agent_vulnerabilities':
                    #    result = self.env['gpt.function'].xdr_get_agent_vulnerabilities(func_args['agent_id'])
                    elif tool.function.name == 'xdr_get_agent_processes':
                        result = self.env['gpt.function'].xdr_get_agent_processes(func_args['agent_id'])
                    elif tool.function.name == 'xdr_get_agent_packages':
                        result = self.env['gpt.function'].xdr_get_agent_packages(func_args['agent_id'])
                    elif tool.function.name == 'xdr_get_agent_os':
                        result = self.env['gpt.function'].xdr_get_agent_os(func_args['agent_id'])
                    elif tool.function.name == 'xdr_get_agent_network_routing':
                        result = self.env['gpt.function'].xdr_get_agent_network_routing(func_args['agent_id'])
                    elif tool.function.name == 'xdr_get_agent_network_address':
                        result = self.env['gpt.function'].xdr_get_agent_network_address(func_args['agent_id'])
                    elif tool.function.name == 'xdr_get_agent_hotfixes':
                        result = self.env['gpt.function'].xdr_get_agent_hotfixes(func_args['agent_id'])
                    elif tool.function.name == 'xdr_get_agent_hardware':
                        result = self.env['gpt.function'].xdr_get_agent_hardware(func_args['agent_id'])
                    elif tool.function.name == 'xdr_get_security_configuration_assessment':
                        result = self.env['gpt.function'].xdr_get_security_configuration_assessment(func_args['agent_id'])
                    # Rootcheck
                    elif tool.function.name == 'xdr_rootcheck_run_scan':
                        result = self.env['gpt.function'].xdr_rootcheck_run_scan()
                    elif tool.function.name == 'xdr_rootcheck_get_results':
                        result = self.env['gpt.function'].xdr_rootcheck_get_results(func_args['agent_id'])
                    elif tool.function.name == 'xdr_rootcheck_clear_results':
                        result = self.env['gpt.function'].xdr_rootcheck_clear_results(func_args['agent_id'])
                    elif tool.function.name == 'xdr_rootcheck_get_last_scan_datetime':
                        result = self.env['gpt.function'].xdr_rootcheck_get_last_scan_datetime(func_args['agent_id'])
                    # Syscheck FIM
                    elif tool.function.name == 'xdr_syscheck_run_scan':
                        result = self.env['gpt.function'].xdr_syscheck_run_scan()
                    elif tool.function.name == 'xdr_syscheck_get_results':
                        result = self.env['gpt.function'].xdr_syscheck_get_results(func_args['agent_id'])
                    #elif tool.function.name == 'xdr_syscheck_clear_results':
                    #    result = self.env['gpt.function'].xdr_syscheck_clear_results(func_args['agent_id'])
                    elif tool.function.name == 'xdr_syscheck_get_last_scan_datetime':
                        result = self.env['gpt.function'].xdr_syscheck_get_last_scan_datetime(func_args['agent_id'])
                    #elif tool.function.name == 'xdr_alerts_summary_1':
                    #    result = self.env['gpt.function'].xdr_alerts_summary_1()
                    # MANAGER
                    elif tool.function.name == 'xdr_manager_get_stats':
                        result = self.env['gpt.function'].xdr_manager_get_stats()
                    elif tool.function.name == 'xdr_manager_get_logs_summary':
                        result = self.env['gpt.function'].xdr_manager_get_logs_summary()
                    # MITRE
                    #elif tool.function.name == 'xdr_mitre_groups':
                    #    result = self.env['gpt.function'].xdr_mitre_groups()
                    # GRC
                    # Asset Management
                    elif tool.function.name == 'grc_get_data_asset':
                        result = self.env['gpt.function'].grc_get_data_asset()
                    elif tool.function.name == 'grc_get_it_inventory':
                        result = self.env['gpt.function'].grc_get_it_inventory()
                    elif tool.function.name == 'grc_get_data_classification':
                        result = self.env['gpt.function'].grc_get_data_classification()
                    elif tool.function.name == 'grc_get_supplier':
                        result = self.env['gpt.function'].grc_get_supplier()
                    elif tool.function.name == 'grc_get_business_process':
                        result = self.env['gpt.function'].grc_get_business_process()
                    # ISMS
                    elif tool.function.name == 'grc_get_iso27001_statement_applicabilty':
                        result = self.env['gpt.function'].grc_get_iso27001_statement_applicabilty()
                    elif tool.function.name == 'grc_get_isms_role':
                        result = self.env['gpt.function'].grc_get_isms_role()
                    #elif tool.function.name == 'grc_it_inventory_summary':
                    #    result = self.env['gpt.function'].grc_it_inventory_summary()
                    # PCI
                    # Risk Management
                    #elif tool.function.name == 'grc_company_risk':
                    #    result = self.env['gpt.function'].grc_company_risk()
                    #elif tool.function.name == 'grc_risk_factor':
                    #    result = self.env['gpt.function'].grc_risk_factor()
                    #elif tool.function.name == 'grc_control_design':
                    #    result = self.env['gpt.function'].grc_control_design()
                    #elif tool.function.name == 'grc_compliance':
                    #    result = self.env['gpt.function'].grc_compliance()
                    #elif tool.function.name == 'grc_tcp_ports':
                    #    result = self.env['gpt.function'].grc_tcp_ports()
                    #elif tool.function.name == 'grc_company_profile_risk':
                    #   result = self.env['grc_company_profile_risk'].grc_risk_profile()
                    else:
                        result = {}
                
                    _logger.info("Funcion ejecutada: " + str(tool.function.name))

                    run = client.beta.threads.runs.submit_tool_outputs(
                            thread_id=thread.id,
                            run_id=run.id,
                            tool_outputs=[
                                {
                                    "tool_call_id": tool.id,
                                    "output": result,
                                },
                            ]
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
                pattern = r'(?<=【)(.*?)(?=】)'
                cleaned_text = re.sub(pattern, '', messages.data[0].content[0].text.value)
                cleaned_text = cleaned_text.replace('【】','')
                #cleaned_text = cleaned_text.replace('-','*')
                #_logger.info('Texto markdown: ' + str(cleaned_text))
                return markdown2.markdown(cleaned_text)
            else:
                _logger.error(run.status)
                raise RuntimeError(run.status)
        except Exception as e:
            _logger.error(e)
            raise RuntimeError(_(e))
