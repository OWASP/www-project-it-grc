
# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import func, misc, transpile_javascript, is_odoo_module
import re
import xw_utils


class ManaJsResource(models.TransientModel):
    '''
    Js Resource
    '''
    _name = 'mana_dashboard_base.js_resource'
    _description = 'Js Resource'

    @api.model
    def get_js_resource(self):
        """
        get js resource
        """
        code_infos = xw_utils.get_code_infos()
        content = ''
        for code_info in code_infos:
            code = code_info['code']
            if is_odoo_module(code):
                code = transpile_javascript(
                    'mana_dashboard/static/src/base_code/{name}'.format(name=code_info['name'].replace('.', '_').lower()), code)
            content += code + ';\n'

        return content
