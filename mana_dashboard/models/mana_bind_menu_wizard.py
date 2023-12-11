
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ManaDashboardBindMenuWizard(models.TransientModel):
    '''
    Bind Menu Wizard
    '''
    _name = 'mana_dashboard.bind_menu_wizard'
    _description = 'Bind Menu Wizard'

    name = fields.Char(string='name', required=True)
    parent_id = fields.Many2one(string='Parent Menu', comodel_name='ir.ui.menu')
    action_id = fields.Many2one(string='action', comodel_name='ir.actions.client', required=True)
    sequence = fields.Integer(string='sequence', default=10, required=True)
    group_access_ids = fields.Many2many(string="Menu Group Access", comodel_name='res.groups')
    
    def bind_menu(self):
        """
        Bind Menu
        """
        self.ensure_one()

        self.env['ir.ui.menu'].create({
            'name': self.name,
            'parent_id': self.parent_id.id,
            'sequence': self.sequence,
            'action': 'ir.actions.client,%d' % (self.action_id.id),
            'groups_id': [(6, 0, self.group_access_ids.ids)]
        })

        return {'type': 'ir.actions.act_window_close'}