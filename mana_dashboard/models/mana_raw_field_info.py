# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ManaDashboardRawFieldInfo(models.Model):
    '''
    Raw Field Info
    '''
    _name = 'mana_dashboard.raw_field_info'
    _description = 'Mana Raw Field Info'

    sequence = fields.Integer(string='sequence')
    data_source_mixin = fields.Many2one(
        'mana_dashboard.data_source_mixin', string='Data Source Mixin')
        
    name = fields.Char(string='Name', required=True)
    full_name = fields.Char(string='Full Name', compute='_compute_full_name')

    alias = fields.Char(string='Alias')

    measure = fields.Boolean(string='Measure', default=False)
    show_measure = fields.Boolean(string='Show Measure', default=False)

    category = fields.Boolean(string='Category (X axis)', default=False)
    show_category = fields.Boolean(string='Show Category', default=False)

    group_by = fields.Boolean(string='Group By', default=False)
    show_group_by = fields.Boolean(string='Show Group By', default=False)

    column_arggregation = fields.Selection(
        string='Column Arggregation',
        selection=[
            ('sum', 'Sum'), 
            ('avg', 'Average'), 
            ('count', 'Count'),
            ('min', 'Min'), 
            ('max', 'Max')],
        default=False)
    
    type = fields.Selection(
        string='Field Type',
        selection=[
            ('char', 'Char'), 
            ('integer', 'Integer'),
            ('float', 'Float'),
            ('date', 'Date'), 
            ('datetime', 'Datetime'), 
            ('boolean', 'Boolean'), 
            ('binary', 'Binary'), 
            ('array', 'Array'),
            ('other', 'Other')],
        default=False)

    alias = fields.Char(string='Alias')

    supported_series_types = fields.Many2many(
        string='Supported Series Types',
        comodel_name='mana_dashboard.series_type',
        relation='mana_dashboard_raw_field_info_series_type_rel',
        column1='raw_field_info_id',
        column2='series_type_id')
    
    series_type = fields.Many2one(
        string='Series Type',
        comodel_name='mana_dashboard.series_type',
        ondelete='set null',
        domain="[('id', 'in', supported_series_types)]")
    
    series_type_name = fields.Char(
        string='Series Type Name', related='series_type.name')
    
    hidden = fields.Boolean(string='Hide', default=False)

    @api.onchange('category')
    def _onchange_category(self):
        if self.category:
            self.measure = False
            self.show_measure = False

    @api.onchange('measure')
    def _onchange_measure(self):
        if self.measure:
            self.category = False
            self.show_category = False

    @api.depends('column_arggregation')
    def _compute_bottomCalc(self):
        for record in self:
            if record.column_arggregation:
                record.bottomCalc = record.column_arggregation
            else:
                record.bottomCalc = False

    @api.depends('name', 'column_arggregation')
    def _compute_full_name(self):
        for record in self:
            if record.name and record.column_arggregation:
                record.full_name = '%s:%s' % (record.name, record.column_arggregation)
            else:
                record.full_name = record.name

    def export_raw_field_info(self):
        return {
            'name': self.name,
            'measure': self.measure,
            'category': self.category,
            'group_by': self.group_by,
            'column_arggregation': self.column_arggregation,
            'alias': self.alias,
            'series_type': self.series_type.name if self.series_type else False,
            'hidden': self.hidden,
        }

    def export_raw_field_infos(self):
        return [raw_field_info.export_raw_field_info() for raw_field_info in self]

    @api.model
    def import_raw_field_infos(self, raw_field_infos):
        """
        :param raw_field_infos: list of dict
        :return: self
        """
        for info in raw_field_infos:
            series_type = info.get('series_type')
            if series_type:
                series_type = self.env['mana_dashboard.series_type'].search(
                    [('name', '=', series_type)])
                info['series_type'] = series_type.id
        return self.create(raw_field_infos)
    
    @api.depends('supported_series_types')
    def _compute_series_type_domain_ids(self):
        for record in self:
            record.series_type_domain_ids = record.supported_series_types.ids or []

    @api.onchange('name')
    def _onchange_name(self):
        # alias
        if not self.alias:
            self.alias = self.name
        # hidden
        if self.name == 'id' and not self.hidden:
            self.hidden = True
