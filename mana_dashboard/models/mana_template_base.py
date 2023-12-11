
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json


class ManaDashboardTemplateBase(models.Model):
    '''
    Mana Code Template Base
    '''
    _name = 'mana_dashboard.template_base'
    _description = 'Mana Code Template Base'

    template_id = fields.Many2one(
        string='Template',
        comodel_name='mana_dashboard.template', 
        ondelete='set null',
        domain="[('id', 'in', template_domain_ids)]")

    template_name = fields.Char(
        string='Template Name',
        related='template_id.name')
        
    component_type = fields.Char(
        string='Component Type', 
        related='template_id.component_type')

    template_category = fields.Char(string='Template Category')
    template_type = fields.Char(string='Template Type')

    multi_data_source = fields.Boolean(
        string='Multi Data Source', related='template_id.multi_data_source')

    template_domain_ids = fields.One2many(
        string='Template Domain',
        comodel_name='mana_dashboard.template',
        compute='_compute_template_domain_ids')

    template = fields.Text(string='Template')
    has_template = fields.Boolean(string='Has Template', related='template_id.has_template')

    styles = fields.Text(string='Styles')
    has_styles = fields.Boolean(string='Has Styles', related='template_id.has_styles')

    scripts = fields.Text(string='Scripts')
    has_scripts = fields.Boolean(string='Has Scripts', related='template_id.has_scripts')

    default_scripts = fields.Text(
        string='Default Scripts')

    disable_children = fields.Boolean(
        string='Disable Children', related='template_id.disable_children')
    disable_first_child = fields.Boolean(
        string='Disable First Child', related='template_id.disable_first_child')

    # json data for demo
    demo_data = fields.Text(
        string='Demo Data')
    demo_template = fields.Text(
        string='Demo Template', 
        help="Demo Template")
    has_demo_template = fields.Boolean(
        string='Has Demo Template', 
        related='template_id.has_demo_template')

    history_datas = fields.Many2many(
            string='History Data',
            comodel_name='mana_dashboard.history_data')
    
    history_data_domain_ids = fields.One2many(
        string='History Data Domain',
        comodel_name='mana_dashboard.history_data',
        compute='_compute_history_data_domain_ids')

    help = fields.Html(string='Help', related='template_id.help')
    preview = fields.Binary(string='Preview', related='template_id.preview')

    # ui related
    need_measure = fields.Boolean(
        string='Need Measure', related='template_id.need_measure')
    need_category = fields.Boolean(
        string='Need Category', related='template_id.need_category')
    need_column_aggregation = fields.Boolean(
        string='Need Column Aggregation', related='template_id.need_column_aggregation')
    
    supported_series_types = fields.Many2many(
        comodel_name='mana_dashboard.series_type',
        related='template_id.supported_series_types')
    
    is_custom = fields.Boolean(
        string='Is Custom', related='template_id.is_custom')
    
    preview_background_color = fields.Char(
        string='Preview Background Color')
    
    get_previous_data = fields.Boolean(
        string='Get Previous Data', 
        related='template_id.get_previous_data')
    
    @api.depends('template_id')
    def _compute_preview_background_color(self):
        for record in self:
            if record.template_id:
                record.preview_background_color = record.template_id.preview_background_color
            else:
                record.preview_background_color = '#ffffff'

    @api.onchange('template_id')
    def onchange_template(self):
        '''
        onchange template, as to avoid discard the changes
        '''
        if self.template or self.styles or self.scripts:
            self.save_history_data()

        self.template = self.template_id.template
        self.styles = self.template_id.styles

        self.disable_children = self.template_id.disable_children
        self.disable_first_child = self.template_id.disable_first_child

        self.demo_template = self.template_id.demo_template
        self.demo_data = self.template_id.demo_data
        
        self.scripts = self.template_id.scripts
        self.default_scripts = self.template_id.default_scripts

    @api.depends('history_datas')
    def _compute_history_data_domain_ids(self):
        for record in self:
            if record.history_datas:
                record.history_data_domain_ids = record.history_datas.ids
            else:
                record.history_data_domain_ids = False

    def get_history_title(self):
        """
        Get History Title, this method should be override
        """
        return 'History Data {date}'.format(date=fields.Datetime.now())
    
    def get_history_title(self):
        """
        Get History Title, this method should be override
        """
        return 'History Data {date}'.format(date=fields.Datetime.now())
    
    def get_history_data(self):
        '''
        get history data, this method should be override
        '''
        self.ensure_one()
        history_data = {
            'template': self.template,
            'styles': self.styles,
            'scripts': self.scripts,
        }
        return history_data

    def save_history_data(self):
        '''
        save history data
        '''
        self.ensure_one()

        # get history data
        history_data = self.get_history_data()
        title = self.get_history_title()

        # save history data
        self.history_datas = [(0, 0, {
            'title': title,
            'data': json.dumps(history_data),
        })]

        # notify save success
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Save Success',
                'message': 'Save Success',
                'sticky': False,
            }
        }

    @api.depends('template_category')
    def _compute_template_domain_ids(self):
        for record in self:
            if record.template_category:
                domain = [('category', '=', record.template_category)]
                if record.template_type:
                    domain.append(('type', '=', record.template_type))
                record.template_domain_ids = self.env['mana_dashboard.template'].search(domain).ids
            else:
                record.template_domain_ids = self.env['mana_dashboard.template'].search([]).ids

    def get_component_type(self):
        '''
        get component type
        '''
        self.ensure_one()
        return self.component_type
