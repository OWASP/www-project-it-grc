
# -*- coding: utf-8 -*-

from odoo import models, fields, api
# unzip the file and get the dashboard.json
import base64
import json
import zipfile
import io
import os
import shutil
import tempfile
import logging

_logger = logging.getLogger(__name__)


class ManaDashboardImportWizard(models.TransientModel):
    '''
    Mana Dashboard Import Wizard
    '''
    _name = 'mana_dashboard.import_wizard'
    _description = 'Import Wizard'

    file = fields.Binary(string='file', required=True)
    file_name = fields.Char(string='file name', required=True)
    name = fields.Char(string='name', required=True)

    def import_dashboard(self):
        '''
        import dashboard
        '''
        self.ensure_one()
        temp_dir = tempfile.mkdtemp()
        try:
            zip_file = zipfile.ZipFile(io.BytesIO(base64.b64decode(self.file)))
            zip_file.extractall(temp_dir)
            dashboard_json_file = os.path.join(temp_dir, 'dashboard.json')
            if not os.path.exists(dashboard_json_file):
                raise Exception('dashboard.json not found!')
            with open(dashboard_json_file, 'r') as f:
                dashboard_json = json.loads(f.read())
                dashboard_json['name'] = self.name
                self.env['mana_dashboard.dashboard'].import_dashboard(dashboard_json)
        finally:
            shutil.rmtree(temp_dir)

        return {
            'type': 'ir.actions.act_window_close'
        }
