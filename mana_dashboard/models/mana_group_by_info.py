# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ManaDashboardGroupbyInfo(models.Model):
    '''
    Mana Dashboard Groupby Info
    '''
    _name = 'mana_dashboard.group_by_info'
    _description = 'group by info'
    _order = 'sequence, id'

    sequence = fields.Integer(string='sequence')

    data_source_mixin = fields.Many2one(
        string='Data source mixin',
        comodel_name='mana_dashboard.data_source_mixin')

    field = fields.Many2one(
        string='Field', 
        comodel_name='ir.model.fields',
        domain="[('store', '=', True), ('name', '!=', 'id'), ('ttype', 'in', ['boolean', 'char', 'date', 'datetime', 'integer','many2one', 'many2many', 'selection', 'float', 'monetary'])]")
    
    field_name = fields.Char(
        string='Field Name',
        related='field.name',
        readonly=True)
    
    field_type = fields.Selection(
        string='Field Type',
        related='field.ttype',
        readonly=True)
    
    field_description = fields.Char(
        string='Field Description',
        related='field.field_description',
        readonly=True)

    type = fields.Selection(string='Field Type', related='field.ttype', readonly=True)
    full_name = fields.Char(string='Full Name', compute='_compute_full_name')

    @api.depends('field', 'show_granularity', 'granularity')
    def _compute_full_name(self):
        for record in self:
            if record.show_granularity and record.granularity:
                record.full_name = record.field.name + ':' + record.granularity
            else:
                record.full_name = record.field.name

    @api.onchange('field', 'show_granularity', 'granularity')
    def _onchange_full_name(self):
        self._compute_full_name()

    @api.depends('field')
    def _compute_show_aggregation(self):
        """
        field type
        """
        for record in self:
            if record.field.ttype in ['boolean', 'integer', 'float', 'monetary']:
                record.show_aggregation = True
            else:
                record.show_aggregation = False

    show_granularity = fields.Boolean(
        string='show granularity',
        compute='_compute_show_granularity')

    granularity = fields.Selection(
        string='granularity',
        selection=[
            ('year', 'year'),
            ('month', 'month'),
            ('day', 'day'),
            ('hour', 'hour'),
            ('minute', 'minute'),
            ('second', 'second'),
            ('week', 'week'),
        ])

    @api.depends('field')
    def _compute_show_granularity(self):
        for record in self:
            if record.field.ttype == 'date' or record.field.ttype == 'datetime':
                record.show_granularity = True
            else:
                record.show_granularity = False

    def export_group_by_info(self):
        """
        export group by info
        """
        model_name = self.field.model_id.model
        return {
            'model': model_name,
            'field': self.field.name,
            'granularity': self.granularity,
            'sequence': self.sequence,
        }

    def export_group_by_infos(self):
        """
        export group by infos
        """
        return [group_by_info.export_group_by_info() for group_by_info in self]

    def import_group_by_info(self, group_by_info):
        """
        import group by info
        """
        model_name = group_by_info['model']
        model = self.env['ir.model'].search([('model', '=', model_name)])
        if not model:
            raise ValueError('model not found: %s' % model_name)
        field = self.env['ir.model.fields'].search(
            [('model_id', '=', model.id), ('name', '=', group_by_info['field'])])
        if not field:
            raise ValueError('field not found: %s' % group_by_info['field'])

        return self.create({
            'field': field.id,
            'sequence': group_by_info.get('sequence', 0),
            'granularity': group_by_info.get('granularity', False) 
        })

    def import_group_by_infos(self, group_by_infos):
        """
        import group by infos, return group by info ids
        """
        records = self.env['mana_dashboard.group_by_info']
        for group_by_info in group_by_infos:
            records += self.import_group_by_info(group_by_info)
        return records