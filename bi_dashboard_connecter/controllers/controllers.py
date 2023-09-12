import json

import requests

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request, Response
from .. import common_url


class QueryEditor(http.Controller):

    @http.route('/report', type='http', auth="user", website=True, csrf=False, cors='*')
    def show_saved_report(self, **kw):
        report_id = kw.get('id')

        report_object = request.env['bi.dashboard'].sudo().search([('dashboard_id', '=', report_id)])
        cred_object = request.env['bi.cred'].sudo().search([])[0]

        return request.render('bi_dashboard_connecter.main_report_window',
                              {'report': cred_object, 'rep': report_object})

    @http.route('/cred', type='http', auth='user', methods=['GET'], website=True)
    def table_result(self, **kw):
        report_id = kw.get('id')
        report_object = request.env['bi.dashboard'].sudo().search([('dashboard_id', '=', report_id)])
        cred_object = request.env['bi.cred'].sudo().search([])[0]
        base_url = http.request.httprequest.url_root
        req = f"{base_url}power-bi/auth/?username={cred_object.username}&password={cred_object.password}&client_id={cred_object.client_id}"
        headers = {"Content-Type": "multipart/form-data"}
        response = requests.post(req, headers=headers)

        if response.status_code == 200:
            token1 = response.json()
            token = token1['access_token']
        else :
            return ValidationError("Check you credentials or check API's permissions/ or you have 0 Dashboards!!!!!")

        data_object = {
            "report_id": report_id,
            'url': report_object.dashboard_url,
            'token': token
        }

        return json.dumps(data_object)

    @http.route('/power-bi/auth/', auth='public', type='http', methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    def powerbi_authentication(self, **kw):
        authentication_url = 'https://login.windows.net/common/oauth2/token'
        parameters = {'grant_type': 'password', 'resource': 'https://analysis.windows.net/powerbi/api',
                      'username': kw.get('username'), 'password': kw.get('password'), 'client_id': kw.get('client_id'),
                      'scope': 'openid'}

        res = requests.post(url=authentication_url, data=parameters)
        print(res)
        # response = Response(json.dumps(res), content_type='application/json', status=status)
        status = res.status_code
        if status == 200:
            res = res.json()
            response = Response(json.dumps(res), content_type='application/json', status=status)
            response.status = str(status)
            return response
