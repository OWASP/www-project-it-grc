# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval, datetime, time, wrap_module, test_python_expr
import json, json5
import logging
import xw_utils

_logger = logging.getLogger(__name__)


class ManaDashboard(models.Model):
    '''
    Mana Dashboard
    '''
    _name = "mana_dashboard.dashboard"
    _description = "Mana Dashboard"
    _order = "id desc"

    # files
    style_files = fields.Many2many(
        'ir.attachment', 
        string='Style Files', 
        relation='mana_dashboard_style_files_rel')   

    js_files = fields.Many2many(
        'ir.attachment', 
        string='Js Files',
        relation='mana_dashboard_js_files_rel')

    image_files = fields.Many2many(
        'ir.attachment', 
        string='Image Files',
        relation='mana_dashboard_image_files_rel')

    # name must be unique
    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Dashboard name already exists !"),
    ]

    @api.model
    def create(self, vals):
        '''
        create the akl dashboard
        :param vals:
        :return:
        '''
        res = super(ManaDashboard, self).create(vals)
        xw_utils.update_dashboard(res)
        return res

    def unlink(self):
        '''
        unlink the dashboard
        :return:
        '''
        for rec in self:
            # search menu which bind to this dashboard
            records = self.env['ir.ui.menu'].sudo().search([
                ('action', '=', "ir.actions.client," + str(rec.action_id.id))
            ])
            records.sudo().unlink()
            rec.action_id.sudo().unlink()

        return super(ManaDashboard, self).unlink()

    def load_dashboard(self):
        """
        load dashboard 
        """
        self.ensure_one()
        result = self.read()[0]
        if result.get('style_urls', False):
            result['style_urls'] = json5.loads(result['style_urls'])
        if result.get('js_urls', False):
            result['js_urls'] = json5.loads(result['js_urls'])
        # search infos
        try:
            result['search_infos'] = self.env['mana_dashboard.search_info'].get_search_infos(self.id)
        except Exception as e:
            _logger.error(e)
        # get system variables
        result['system_variables'] = self.get_system_variables()
        return result
    
    def _get_eval_context(self):
        """
        Get the context used when evaluating python code
        """
        context = {
            'env': self.env,
            'self': self,
            'datetime': datetime,
            'context_today': datetime.datetime.now,
            'user': self.env.user.sudo(),
            'time': time,
            'res_company': self.env.company.sudo(),
            'json5': wrap_module(__import__('json5'), ['loads', 'dumps']),
            'pendulum': wrap_module(__import__('pendulum'), ['today', 'now', 'parse', 'from_timestamp']),
        }
        return context
    
    def get_system_variables(self):
        """
        get system variables
        """
        self.ensure_one()
        eval_context = self._get_eval_context()
        system_variable = self.system_variables
        system_variable = safe_eval(system_variable.strip(), eval_context, mode="eval", nocopy=True)
        return system_variable
    
    def reset_search_infos(self):
        '''
        reset search infos
        :return:
        '''
        self.ensure_one()
        self.env['mana_dashboard.search_info'].reset_search_infos(self.id)
        return True

    def _get_dashboard_action(self, mode):
        """
        get dashboard action
        """
        self.ensure_one()
        return {
            'name': 'Dashboard_' + self.name,
            "type": "ir.actions.client",
            "params": {
                "dashboard_id": self.id,
                "mode": mode
            },
            "tag": "mana_dashboard"
        }

    def edit_dashboard(self):
        '''
        edit dashboard
        :return:
        '''
        return self._get_dashboard_action('edit')

    def view_dashboard(self):
        '''
        view dashboard
        :return:
        '''
        return self._get_dashboard_action('view')

    def view_dashboard_full_screen(self):
        '''
        view dashboard full screen
        :return:
        '''
        action = self._get_dashboard_action('view')
        action['target'] = 'fullscreen'
        return action

    @api.model
    def get_model_field_statistics(self, model_id, field_id, statistics):
        """
        """
        ir_model = self.env['ir.model'].browse(int(model_id))
        field = self.env['ir.model.fields'].browse(int(field_id))
        if not ir_model or not field:
            return []
        domain = []
        
        if self.start_time:
            domain.append((field.name, '>=', self.start_time))
        if self.end_time:
            domain.append((field.name, '<=', self.end_time))

        # check the field type
        if statistics != 'count' and field.ttype not in ['integer', 'float']:
            raise UserError("Hi, Body, The field type is not integer or float!!!")

        model = self.env[ir_model.model].sudo()
        if statistics == 'count':
            return model.search_count(domain)
        elif statistics == 'sum':
            # check the field type
            if field.ttype not in ['integer', 'float']:
                raise UserError("Hi, Body, The field type is not integer or float!!!")
            records = model.search_read(domain, [field.name])
            return sum([record[field.name] for record in records])
        elif statistics == 'avg':
            records = model.search_read(domain, [field.name])
            if len(records) == 0:
                return []
            return sum([record[field.name] for record in records]) / len(records)
        elif statistics == 'min':
            records = model.search_read(domain, [field.name])
            return min([record[field.name] for record in records])  
        elif statistics == 'max':
            records = model.search_read(domain, [field.name])
            return max([record[field.name] for record in records])
        else:
            return []

    def update_search_infos(self, search_infos):
        """
        update search info
        """
        self.ensure_one()
        self.env['mana_dashboard.search_info'].update_search_infos(self.id, search_infos)

    def bind_menu_wizard(self):
        """
        bind to menu
        """
        if not self.action_id:
            val = {
                'name': 'Dashboard_' + self.name,
                'res_model': 'mana.dashboard',
                'params': {
                    'dashboard_id': self.id,
                    'mode': 'view',
                },
                'tag': 'mana_dashboard',
            }
            action_id = self.env['ir.actions.client'].sudo().create(val)
            self.action_id = action_id

        return {
            "type": "ir.actions.act_window",
            "res_model": "mana_dashboard.bind_menu_wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_action_id": self.action_id.id,
            }
        }

    @api.depends()
    def _compute_binded_menu_ids(self):
        """
        compute binded menu ids
        """
        for rec in self:
            rec.binded_menu_ids = self.env['ir.ui.menu'].sudo().search([
                ('action', '=', "ir.actions.client," + str(rec.action_id.id))
            ])
            rec.binded_menu_count = len(rec.binded_menu_ids)

    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals_list):
        """
        update inited
        """
        records = super(ManaDashboard, self).create(vals_list)
        records.write({'inited': True})
        return records

    @api.onchange('template_id')
    def _onchange_template_id(self):
        """
        onchange template id
        """
        if self.template_id:
            self.style_files = self.template_id.style_files
            self.js_files = self.template_id.js_files
            self.image_files = self.template_id.image_files
            self.dashboard_html = self.template_id.template
        else:
            self.style_files = False
            self.js_files = False
            self.image_files = False
            self.dashboard_html = False

    @api.depends('style_files')
    def _compute_style_urls(self):
        """
        compute cavas urls
        """
        for rec in self:
            urls = []
            for style_file in rec.style_files:
                urls.append(style_file.url)
            rec.style_urls = urls or False

    @api.depends('js_files')
    def _compute_js_urls(self):
        """
        compute js urls
        """
        for rec in self:
            urls = []
            for js_file in rec.js_files:
                urls.append(js_file.url)
            rec.js_urls = urls or False

    @api.onchange('use_template')
    def _onchange_use_template(self):
        """
        onchange use template
        """
        if not self.use_template:
            self.template_id = False

    def export_dashboard(self):
        """
        export dashboard, use xml to describe the dashboard, and zip the files
        """
        dashboard_data = xw_utils.export_dashboard(self)
        return dashboard_data

    def import_dashboard(self, dashboard_data):
        """
        import dashboard
        """
        dashboard = xw_utils.import_dashboard(self, dashboard_data)
        return dashboard

    def jump_to_export_url(self):
        """
        jump to export dashboard
        """
        return {
            "type": "ir.actions.act_url",
            "url": "/mana_dashboard/export_dashboard/" + str(self.id),
            "target": "new",
        }

    @api.model
    def remove_configs(self, config_infos):
        """
        remove configs
        """
        for model_name in config_infos:
            ids = config_infos[model_name]
            self.env[model_name].sudo().browse(ids).unlink()

    def write(self, vals):
        """
        override write method
        """
        # if 'dashboard_html' in vals:
        #     config_ids = re.findall(r'config_id="(\d+)"', vals['dashboard_html'])
        #     if config_ids:
        #         old_config_ids = self.config_ids.ids
        #         new_config_ids = [int(config_id) for config_id in config_ids]
        #         remove_config_ids = list(set(old_config_ids) - set(new_config_ids))
        #         if remove_config_ids:
        #             self.env['mana_dashboard.any_config'].sudo().browse(remove_config_ids).unlink()

        return super(ManaDashboard, self).write(vals)
    
    @api.model
    def test_button(self):
        """
        test button
        """
        return {
            "type": "ir.actions.act_url",
            "url": "https://www.openerpnext.com/",
            "target": "new",
        }
    
    def save_theme_info(self, theme_info):
        """
        save theme data
        """
        self.ensure_one()
        self.theme_info = theme_info

    @api.model
    def _add_inherited_fields(self):
        """ Determine inherited fields. """

        # add inherited fields
        super()._add_inherited_fields()

        # check fields
        xw_utils.ensure_dashboard_fields(self, fields)
