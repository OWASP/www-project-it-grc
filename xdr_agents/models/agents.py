# -*- coding: utf-8 -*-
import os
import json
import logging
import requests
from requests.auth import HTTPBasicAuth
from odoo import api, fields, models, _, exceptions
from datetime import date

_logger = logging.getLogger(__name__)
    
# try:
#     host_ip = os.environ.get('XDR_API_HOST')
#     port = os.environ.get('XDR_API_PORT')
#     password = os.environ.get('XDR_API_PASS')
# except exceptions.ValidationError:
#     host_ip = '54.205.168.151'
#     port = ':55000'
#     password = 'T3sTW@zu$'

class ConnectionSettings(models.Model):
    _name = 'xdr.connection_settings'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    xdr_api_host_ip = fields.Char(string="XDR API HOST")
    xdr_api_port = fields.Char(string="XDR API PORT")
    xdr_api_password = fields.Char(string="XDR API PASSWORD")

class ListAgents(models.Model):
    _name = 'xdr.list_agents'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Date")
    description = fields.Text(string="Response")

    def _get_connection_settings(self):
        conn = self.env['xdr.connection_settings'].search([], order="create_date DESC", limit=1)
        return conn

    def get_jwt(self):
        conn = self._get_connection_settings()
        host_ip = conn.xdr_api_host_ip
        password = conn.xdr_api_password
        port = conn.xdr_api_port
        user = 'wazuh-wui'
        http_protocol = 'https://'
        end_point = '/security/user/authenticate'
        basic = HTTPBasicAuth(user, password)
        return requests.post(http_protocol + host_ip + port + end_point, auth=basic, verify=False)

    def list_agents(self):
        conn = self._get_connection_settings()
        host_ip = conn.xdr_api_host_ip
        port = conn.xdr_api_port
        http_protocol = 'https://'
        end_point = '/overview/agents'
        auth_token = self.get_jwt()
        auth_token = auth_token.json()['data']['token']
        data = {}
        headers = {'Authorization': 'Bearer ' + str(auth_token)}

        response = requests.get(http_protocol + host_ip + port + end_point, headers=headers, verify=False)
        return json.dumps(response.json(), indent=1)

    def list_agents_action_server(self):
        self.write({
            'name': date.today(),
            'description': str(self.list_agents())
        })

class ActiveConfiguration(models.Model):
    _name = 'xdr.active_configuration'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Date")
    description = fields.Text(string="Response")

    def _get_connection_settings(self):
        conn = self.env['xdr.connection_settings'].search([], order="create_date DESC", limit=1)
        return conn

    def get_jwt(self):
        conn = self._get_connection_settings()
        host_ip = conn.xdr_api_host_ip
        password = conn.xdr_api_password
        port = conn.xdr_api_port
        user = 'wazuh-wui'
        http_protocol = 'https://'
        end_point = '/security/user/authenticate'
        basic = HTTPBasicAuth(user, password)
        return requests.post(http_protocol + host_ip + port + end_point, auth=basic, verify=False)

    def get_active_configuration(self):
        conn = self._get_connection_settings()
        host_ip = conn.xdr_api_host_ip
        port = conn.xdr_api_port
        http_protocol = 'https://'
        agent_id = '001' #Este dato se obtiene del registro seleccionado en Odoo
        end_point = '/agents/'+agent_id+'/config/agent/client'
        auth_token = self.get_jwt()
        auth_token = auth_token.json()['data']['token']
        data = {}
        headers = {'Authorization': 'Bearer ' + str(auth_token)}

        response = requests.get(http_protocol + host_ip + port + end_point, headers=headers, verify=False)
        return json.dumps(response.json(), indent=1)

    def get_active_configuration_action_server(self):
        self.write({
            'name': date.today(),
            'description': str(self.get_active_configuration())
        })

class Stats(models.Model):
    _name = 'xdr.stats'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Date")
    description = fields.Text(string="Response")

    def _get_connection_settings(self):
        conn = self.env['xdr.connection_settings'].search([], order="create_date DESC", limit=1)
        return conn

    def get_jwt(self):
        conn = self._get_connection_settings()
        host_ip = conn.xdr_api_host_ip
        password = conn.xdr_api_password
        port = conn.xdr_api_port
        user = 'wazuh-wui'
        http_protocol = 'https://'
        end_point = '/security/user/authenticate'
        basic = HTTPBasicAuth(user, password)
        return requests.post(http_protocol + host_ip + port + end_point, auth=basic, verify=False)

    def get_stats(self):
        conn = self._get_connection_settings()
        host_ip = conn.xdr_api_host_ip
        port = conn.xdr_api_port
        http_protocol = 'https://'
        agent_id = '001' #Este dato se obtiene del registro seleccionado en Odoo
        end_point = '/agents/'+agent_id+'/stats/agent'
        auth_token = self.get_jwt()
        auth_token = auth_token.json()['data']['token']
        data = {}
        headers = {'Authorization': 'Bearer ' + str(auth_token)}

        response = requests.get(http_protocol + host_ip + port + end_point, headers=headers, verify=False)
        return json.dumps(response.json(), indent=1)

    def get_stats_action_server(self):
        self.write({
            'name': date.today(),
            'description': str(self.get_stats())
        })

class Ciscat(models.Model):
    _name = 'xdr.ciscat'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Date")
    description = fields.Text(string="Response")

    def _get_connection_settings(self):
        conn = self.env['xdr.connection_settings'].search([], order="create_date DESC", limit=1)
        return conn

    def get_jwt(self):
        conn = self._get_connection_settings()
        host_ip = conn.xdr_api_host_ip
        password = conn.xdr_api_password
        port = conn.xdr_api_port
        user = 'wazuh-wui'
        http_protocol = 'https://'
        end_point = '/security/user/authenticate'
        basic = HTTPBasicAuth(user, password)
        return requests.post(http_protocol + host_ip + port + end_point, auth=basic, verify=False)

    def ciscat_results(self):
        conn = self._get_connection_settings()
        host_ip = conn.xdr_api_host_ip
        port = conn.xdr_api_port
        http_protocol = 'https://'
        agent_id = '001' #Este dato se obtiene del registro seleccionado en Odoo
        end_point = '/ciscat/'+agent_id+'/results'
        auth_token = self.get_jwt()
        auth_token = auth_token.json()['data']['token']
        data = {}
        headers = {'Authorization': 'Bearer ' + str(auth_token)}

        response = requests.get(http_protocol + host_ip + port + end_point, headers=headers, verify=False)
        return json.dumps(response.json(), indent=1)

    def ciscat_results_action_server(self):
        self.write({
            'name': date.today(),
            'description': str(self.ciscat_results())
        })