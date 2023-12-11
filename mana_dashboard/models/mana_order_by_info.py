# -*- coding: utf-8 -*-

from dataclasses import field
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class OrderByInfo(models.Model):
    '''
    mana dashboard order by info
    '''
    _name = "mana_dashboard.order_by_info"
    _description = "Mana Dashboard Chart Order By Info"
    _order = 'sequence, id'

    data_source_mixin = fields.Many2one(
        string='data source mixin',
        comodel_name='mana_dashboard.data_source_mixin')

    field = fields.Many2one(
        string='field', 
        comodel_name='ir.model.fields',
        domain="[('store', '=', True), ('name', '!=', 'id'), ('ttype', 'in', ['boolean', 'char', 'date', 'datetime', 'integer','many2one', 'many2many', 'selection'])]"
    )

    field_name = fields.Char(
        string='field name', 
        related='field.name', 
        readonly=True)
    field_type = fields.Selection(
        string='field type',
        related='field.ttype',
        readonly=True)
    field_description = fields.Char(
        string='field description',
        related='field.field_description',
        readonly=True)

    sequence = fields.Integer(string='sequence')

    order_type = fields.Selection(
        string='order type', 
        required=True,
        selection=[('asc', 'asc'), ('desc', 'desc')], 
        default='asc')

    full_name = fields.Char(string='full name', compute='_compute_full_name')

    @api.depends('field', 'order_type')
    def _compute_full_name(self):
        for record in self:
            if record.field and record.order_type:
                record.full_name = record.field.name + ' ' + record.order_type
            else:
                record.full_name = False

    def export_order_by_info(self):
        """
        export order by info
        """
        model_name = self.field.model_id.model
        return {
            'model': model_name,
            'sequence': self.sequence,
            'field_name': self.field_name,
            'order_type': self.order_type
        }

    def export_order_by_infos(self):
        """
        export order by infos
        """
        order_by_infos = []
        for order_by_info in self:
            order_by_infos.append(order_by_info.export_order_by_info())
        return order_by_infos

    def import_order_by_info(self, order_by_info):
        """
        import order by info
        """
        model_name = order_by_info.get('model')
        model = self.env['ir.model'].search([('model', '=', model_name)])
        if not model:
            raise UserError(_('Model %s not found') % model_name)

        field_name = order_by_info.get('field_name')
        field = self.env['ir.model.fields'].search([('model_id', '=', model.id), ('name', '=', field_name)])
        if not field:
            raise UserError(_('Field %s not found') % field_name)

        order_type = order_by_info.get('order_type')
        if order_type not in ['asc', 'desc']:
            raise UserError(_('Order Type %s not found') % order_type)

        return self.create({
            'field': field.id,
            'sequence': order_by_info.get('sequence', 0),
            'order_type': order_type
        })

    def import_order_by_infos(self, order_by_infos):
        """
        import order by infos
        """
        order_by_infos = self.env['mana_dashboard.order_by_info']
        for order_by_info in order_by_infos:
            order_by_infos += self.import_order_by_info(order_by_info)
        return order_by_infos
