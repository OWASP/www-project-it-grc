# -*- coding: utf-8 -*-
import os
import json
import logging
import requests
from requests.auth import HTTPBasicAuth
from odoo import api, fields, models, _, exceptions
from datetime import date

_logger = logging.getLogger(__name__)
    
class GptFunction(models.Model):
    _name = 'gpt.function'

    def get_xdr_config(self, param_id):
        config_parameter = self.env['ir.config_parameter'].sudo()
        xdr_value = config_parameter.get_param(param_id)
        return xdr_value

    def get_jwt(self):
        host_ip  = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_host') 
        password = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_port')
        port     = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_pass')
        user = 'wazuh-wui'
        http_protocol = 'https://'
        end_point = '/security/user/authenticate'
        basic = HTTPBasicAuth(user, password)
        return requests.post(http_protocol + host_ip + ':' + port + end_point, auth=basic, verify=False)

    def list_agents(self):
        # Return information about all available agents or a list of them
        host_ip  = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_host')
        port     = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_pass')
        http_protocol = 'https://'
        end_point = '/agents'
        auth_token = self.get_jwt().json()['data']['token']
        headers = {'Authorization': 'Bearer ' + str(auth_token)}
        response = requests.get(http_protocol + host_ip + ':' + port + end_point, headers=headers, verify=False)
        return json.dumps(response.json(), indent=1)

    def get_active_configuration_agent_client(self, agent_id):
        # Return the active configuration the agent is currently using. This can be different from the configuration
        # present in the configuration file if it has been modified  and the agent has not been restarted yet
        host_ip  = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_host')
        port     = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_pass')
        http_protocol = 'https://'
        #agent_id = agent_id
        end_point = '/agents/'+agent_id+'/config/agent/client'
        auth_token = self.get_jwt().json()['data']['token']
        #data = {}
        headers = {'Authorization': 'Bearer ' + str(auth_token)}
        response = requests.get(http_protocol + host_ip + ':' + port + end_point, headers=headers, verify=False)
        return json.dumps(response.json(), indent=1)

    def get_agent_key(self, agent_id):
        # Return the key of an agent
        host_ip  = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_host')
        port     = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_pass')
        http_protocol = 'https://'
        end_point = '/agents/'+agent_id+'/key'
        auth_token = self.get_jwt().json()['data']['token']
        headers = {'Authorization': 'Bearer ' + str(auth_token)}
        response = requests.get(http_protocol + host_ip + ':' + port + end_point, headers=headers, verify=False)
        return json.dumps(response.json(), indent=1)

    def summarize_agents_os(self):
        # Return a summary of the OS of available agents
        host_ip  = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_host')
        port     = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_pass')
        http_protocol = 'https://'
        end_point = '/agents/summary/os'
        auth_token = self.get_jwt().json()['data']['token']
        headers = {'Authorization': 'Bearer ' + str(auth_token)}
        response = requests.get(http_protocol + host_ip + ':' + port + end_point, headers=headers, verify=False)
        return json.dumps(response.json(), indent=1)

    def summarize_agents_status(self):
        # Return a summary of the connection and groups configuration
        # synchronization statuses of available agents
        host_ip  = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_host')
        port     = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_pass')
        http_protocol = 'https://'
        end_point = '/agents/summary/status'
        auth_token = self.get_jwt().json()['data']['token']
        headers = {'Authorization': 'Bearer ' + str(auth_token)}
        response = requests.get(http_protocol + host_ip + ':' + port + end_point, headers=headers, verify=False)
        return json.dumps(response.json(), indent=1)

    def get_agent_key(self, agent_id):
        # Return the key of an agent
        host_ip  = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_host')
        port     = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_pass')
        http_protocol = 'https://'
        end_point = '/agents/'+agent_id+'/key'
        auth_token = self.get_jwt().json()['data']['token']
        headers = {'Authorization': 'Bearer ' + str(auth_token)}
        response = requests.get(http_protocol + host_ip + ':' + port + end_point, headers=headers, verify=False)
        return json.dumps(response.json(), indent=1)

    def get_ciscat_scan_results(self, agent_id):
        # Return the agents ciscat result info
        host_ip  = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_host')
        port     = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_pass')
        http_protocol = 'https://'
        end_point = '/ciscat/'+agent_id+'/results'
        auth_token = self.get_jwt().json()['data']['token']
        headers = {'Authorization': 'Bearer ' + str(auth_token)}
        response = requests.get(http_protocol + host_ip + ':' + port + end_point, headers=headers, verify=False)
        return json.dumps(response.json(), indent=1)

    def get_agents_ports(self, agent_id):
        # Return the agents ports info.
        # This information includes local IP, Remote IP, protocol information among other
        host_ip  = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_host')
        port     = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_pass')
        http_protocol = 'https://'
        end_point = '/syscollector/'+agent_id+'/ports'
        auth_token = self.get_jwt().json()['data']['token']
        headers = {'Authorization': 'Bearer ' + str(auth_token)}
        response = requests.get(http_protocol + host_ip + ':' + port + end_point, headers=headers, verify=False)
        return json.dumps(response.json(), indent=1)

    def get_agent_vulnerabilities(self, agent_id):
        # Return the agents ciscat result info
        host_ip  = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_host')
        port     = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_pass')
        http_protocol = 'https://'
        end_point = '/vulnerability/'+agent_id
        auth_token = self.get_jwt().json()['data']['token']
        headers = {'Authorization': 'Bearer ' + str(auth_token)}
        response = requests.get(http_protocol + host_ip + ':' + port + end_point, headers=headers, verify=False)
        return json.dumps(response.json(), indent=1)

    def get_agent_processes(self, agent_id):
        # Return the agents processes info
        host_ip  = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_host')
        port     = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_pass')
        http_protocol = 'https://'
        end_point = '/syscollector/'+agent_id+'/processes'
        auth_token = self.get_jwt().json()['data']['token']
        headers = {'Authorization': 'Bearer ' + str(auth_token)}
        response = requests.get(http_protocol + host_ip + ':' + port + end_point, headers=headers, verify=False)
        return json.dumps(response.json(), indent=1)

    def get_agent_packages(self, agent_id):
        # Return the agents packages info.
        # This information include name, section, size, priority information of all packages among others
        host_ip  = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_host')
        port     = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_pass')
        http_protocol = 'https://'
        end_point = '/syscollector/'+agent_id+'/packages'
        auth_token = self.get_jwt().json()['data']['token']
        headers = {'Authorization': 'Bearer ' + str(auth_token)}
        response = requests.get(http_protocol + host_ip + ':' + port + end_point, headers=headers, verify=False)
        return json.dumps(response.json(), indent=1)

    def get_agent_os(self, agent_id):
        # Return the agents OS info.
        # This information include OS information, architecture
        host_ip  = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_host')
        port     = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_pass')
        http_protocol = 'https://'
        end_point = '/syscollector/'+agent_id+'/os'
        auth_token = self.get_jwt().json()['data']['token']
        headers = {'Authorization': 'Bearer ' + str(auth_token)}
        response = requests.get(http_protocol + host_ip + ':' + port + end_point, headers=headers, verify=False)
        return json.dumps(response.json(), indent=1)

    def get_agent_network_routing(self, agent_id):
        # Return de agents routing configuration for each network interface
        host_ip  = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_host')
        port     = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_pass')
        http_protocol = 'https://'
        end_point = '/syscollector/'+agent_id+'/netproto'
        auth_token = self.get_jwt().json()['data']['token']
        headers = {'Authorization': 'Bearer ' + str(auth_token)}
        response = requests.get(http_protocol + host_ip + ':' + port + end_point, headers=headers, verify=False)
        return json.dumps(response.json(), indent=1)

    def get_agent_network_address(self, agent_id):
        # Return the agents network address info.
        # This information include used IP protocol, interface, IP address 
        host_ip  = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_host')
        port     = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_pass')
        http_protocol = 'https://'
        end_point = '/syscollector/'+agent_id+'/netaddr'
        auth_token = self.get_jwt().json()['data']['token']
        headers = {'Authorization': 'Bearer ' + str(auth_token)}
        response = requests.get(http_protocol + host_ip + ':' + port + end_point, headers=headers, verify=False)
        return json.dumps(response.json(), indent=1)

    def get_agent_hotfixes(self, agent_id):
        # Return all hotfixies intalled by Microsoft in Windows Systems
        host_ip  = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_host')
        port     = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_pass')
        http_protocol = 'https://'
        end_point = '/syscollector/'+agent_id+'/hotfixes'
        auth_token = self.get_jwt().json()['data']['token']
        headers = {'Authorization': 'Bearer ' + str(auth_token)}
        response = requests.get(http_protocol + host_ip + ':' + port + end_point, headers=headers, verify=False)
        return json.dumps(response.json(), indent=1)

    def get_agent_hardware(self, agent_id):
        # Return the agents hardware info. This informatoion include cpu, ram, scan info amon others
        host_ip  = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_host')
        port     = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_pass')
        http_protocol = 'https://'
        end_point = '/syscollector/'+agent_id+'/hardware'
        auth_token = self.get_jwt().json()['data']['token']
        headers = {'Authorization': 'Bearer ' + str(auth_token)}
        response = requests.get(http_protocol + host_ip + ':' + port + end_point, headers=headers, verify=False)
        return json.dumps(response.json(), indent=1)

    def get_security_configuration_assessment(self, agent_id):
        # Return the security configuration assessment database of an agent
        host_ip  = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_host')
        port     = self.get_xdr_config('chatgpt_assistant_discuss_integration.xdr_api_pass')
        http_protocol = 'https://'
        end_point = '/sca/'+agent_id
        auth_token = self.get_jwt().json()['data']['token']
        headers = {'Authorization': 'Bearer ' + str(auth_token)}
        response = requests.get(http_protocol + host_ip + ':' + port + end_point, headers=headers, verify=False)
        return json.dumps(response.json(), indent=1)


