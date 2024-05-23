import base64

from odoo import models, fields, api
from odoo.modules import get_module_resource


class ThemeInh(models.TransientModel):
    _inherit = 'theme.data'

    def icon_change_theme_default(self):
        res = super(ThemeInh,self).icon_change_theme_default()
        menu_item = self.env['ir.ui.menu'].sudo().search([('parent_id', '=', False)])
        if self.env.user.lang == 'es_MX':
            text = 'Campaña Concientización'
        else:
            text = 'Awareness Campaign'
        for menu in menu_item:
            if menu.name == text:
                img_path = get_module_resource(
                    'grcbit_iso27001', 'static', 'src', 'img'
                    'email-marketing.png')
                menu.write({'web_icon_data': base64.b64encode(
                    open(img_path, "rb").read())})
        return res