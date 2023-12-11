
# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from odoo.modules.module import get_resource_path
import base64

default_svg_icon = '<svg class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"><path d="M938.667 443.733V140.8c0-25.6-21.334-46.933-46.934-46.933H576c-25.6 0-46.933 21.333-46.933 46.933v302.933c0 25.6 21.333 46.934 46.933 46.934h315.733c25.6 0 46.934-21.334 46.934-46.934z m-806.4 93.867c-25.6 0-46.934 21.333-46.934 46.933v302.934c0 25.6 21.334 46.933 46.934 46.933H448c25.6 0 46.933-21.333 46.933-46.933V584.533c0-25.6-21.333-46.933-46.933-46.933H132.267zM307.2 332.8h-46.933c0-81.067 68.266-149.333 149.333-149.333h17.067c12.8 0 21.333-8.534 21.333-21.334v-55.466c0-12.8-8.533-21.334-21.333-21.334H409.6c-136.533 0-247.467 110.934-247.467 247.467h-55.466c-8.534 0-12.8 8.533-12.8 17.067 0 4.266 0 4.266 4.266 8.533L192 465.067c8.533 8.533 21.333 8.533 29.867 0L315.733 358.4c4.267-4.267 4.267-12.8 0-17.067-4.266-4.266-4.266-8.533-8.533-8.533z m409.6 358.4h46.933c0 81.067-68.266 149.333-149.333 149.333h-17.067c-12.8 0-21.333 8.534-21.333 21.334V921.6c0 12.8 8.533 21.333 21.333 21.333H614.4c136.533 0 247.467-110.933 247.467-247.466h55.466c8.534 0 12.8-4.267 12.8-12.8 0-4.267 0-4.267-4.266-8.534L832 567.467c-8.533-8.534-21.333-8.534-29.867 0l-93.866 106.666c-4.267 4.267-4.267 12.8 0 17.067 0-4.267 4.266 0 8.533 0z"></path></svg>'

class ManaDashboardSendToDashboard(models.Model):
    '''
    Send to dashboard wizard
    '''
    _name = 'mana_dashboard.send_to_dashboard'
    _description = 'Mana send to dashboard'

    name = fields.Char(string='Name', required=True)
    category = fields.Many2one(
        string='Category', 
        comodel_name='mana_dashboard.action_block_category',
        required=True)
    svg_icon = fields.Text(string='Svg Icon', default=default_svg_icon, required=True)
    shared = fields.Boolean(string='Shared', default=False)
