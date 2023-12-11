# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

default_svg = '<svg class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" width="200" height="200"><path d="M85.312 512a426.688 426.688 0 0 0 844.8 85.312H426.688V93.888A426.816 426.816 0 0 0 85.312 512zM512 0v512h512a512 512 0 1 1-512-512z m506.816 438.848H585.152V5.184a512.32 512.32 0 0 1 433.664 433.664z" fill="#ffffff"></path></svg>'

class DashboardActionBlocks(models.Model):
    '''
    dashboard blocks, this blocks if from other views
    '''
    _name = "mana_dashboard.action_blocks"
    _description = "Mana Dashboard Action Blocks"

    name = fields.Char(string='Name')
    uid = fields.Many2one(
        'res.users', string='User', default=lambda self: self.env.user)
    svg_icon = fields.Text(string='Svg Icon')

    category = fields.Many2one(
        string='Category', comodel_name='mana_dashboard.action_block_category')
    share = fields.Boolean(string='Share', default=False)
    action_id = fields.Char(string='Action Id')

    view_mode = fields.Char(string='View Mode')
    context = fields.Char(string='Context')
    domain = fields.Char(string='Domain', help="maybe the user will dynamic set the domain")
    description = fields.Text(string='Description')

    @api.model
    def load_action_blocks(self):
        '''
        get blocks from warehouse
        '''
        uid = self.env.user.id
        blocks = self.env['mana_dashboard.action_blocks'].search(
            ['|', ('uid', '=', uid), ('share', '=', True)])

        return blocks.read()

    @api.model
    def send_to_dashboard(self, action_info):
        """
        add action to dashboard library
        """
        record = self.env['mana_dashboard.action_blocks'].search(
            [('action_id', '=', action_info.get('action_id')), ('name', '=', action_info.get('name'))])
        if not record:
            self.env['mana_dashboard.action_blocks'].create({
                'uid': self.env.user.id,
                'action_id': action_info.get('action_id'),
                'view_mode': action_info.get('view_mode'),
                'name': action_info.get('name'),
                'category': action_info.get('category'),
                'domain': str(action_info.get('domain') or []),
                'context': str(action_info.get('context_to_save') or {}),
                'svg_icon': action_info.get('svg_icon') or default_svg,
            })
            return True
        else:
            return False