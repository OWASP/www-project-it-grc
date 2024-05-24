# -*- coding: utf-8 -*-
""" This file add two objects """
from odoo import fields, models, api, _

class ZeroTrustSettings(models.Model):
    _name = 'zerotrust.settings.zt'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    is_zerotrust = fields.Boolean(string="ZTrust", default=lambda x: x._default_get_last())

    def _default_get_last(self):
        last_one = self.env['zerotrust.settings.zt'].sudo().search([], order="create_date DESC", limit=1)
        if last_one:
            for rec in last_one:
                return rec.is_zerotrust
        else:
            return True

    def zt_enable(self):
        for rec in self:
            rec.is_zerotrust = True

    def zt_disable(self):
        for rec in self:
            rec.is_zerotrust = False


class TagZT(models.Model):
    _name = "dashboard.tag.zt"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "dashboard Tag ZT"

    name = fields.Char('Tag Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]


class BackendDashboardZT(models.Model):
    _name = 'backend.dashboard.zt'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = 'sequence, id'

    name = fields.Char('Name')
    comment = fields.Text(string='Notes')
    color = fields.Integer('Color Index')
    user_id = fields.Many2one(
        'res.users',
        string='Owner',
        ondelete='cascade',
        track_visibility='onchange',
        default=lambda self: self.env.uid,
        help="Owner dashboard")
    url = fields.Char(
        'URL',
        index=True,
        track_visibility='onchange')
    active = fields.Boolean('Active', default=True)
    sequence = fields.Integer()
    tag_ids = fields.Many2many(
        'dashboard.tag.zt',
        'dashboard_tags_zt_rel',
        'dashboard_id',
        'tag_id',
        string='Tags')
    main_dashboard = fields.Boolean('Main Dashboard', default=False)
    height = fields.Integer('Height(px)', default='750', help='Height in px')
    width = fields.Integer('Width(%)', default='100', help='Width in %')
    zerotrust_enable = fields.Boolean(string="ZT Eneable", compute="_compute_check_iszt")
    url_zt = fields.Char(string="URL ZT")



    @api.depends('name')
    def _compute_check_iszt(self):
        last_one = self.env['zerotrust.settings.zt'].sudo().search([], order="create_date DESC", limit=1)
        if last_one:
            for rec in last_one:
                self.zerotrust_enable = rec.is_zerotrust
        else:
            self.zerotrust_enable = True

    def get_dashboard(self):
        """ to visit your dashboard """
        
        if self.zerotrust_enable == True:
            action = {
                'type': 'ir.actions.client',
                'tag': 'view_dashboard_zt',
                'params': {
                    'url': self.url_zt,
                    'height': self.height,
                    'width': self.width,
                    'main_dashboard': self.main_dashboard,
                    'zerotrust_enable': self.zerotrust_enable,
                },
            }
        elif self.zerotrust_enable == False:
            action = {
                'type': 'ir.actions.client',
                'tag': 'view_dashboard_zt',
                'params': {
                    'url': self.url,
                    'height': self.height,
                    'width': self.width,
                    'main_dashboard': self.main_dashboard,
                    'zerotrust_enable': self.zerotrust_enable,
                },
            }
        else:
            action = {'warning': {'title': _("Warning"), 'message': _(
                "Wrong configuration for the iframe"), }, }
        return action
