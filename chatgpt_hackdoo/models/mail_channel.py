# -*- coding: utf-8 -*-

from openai import OpenAI
import openai
import time
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


#====================================
#grcbit
#openai_api_key = ''
# assistant_id   = 'asst_VVFoMjDkTFbXY20HQyhm8QOO'
#openai.api_key = open_ai_key
#====================================



class Channel(models.Model):
    _inherit = 'mail.channel'

    def _notify_thread(self, message, msg_vals=False, **kwargs):
        rdata = super(Channel, self)._notify_thread(message, msg_vals=msg_vals, **kwargs)
        chatgpt_channel_id = self.env.ref('chatgpt_hackdoo.channel_chatgpt')
        user_chatgpt = self.env.ref("chatgpt_hackdoo.user_chatgpt")
        partner_chatgpt = self.env.ref("chatgpt_hackdoo.partner_chatgpt")
        author_id = msg_vals.get('author_id')
        chatgpt_name = str(partner_chatgpt.name or '') + ', '
        prompt = msg_vals.get('body')
        temp = ''
        #_logger.info(prompt)
        #============================================================
        #grcbit
        prompt = str(prompt) + '. Answer based on the information and files you have loaded and your instructions.'
        #_logger.info(prompt)
        #message = client.beta.threads.messages.create(
        #        thread_id = thread.id
        #        )
        #============================================================

        if not prompt:
            return rdata
        Partner = self.env['res.partner']
        partner_name = ''
        if author_id:
            partner_id = Partner.browse(author_id)
            if partner_id:
                partner_name = partner_id.name

        if self.channel_type == 'chat':
            if (author_id != partner_chatgpt.id and
                    (chatgpt_name in msg_vals.get('record_name', '') or 'ChatGPT,' in msg_vals.get('record_name', ''))):
                try:
                    res = self._get_chatgpt_response(prompt=prompt)
                    self.with_user(user_chatgpt).message_post(body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
                except Exception as e:
                    raise UserError(_(e))

        elif msg_vals.get('model', '') == 'mail.channel' and msg_vals.get('res_id', 0) == chatgpt_channel_id.id:
            if author_id != partner_chatgpt.id:
                try:
                    res = self._get_chatgpt_response(prompt=prompt)
                    chatgpt_channel_id.with_user(user_chatgpt).message_post(body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
                except Exception as e:
                    raise UserError(_(e))

        return rdata

    def _get_chatgpt_response(self, prompt):
        ICP = self.env['ir.config_parameter'].sudo()
        api_key = ICP.get_param('chatgpt_hackdoo.openapi_api_key')
        client = OpenAI(api_key=api_key)
        assistant_id = ICP.get_param('chatgpt_hackdoo.assistant_id')

        #=================================================
        #grcbit
        thread = client.beta.threads.create()
        #message = client.beta.threads.messages.create(
        #        thread_id = thread.id,
        #        role = 'user',
        #        content = prompt
        #        )
        #run = client.beta.threads.runs.create(
        #        thread_id=thread.id,
        #        assistant_id=assintant_id
        #        )
        #=================================================


        gpt_model_id = ICP.get_param('chatgpt_hackdoo.chatgp_model')
        gpt_model = 'gpt-3.5-turbo'
        try:
            if gpt_model_id:
                gpt_model = self.env['chatgpt.model'].browse(int(gpt_model_id)).name
        except Exception as ex:
            # gpt_model = 'text-davinci-003'
            gpt_model = 'gpt-3.5-turbo'
            pass
        try:
            #===============================================
            #grcbit
            message = client.beta.threads.messages.create(
                thread_id = thread.id,
                role = 'user',
                content = prompt
                )
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant_id
                )
            #run = client.beta.threads.runs.retrieve(
            #    thread_id=thread.id,
            #    run_id=run.id,
            #    )
            #run = wait_on_run(run, thread, client)
            while True:
                try:
                    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
                    #_logger.info(run.status)
                    #_logger.info(run)
                    if run.status == 'completed':
                        break
                    elif run.status == 'queued' or run.status=='in_progress':
                        #break
                        # Wait for some time before checking again
                        time.sleep(5)
                    elif run.status == 'failed':
                        break
                    #else:
                    #    break
                except:
                    pass

            #response = client.chat.completions.create(
            #    messages=[{"role": "system", "content": prompt}],
            #    model=gpt_model,
            #    temperature=0.6,
            #    max_tokens=3000,
            #    top_p=1,
            #    frequency_penalty=0,
            #    presence_penalty=0,
            #    user=self.env.user.name
            #)
            #===================================
            #res = response.choices[0].message.content
            response = client.beta.threads.messages.list(thread_id=thread.id)
            #_logger.info(response.data[0].content[0].text.value)
            #try:
            #    _logger.info(run.data)
            #except:
            #    pass
            #_logger.info(len(response.data))
            #_logger.info(response.data[0].content[0].text.value)
            return response.data[0].content[0].text.value
        except Exception as e:
            raise UserError(_(e))

def wait_on_run(run, thread, client):
    _logger.info(run)
    _logger.info(thread)
    _logger.info(client)
    while run.status == 'queued' or run.status =='in_progress':
        run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
                )
        time.sleep(0.5)
    return run
