# -*- coding: utf-8 -*-

from odoo import http
import json


class ManaDashboard(http.Controller):

    @http.route('/mana_dashboard/export_dashboard/<int:dashboard_id>', type='http', auth='user')
    def export_dashboard(self, **kw):
        """
        export dashboard as a zip file
        """
        dashboard_id = kw.get('dashboard_id', False)
        if dashboard_id:
            dashboard = http.request.env['mana_dashboard.dashboard'].sudo().search([('id', '=', dashboard_id)])
            if dashboard:
                dashboard_json = dashboard.export_dashboard()
                dashboard_json = json.dumps(dashboard_json, indent=4).encode('utf-8')
                # make a zip file
                import zipfile
                import io
                zip_buffer = io.BytesIO()
                zip_file = zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED)
                dashboard_name = dashboard.name
                # normalize name
                import re
                dashboard_name = re.sub(r'[^a-zA-Z0-9]', '_', dashboard_name)
                # write json to zip file
                zip_file.writestr('dashboard.json', dashboard_json)
                zip_file.close()
                zip_buffer.seek(0)
                # make a response
                return http.request.make_response(zip_buffer, headers=[
                    ('Content-Type', 'application/zip'),
                    ('Content-Disposition', 'attachment; filename=%s.zip;' % dashboard_name),
                ])
        return http.request.not_found()
