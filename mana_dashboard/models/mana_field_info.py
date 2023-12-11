
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _


class ManaDashboardFieldInfo(models.Model):
    '''
    Field Info
    '''
    _name = 'mana_dashboard.field_info'
    _description = 'Mana Dashboard Field Info'
    _order = 'sequence, id'

    data_source_mixin = fields.Many2one(
        string='Data Source', 
        comodel_name='mana_dashboard.data_source_mixin')

    sequence = fields.Integer(string='sequence')

    field = fields.Many2one(
        string='Field',
        comodel_name='ir.model.fields')
    
    title = fields.Char(
        string='title', related='field.field_description', readonly=True)
    field_name = fields.Char(
        string='Name', related='field.name', readonly=True)
    field_type = fields.Selection(
        string='type', related='field.ttype', readonly=True, help="use for front compute")
    field_description = fields.Char(
        string='description', related='field.field_description', readonly=True)

    measure = fields.Boolean(
        string='Measure',
        default=False)
        
    show_measure = fields.Boolean(
        string='Show Measure',
        compute='_compute_show_measure')

    @api.depends('field')
    def _compute_show_measure(self):
        for record in self:
            if record.field_type in ['integer', 'float', 'monetary','boolean'] and record.field.store:
                record.show_measure = True
            else:
                record.show_measure = False

    category = fields.Boolean(
        string='Is Category',
        default=False)
    
    show_category = fields.Boolean(
        string='show category',
        compute='_compute_show_category')

    show_time = fields.Boolean(string='Show Time', compute='_compute_show_time')
    
    start_time = fields.Datetime(string='Start Time')
    end_time = fields.Datetime(string='end time')

    datetime_range = fields.Many2one(
        string='Datetime Range',
        comodel_name='mana_dashboard.field_datetime_range')
    
    relative_to = fields.Char(
        string='Relative To',
        default='$today')
    
    range_start_time = fields.Datetime(
        string='Range Start Time',
        related='datetime_range.start_time')
    range_end_time = fields.Datetime(
        string='Range End Time',
        related='datetime_range.end_time')
    previous_start_time = fields.Datetime(
        string='Previous Start Time',
        related='datetime_range.previous_start_time')
    previous_end_time = fields.Datetime(
        string='Previous End Time',
        related='datetime_range.previous_end_time')

    affect_by_global = fields.Boolean(
        string='Affect By Global', 
        default=True)
    
    search_key = fields.Char(
        string='Search Key',
        help="use for search key in search view")

    @api.depends('field')
    def _compute_show_time(self):
        for record in self:
            if record.field.ttype in ['date', 'datetime']:
                record.show_time = True
            else:
                record.show_time = False

    @api.depends('measure')
    def _compute_show_category(self):
        for record in self:
            if record.measure:
                record.show_category = False
            else:
                record.show_category = True

    aggregation_domain_ids = fields.One2many(
        string='Aggregation Domain Ids',
        compute='_compute_aggregation_dommain_id',
        comodel_name='mana_dashboard.aggregation_type')

    aggregation = fields.Many2one(
        string='Group Aggregation',
        comodel_name='mana_dashboard.aggregation_type', 
        # default=lambda self: self.env['mana_dashboard.aggregation_type'].search([('name', '=', 'count')]),
        domain="[('id', 'in', aggregation_domain_ids)]", 
        help="Just when there has group by field")

    column_agregation = fields.Many2one(
        string='Column Aggregation',
        comodel_name='mana_dashboard.aggregation_type', 
        default=lambda self: self.env['mana_dashboard.aggregation_type'].search([('name', '=', 'count')]),
        domain="[('id', 'in', aggregation_domain_ids)]")

    full_name = fields.Char(string='full name', compute='_compute_full_name')

    compare_with_last_period = fields.Boolean(
        string='Compare With Last Period',
        default=False)
    show_compare_with_last_period = fields.Boolean(
        string='Show Compare With Last Period',
        compute='_compute_show_compare_with_last_period')
    
    date_range_name = fields.Char(
        string='Date Range Name',
        default='Last Period',
        related='datetime_range.range_type')
    
    @api.depends('field')
    def _compute_show_compare_with_last_period(self):
        """
        just time field can compare with last period
        """
        for record in self:
            if record.field.ttype in ['date', 'datetime']:
                record.show_compare_with_last_period = True
            else:
                record.show_compare_with_last_period = False

    @api.constrains('measure', 'category')
    def _check_measure_category(self):
        for record in self:
            if record.measure and record.category:
                raise exceptions.ValidationError(
                    _('Measure and Category can not be both True'))

    @api.onchange('measure', 'category')
    def _onchange_measure_category(self):
        if self.measure and self.category:
            raise exceptions.ValidationError(
                _('Measure and Category can not be both True'))

    @api.depends('field')
    def _compute_aggregation_dommain_id(self):
        for record in self:
            if record.field.ttype in ['integer', 'float', 'monetary']:
                record.aggregation_domain_ids = self.env[
                    'mana_dashboard.aggregation_type'].search([])
            elif record.field.ttype in ['boolean']:
                record.aggregation_domain_ids = self.env[
                    'mana_dashboard.aggregation_type'].search([('name', 'in', ['count', 'bool_and', 'bool_or', 'every'])])
            elif record.field.ttype in ['date', 'datetime']:
                record.aggregation_domain_ids = self.env[
                    'mana_dashboard.aggregation_type'].search([('name', 'in', ['count', 'min', 'max'])])
            else:
                record.aggregation_domain_ids = self.env[
                    'mana_dashboard.aggregation_type'].search([('name', '=', 'count')])

            if record.field and record.data_source_mixin.model:
                model = self.env[record.data_source_mixin.model.model]
                fields = model._fields
                field = fields[record.field.name]
                group_operator = field.group_operator
                if group_operator:
                    record.aggregation = self.env['mana_dashboard.aggregation_type'].search(
                        [('name', '=', group_operator)])

    @api.onchange('field')
    def _onchange_aggregation_dommain_id(self):
        self._compute_aggregation_dommain_id()

    @api.onchange('field', 'aggregation')
    def _onchange_full_name(self):
        """
        onchange full name
        """
        self._compute_full_name()

    @api.depends('field', 'aggregation')
    def _compute_full_name(self):
        for record in self:
            if record.field:
                if record.aggregation:
                    record.full_name = record.field.name + ':' + record.aggregation.name
                else:
                    record.full_name = record.field.name
            else:
                record.full_name = False

    @api.onchange('datetime_range')
    def _onchange_datetime_range(self):
        """
        onchange datetime range
        """
        if self.datetime_range.range_type != 'custom':
            if self.datetime_range:
                self.start_time = self.datetime_range.start_time
                self.end_time = self.datetime_range.end_time
            else:
                self.start_time = False
                self.end_time = False
        else:
            self.start_time = False
            self.end_time = False

    def export_field_info(self):
        """
        export field info
        """ 
        self.ensure_one()
        model = self.field.model_id.model
        return {
            'model': model,
            'field': self.field.name,
            'aggregation': self.aggregation.name,
            'category': self.category,
            'measure': self.measure,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S') if self.start_time else False,
            'end_time': self.end_time.strftime('%Y-%m-%d %H:%M:%S') if self.end_time else False,
            'datetime_range': self.datetime_range.range_type,
            'affect_by_global': self.affect_by_global,
            'measure': self.measure,
            'category': self.category,
        }

    def export_field_infos(self):
        """
        export field infos
        """
        return [field.export_field_info() for field in self]

    def import_field_info(self, info):
        """
        create for export info
        """
        model_name = info['model']
        model = self.env['ir.model'].search([('model', '=', model_name)])
        if not model:
            raise exceptions.ValidationError(
                _('Model %s not found') % model_name)
        field = self.env['ir.model.fields'].search(
            [('model_id', '=', model.id), ('name', '=', info['field'])])
        if not field:
            raise exceptions.ValidationError(
                _('Field %s not found') % info['field'])

        aggregation = self.env['mana_dashboard.aggregation_type'].search(
            [('name', '=', info['aggregation'])])
        
        datetime_range = self.env['mana_dashboard.datetime_range'].search(
            [('range_type', '=', info['datetime_range'])])

        return self.create({
            'field': field.id,
            'aggregation': aggregation.id,
            'category': info['category'],
            'measure': info['measure'],
            'start_time': info['start_time'],
            'end_time': info['end_time'],
            'datetime_range': datetime_range.id,
            'affect_by_global': info['affect_by_global'],
            'measure': info['measure'],
            'category': info['category'],
        })

    def import_field_infos(self, infos):
        """
        create for export infos
        """
        records = self.env['mana_dashboard.field_info']
        for info in infos:
            records += self.import_field_info(info)
        return records
