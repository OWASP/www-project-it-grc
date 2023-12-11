# -*- coding: utf-8 -*-

from odoo import models, fields, _, api, tools, exceptions

default_ptyhon_code = '''
# use the result var to get the data
# write your code here, and assign your data to result
result = [
    { product: 'Matcha Latte', '2015': 43.3, '2016': 85.8, '2017': 93.7 },
    { product: 'Milk Tea', '2015': 83.1, '2016': 73.4, '2017': 55.1 },
    { product: 'Cheese Cocoa', '2015': 86.4, '2016': 65.2, '2017': 82.5 },
    { product: 'Walnut Brownie', '2015': 72.4, '2016': 53.9, '2017': 39.1 }
]
'''

default_json_code = '''
[
    { product: 'Matcha Latte', '2015': 43.3, '2016': 85.8, '2017': 93.7 },
    { product: 'Milk Tea', '2015': 83.1, '2016': 73.4, '2017': 55.1 },
    { product: 'Cheese Cocoa', '2015': 86.4, '2016': 65.2, '2017': 82.5 },
    { product: 'Walnut Brownie', '2015': 72.4, '2016': 53.9, '2017': 39.1 }
]
'''

default_sql_code = '''
select id from res_partner group by city order by count('id') desc limit 10
'''


class ManaDataSourceMixin(models.Model):
    '''
    Mana Dashboard Data Source Mixin
    '''
    _name = 'mana_dashboard.data_source_mixin'
    _description = 'Mana Dashboard Data Source Mixin'

    name = fields.Char(string='Name')

    config_id = fields.Many2one(
        string='Multi Source Config',
        comodel_name='mana_dashboard.config',
        ondelete='cascade', help='Multi Source Config')

    # must override this field in mana_dashboard.config
    template_id = fields.Many2one(
        string='Template',
        comodel_name='mana_dashboard.template',
        related='config_id.template_id')

    default_sql = fields.Text(
        string='Default SQL', related='template_id.default_sql')
    default_code = fields.Text(
        string='Default Code', related='template_id.default_code')
    default_json = fields.Text(
        string='Default JSON', related='template_id.default_json')

    dashboard_id = fields.Many2one(
        string='Dashboard',
        comodel_name='mana_dashboard.dashboard',
        related='config_id.dashboard_id')

    config_help = fields.Html(string='config_help', related='config_id.help')

    # for the data we need not change, just related to template
    supported_data_source_types = fields.Many2many(
        comodel_name='mana_dashboard.data_source_type',
        related='template_id.supported_data_source_types')

    # data source type domain ids
    data_source_type_domain_ids = fields.One2many(
        string='Data Source Type Domain',
        compute='_compute_data_source_type_domain_ids',
        comodel_name='mana_dashboard.data_source_type')

    # data source type
    data_source_type = fields.Many2one(
        string='Data Source',
        comodel_name='mana_dashboard.data_source_type',
        domain="[('id', 'in', data_source_type_domain_ids)]")

    data_source_type_name = fields.Char(
        string='Source Type Name', 
        related='data_source_type.name')

    # 1\ get data from model
    model = fields.Many2one(
        string='Model', 
        comodel_name='ir.model', 
        domain=[
            ('transient', '=', False), 
            ('model', 'not in', ['Unknown', 'Base', '_unknown', 'base']), 
            ('model', 'not like', 'Tests%'), 
            ('model', 'not like', '%.mixin%'),
        ])

    domain = fields.Text(string='Domain', default='[]')
    context = fields.Text(string='Context', default='{}')
    model_name = fields.Char(string='Model Name', related='model.model', readonly=True)

    # drill domain
    drill_field = fields.Many2one(
        string='Drill Field',
        comodel_name='ir.model.fields',
        domain="[('model_id', '=', model)]")
    
    # drill down config
    drill_domain_type = fields.Selection(
        string='Drill Domain Type',
        selection=[
            ('standard', 'Standard'),
            ('custom', 'Custom'),
        ],
        default='standard'
    )
    drill_operator = fields.Selection(
        string='Drill Operator',
        selection=[
            ('=', '='),
            ('!=', '!='),
            ('>', '>'),
            ('>=', '>='),
            ('<', '<'),
            ('like', 'like'),
            ('ilike', 'ilike'),
            ('in', 'in'),
            ('not in', 'not in'),
            ('child_of', 'child_of'),
            ('parent_of', 'parent_of'),
        ],
        default='='
    )
    drill_domain = fields.Char(string='Drill Domain')
    drill_extra_domain = fields.Text(string='Drill Extra Domain', default='[]')

    # link to config
    link_to_config = fields.Many2one(
        string='Link To Config',
        comodel_name='mana_dashboard.any_config',
        domain="[('dashboard_id', '=', dashboard_id)]")

    link_action_field = fields.Many2one(
        string='Link Action Field',
        comodel_name='ir.model.fields',
        domain="[('model_id', '=', model)]")
        
    link_action_operator = fields.Selection(
        string='Link Action Operator',
        selection=[
            ('=', '='),
            ('!=', '!='),
            ('>', '>'),
            ('>=', '>='),
            ('<', '<'),
            ('like', 'like'),
            ('ilike', 'ilike'),
            ('in', 'in'),
            ('not in', 'not in'),
            ('child_of', 'child_of'),
            ('parent_of', 'parent_of'),
        ],
        default='='
    )
    link_action_domain = fields.Text(string='Link Action Domain', default='[]')

    # do not name it as fields, because it will conflict with fields
    model_fields = fields.One2many(
        string='Model Fields', 
        comodel_name='mana_dashboard.field_info',
        inverse_name='data_source_mixin',
        copy=True)

    has_time_field = fields.Boolean(
        string='Has Time Fields',
        compute='_compute_has_time_field')
    
    parameter_ids = fields.One2many(
        string='Parameters',
        comodel_name='mana_dashboard.parameter',
        inverse_name='data_source_mixin_id')

    @api.depends('model_fields')
    def _compute_has_time_field(self):
        for record in self:
            record.has_time_field = bool(record.model_fields.filtered(lambda x: x.show_time))

    # raw fields
    raw_fields = fields.One2many(
        string='Raw Fields', 
        comodel_name='mana_dashboard.raw_field_info',
        inverse_name='data_source_mixin',
        copy=True)

    category_field = fields.Many2one(
        string='Category Field',
        comodel_name='mana_dashboard.raw_field_info',
        domain="[('data_source_mixin', '=', id)]",
        copy=True)

    # compute has multi group by
    multi_group_by = fields.Boolean(
        string='Multi Group By',
        compute='_compute_multi_group_by')

    group_by_infos = fields.One2many(
        string='Group By',
        comodel_name='mana_dashboard.group_by_info',
        inverse_name='data_source_mixin',
        copy=True)

    has_group_by = fields.Boolean(
        string='Has Group By',
        compute='_compute_has_group_by')

    def _compute_has_group_by(self):
        for record in self:
            record.has_group_by = bool(record.group_by_infos)
    
    order_by_infos = fields.One2many(
        string='Order By', 
        comodel_name='mana_dashboard.order_by_info',
        inverse_name='data_source_mixin',
        copy=True)

    limit = fields.Integer(string='Limit', default=0)

    # 2\ rpc method
    method = fields.Char(string='Method')
    
    # 3\ get data from sql
    sql = fields.Text(
        string='Sql', 
        default=default_sql_code,
        help="User can use custom sql to get datas")

    # 4\ get data from record
    res_id = fields.Integer(string='Res Id')

    # 5\ get data from json
    json_data_format = fields.Selection(
        string='Json Data Format',
        selection=[('key_val', 'Key & Val'), ('dimensions_datas', 'Dimensions & Datas')],
        default='key_val')
    json_data = fields.Text(string='Json Data', default=default_json_code)

    # 6\ get data from python code
    code = fields.Text(string='Python Code', default=default_code)

    # 7\ result types
    supported_result_types = fields.Many2many(
        string='Supported Result Types',
        comodel_name='mana_dashboard.result_type',
        related='template_id.supported_result_types')

    result_type_domain_ids = fields.One2many(
        string='Result Type Domain',
        comodel_name='mana_dashboard.result_type',
        compute='_compute_result_type_domain_ids')

    result_type = fields.Many2one(
        string='Result Type',
        comodel_name='mana_dashboard.result_type',
        domain="[('id', 'in', result_type_domain_ids)]")

    result_type_name = fields.Char(
        string='Result Type Name',
        related='result_type.name')

    fake_field = fields.Text(
        string='Fake Field', help='This field is used to trigger onchange event')

    search_info = fields.Text(
        string='Search Info',
        help='This field is used to store search info')
    
    fields_as_category = fields.Boolean(
        string='Field As Category', 
        default=False)

    @api.depends('supported_result_types')
    def _compute_result_type_domain_ids(self):
        for record in self:
            if record.supported_result_types:
                record.result_type_domain_ids = record.supported_result_types.ids
            else:
                record.result_type_domain_ids = self._get_result_types()

    @api.depends('data_source_type_name', 'group_by_infos', 'raw_fields.group_by')
    def _compute_multi_group_by(self):
        """
        compute multi group by
        """
        for record in self:
            if record.data_source_type_name == 'model':
                record.multi_group_by = len(record.group_by_infos) > 1
            else:
                record.multi_group_by = len(record.raw_fields.filtered(lambda x: x.group_by)) > 1

    @api.depends('supported_data_source_types')
    def _compute_data_source_type_domain_ids(self):
        for record in self:
            if record.supported_data_source_types:
                record.data_source_type_domain_ids = record.supported_data_source_types.ids
            else:
                record.data_source_type_domain_ids = self._get_data_source_types()

    @tools.ormcache()
    
    def _get_data_source_types(self):
        """
        get data source type
        """
        return self.env['mana_dashboard.data_source_type'].search([]).ids

    @tools.ormcache()
    def _get_result_types(self):
        return self.env['mana_dashboard.result_type'].search([]).ids

    def export_data_source_mixin(self):
        """
        export data source mixin
        """
        self.ensure_one()

        return {
            'name': self.name,
            'data_source_type': self.data_source_type_name,
            'model': self.model_name,
            'model_fields': self.model_fields.export_field_infos(),
            'raw_fields': self.raw_fields.export_raw_field_infos(),
            'group_by_infos': self.group_by_infos.export_group_by_infos(),
            'order_by_infos': self.order_by_infos.export_order_by_infos(),
            'limit': self.limit,
            'method': self.method,
            'sql': self.sql,
            'res_id': self.res_id,
            'json_data_format': self.json_data_format,
            'json_data': self.json_data,
            'code': self.code,
            'result_type': self.result_type_name,
            'fake_field': self.fake_field,
            'supported_result_types': self.supported_result_types.mapped('name'),
            'supported_result_types': self.supported_result_types.mapped('name'),
            # drill
            'drill_field': self.drill_field.name,
            'drill_domain_type': self.drill_domain_type,
            'drill_domain': self.drill_domain,
            'drill_operator': self.drill_operator,
            'drill_extra_domain': self.drill_extra_domain,
            # link to
            'link_to_config': self.link_to_config.config_name,
            'link_action_field': self.link_action_field.name,
            'link_action_operator': self.link_action_operator,
            'link_action_domain': self.link_action_domain
        }

    def import_data_source_mixin(self, info):
        """
        import data source mixin
        """
        vals = {}

        data_source_type = self.env['mana_dashboard.data_source_type'].search([('name', '=', info['data_source_type'])])
        vals['data_source_type'] = data_source_type.id

        result_type = self.env['mana_dashboard.result_type'].search([('name', '=', info['result_type'])])
        vals['result_type'] = result_type.id

        supported_result_types = self.env['mana_dashboard.result_type'].search([('name', 'in', info['supported_result_types'])])
        if supported_result_types:
            vals['supported_result_types'] = [(6, 0, supported_result_types.ids)]

        # model
        model_name = info.get('model')
        if model_name:
            model = self.env['ir.model'].search([('model', '=', model_name)])
            if not model:
                raise exceptions.ValidationError(_('Model %s not found') % model_name)
            vals['model'] = model.id

        # model fields infos
        model_field_infos = info.get('model_fields', [])
        if model_field_infos:
            model_fields = self.env['mana_dashboard.field_info'].import_field_infos(model_field_infos)
            vals['model_fields'] = [(6, 0, model_fields.ids)]

        # raw fields infos
        raw_field_infos = info.get('raw_fields', [])
        if raw_field_infos:
            raw_fields = self.env['mana_dashboard.raw_field_info'].import_raw_field_infos(raw_field_infos)
            vals['raw_fields'] = [(6, 0, raw_fields.ids)]

        # group by infos
        group_by_infos = info.get('group_by_infos', [])
        if group_by_infos:
            group_by_infos = self.env['mana_dashboard.group_by_info'].import_group_by_infos(group_by_infos)
            vals['group_by_infos'] = [(6, 0, group_by_infos.ids)]

        # order by infos
        order_by_infos = info.get('order_by_infos', [])
        if order_by_infos:
            order_by_fields = self.env['mana_dashboard.order_by_info'].import_order_by_infos(order_by_infos)
            vals['order_by_infos'] = [(6, 0, order_by_fields.ids)]
        
        # drill
        if vals.get('model'):
            drill_field_name = info.get('drill_field')
            if drill_field_name:
                drill_field = self.env['ir.model.fields'].search([('model_id', '=', vals['model']), ('name', '=', drill_field_name)])
                if not drill_field:
                    raise exceptions.ValidationError(_('Drill Field %s not found') % drill_field_name)
                vals['drill_field'] = drill_field.id

        # search group by

        vals.update({
            'name': info.get('name'),
            'limit': info.get('limit'),
            'method': info.get('method'),
            'sql': info.get('sql'),
            'res_id': info.get('res_id'),
            'json_data_format': info.get('json_data_format'),
            'json_data': info.get('json_data'),
            'code': info.get('code'),
            'fake_field': info.get('fake_field'),
        })

        record = self.create(vals)
        return record
