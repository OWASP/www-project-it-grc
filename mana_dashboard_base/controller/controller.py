# -*- coding: utf-8 -*-

import odoo
import odoo.modules.registry
from odoo.tools.translate import _
from odoo.addons.web.controllers.main import CONTENT_MAXAGE
from odoo.addons.web.controllers.home import Home as Home
from odoo import http
from odoo.http import request
import xw_utils

import json
import base64
import functools
import io
import os
import logging
from io import BytesIO
from odoo.http import STATIC_CACHE_LONG

BASE_PATH = os.path.dirname(os.path.dirname(__file__))

class ManaWeb(Home):
    '''
    inhere home to extend web.login style
    '''
    @http.route('/mana_dashboard_base/js_resource', type='http', auth="none")
    def js_resource(self):
        """"
        get js resource
        """
        content = request.env['mana_dashboard_base.js_resource'].sudo().get_js_resource()
        return request.make_response(content, [
                ('Content-Type', 'text/javascript'),
                ('Cache-Control','public, max-age=' + str(STATIC_CACHE_LONG))
            ])

