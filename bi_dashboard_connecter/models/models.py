# -*- coding: utf-8 -*-
import logging

import requests
from requests.structures import CaseInsensitiveDict

from odoo import models, fields, api, http
from odoo.exceptions import ValidationError
from .. import common_url

_logger = logging.getLogger(__name__)


class bi_dashboard_cred(models.Model):
    _name = 'bi.cred'
    _description = 'bi.cred'
    _rec_name = 'name'

    name = fields.Char(string='Name')
    username = fields.Char(string='Username')
    password = fields.Char(string='Password')
    client_id = fields.Char(string='Client ID')
    server_message = fields.Char(string='Important Message')
    token = fields.Char(string='Token')
    po_number = fields.Char(string='Purchase order number (POXXXX)')
    personal_email = fields.Char(string='Personal email for verification message')
    activated = fields.Boolean(default=False)
    dashboard_line = fields.One2many(comodel_name="bi.dashboard", inverse_name='dashboard_line_id')
    created_flag = fields.Boolean(name="Hide password/Client_id from other admin", default=False)

    @api.model
    def create(self, vals):
        try:
            base_url = http.request.httprequest.url_root
            is_conf = self.env['bi.cred'].sudo().search([])
            if not is_conf:

                req = f"{base_url}power-bi/auth/?username={vals['username']}&password={vals['password']}&client_id={vals['client_id']}"
                headers = {"Content-Type": "multipart/form-data; boundary=<calculated when request is sent>"}
                print(req)
                response = requests.post(req, headers=headers)
                _logger.info(" ---------------33" + str(response.status_code))

                if response.status_code == 200:
                    token = response.json()
                    vals['token'] = token['access_token']
                    vals['created_flag'] = True
                    vals['activated'] = True
                    _logger.info(" ---------------4")

                    return super(models.Model, self).create(vals)
                else:
                    raise ValidationError("Check you credentials or check API's permissions")
            else:
                raise ValidationError("You already created a Configration object!!!!")


        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            raise ValidationError(e)

    # Refresh Token on every dashboard API
    def refresh_token(self):
        base_url = http.request.httprequest.url_root
        req = f"{base_url}power-bi/auth/?username={self.username}&password={self.password}&client_id={self.client_id}"
        print(req)
        headers = {"Content-Type": "multipart/form-data"}
        response = requests.post(req, headers=headers)
        print(response)
        if response.status_code == 200:
            token = response.json()
            self.token = token['access_token']
            return self.token
        else:
            print(response.status_code)
            raise ValidationError("Check you credentials or check API's permissions")

    def fetch_dashboard(self):  # function to fetch dashboard in setting section
        base_url = http.request.httprequest.url_root

        url = "https://api.powerbi.com/v1.0/myorg/reports"
        headers = CaseInsensitiveDict()
        token = self.refresh_token()
        headers["Accept"] = "application/json"
        headers["Authorization"] = f"Bearer {token}"
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            dashboards = res.json()
        base_url = http.request.httprequest.url_root

        if res.status_code == 200 and dashboards['value']:
            for dashboard in dashboards['value']:
                is_dashboard = self.env['bi.dashboard'].sudo().search([('dashboard_id', '=', dashboard['id'])])
                if not is_dashboard:
                    self.env['bi.dashboard'].create(
                        {'dashboard_name': dashboard['name'], 'dashboard_id': dashboard['id'],
                         'dashboard_line_id': self.id,
                         'dashboard_url': dashboard['embedUrl'],
                         'dashboard_iframe': f'''<div class="embed-responsive embed-responsive-16by9"><iframe class="embed-responsive-item" title="{dashboard['name']}" width="100%" height="100%" src="{base_url}report?id={dashboard['id']}" frameborder="0" allowFullScreen="true"/></div>'''})
        else:
            raise ValidationError("Check you credentials or check API's permissions/ or you have 0 Dashboards!!!!!")


class bi_dashboard_connecter(models.Model):
    _name = 'bi.dashboard'
    _description = 'bi dashboard'
    _rec_name = 'dashboard_name'

    dashboard_name = fields.Char(string='Dashboard name')
    dashboard_url = fields.Char(string='Dashboard Url')
    dashboard_id = fields.Char(string="Report Id")
    dashboard_iframe = fields.Html("Dashboard Preview", sanitize=False)
    dashboard_line_id = fields.Many2one(comodel_name='bi.cred', ondelete='cascade')
    allowed_users = fields.Many2many("res.users", string="Allowed Users")

    def open_url(self):  # action url to open dashboard in fullscreen
        if self.id:
            return {
                'type': 'ir.actions.act_url',
                'url': '/report?id=%s' % self.dashboard_id,
                'target': 'new',
            }

    def delete_dashboard(self):
        self.search([('id', '=', self.id)]).unlink()
        return {'view_mode': 'tree',
                'view_id': False,
                'tag': 'reload',
                'res_model': 'bi.dashboard',
                'type': 'ir.actions.act_window'
                }


class organization_dashboard(models.Model):
    _name = 'org.dashboard'
    _description = 'Organization dashboard'
    _rec_name = 'dashboard_name'

    dashboard_name = fields.Char(string='Dashboard name')
    dashboard_url = fields.Char(string='Dashboard Url')
    created_flag = fields.Boolean(default=False)
    dashboard_iframe = fields.Html("Dashboard Preview", sanitize=False)

    @api.model
    def create(self, vals):
        vals[
            'dashboard_iframe'] = f'''<div class="embed-responsive embed-responsive-16by9"><iframe class="embed-responsive-item" title="{vals['dashboard_name']}" width="100%" height="100%" src="{vals['dashboard_url']}" frameborder="0" allowFullScreen="true"/></div>'''
        vals['created_flag'] = True
        return super(models.Model, self).create(vals)
