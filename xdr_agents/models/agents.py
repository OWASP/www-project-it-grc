# -*- coding: utf-8 -*-
import os
import logging
import requests
from requests.auth import HTTPBasicAuth
from odoo import api, fields, models, _, exceptions

_logger = logging.getLogger(__name__)
    
try:
    host_ip = os.environ.get('XDR_API_HOST')
    port = os.environ.get('XDR_API_PORT')
    password = os.environ.get('XDR_API_PASS')
except exceptions.ValidationError:
    host_ip = '192.168.112.3' #
    port = ':55000' #
    password = 'T3sTW@zu$'

user = 'wazuh-wui'
http_protocol = 'https://'

class ListAgents(models.Model):
    _name = 'xdr.list_agents'

    name = fields.Char()
    description = fields.Text()

    def get_jwt(self, host_ip, user, password):
        #curl -u <USER>:<PASSWORD> -k -X POST "https://<HOST_IP>:55000/security/user/authenticate
        end_point = '/security/user/authenticate'
        basic = HTTPBasicAuth(user, password)
        return requests.post(http_protocol + host_ip + port + end_point, auth=basic, verify=False)

    def list_agents(self):
        end_point = '/overview/agents'
        auth_token = self.get_jwt(host_ip, user, password)
        auth_token = auth_token.json()['data']['token']
        #_logger.info(auth_token)
        data = {}
        headers = {'Authorization': 'Bearer ' + str(auth_token)}

        response = requests.get(http_protocol + host_ip + port + end_point, headers=headers, verify=False)
        _logger.info(response.json())

class ActiveConfiguration(models.Model):
    _name = 'xdr.active_configuration'

    name = fields.Char()
    description = fields.Text()

    def get_jwt(self, host_ip, user, password):
        #curl -u <USER>:<PASSWORD> -k -X POST "https://<HOST_IP>:55000/security/user/authenticate
        end_point = '/security/user/authenticate'
        basic = HTTPBasicAuth(user, password)
        return requests.post(http_protocol + host_ip + port + end_point, auth=basic, verify=False)

    def get_active_configuration(self):
        # {protocol}://{host}:{port}/agents/{agent_id}/config/{component}/{configuration}
        # end_point = '/agents/{agent_id}/config/{component}/{configuration}'
        agent_id = '001' #Este dato se obtiene del registro seleccionado en Odoo
        end_point = '/agents/'+agent_id+'/config/agent/client'
        auth_token = self.get_jwt(host_ip, user, password)
        auth_token = auth_token.json()['data']['token']
        data = {}
        headers = {'Authorization': 'Bearer ' + str(auth_token)}

        response = requests.get(http_protocol + host_ip + port + end_point, headers=headers, verify=False)
        _logger.info(response.json())

class Stats(models.Model):
    _name = 'xdr.stats'

    name = fields.Char()
    description = fields.Text()

    def get_jwt(self, host_ip, user, password):
        #curl -u <USER>:<PASSWORD> -k -X POST "https://<HOST_IP>:55000/security/user/authenticate
        end_point = '/security/user/authenticate'
        basic = HTTPBasicAuth(user, password)
        return requests.post(http_protocol + host_ip + port + end_point, auth=basic, verify=False)

    def get_stats(self):
        # {protocol}://{host}:{port}/agents/{agent_id}/stats/{component}
        agent_id = '001' #Este dato se obtiene del registro seleccionado en Odoo
        end_point = '/agents/'+agent_id+'/stats/agent'
        auth_token = self.get_jwt(host_ip, user, password)
        auth_token = auth_token.json()['data']['token']
        data = {}
        headers = {'Authorization': 'Bearer ' + str(auth_token)}

        response = requests.get(http_protocol + host_ip + port + end_point, headers=headers, verify=False)
        _logger.info(response.json())

class Ciscat(models.Model):
    _name = 'xdr.ciscat'

    name = fields.Char()
    description = fields.Text()

    def get_jwt(self, host_ip, user, password):
        #curl -u <USER>:<PASSWORD> -k -X POST "https://<HOST_IP>:55000/security/user/authenticate
        end_point = '/security/user/authenticate'
        basic = HTTPBasicAuth(user, password)
        return requests.post(http_protocol + host_ip + port + end_point, auth=basic, verify=False)

    def ciscat_results(self):
        # {protocol}://{host}:{port}/ciscat/{agent_id}/results
        agent_id = '001' #Este dato se obtiene del registro seleccionado en Odoo
        end_point = '/ciscat/'+agent_id+'/results'
        auth_token = self.get_jwt(host_ip, user, password)
        auth_token = auth_token.json()['data']['token']
        data = {}
        headers = {'Authorization': 'Bearer ' + str(auth_token)}

        response = requests.get(http_protocol + host_ip + port + end_point, headers=headers, verify=False)
        _logger.info(response.json())