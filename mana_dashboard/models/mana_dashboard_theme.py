
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ManaDashboardTheme(models.Model):
    '''
    Model Project
    '''
    _name = 'mana_dashboard.theme'
    _description = 'theme for dashboard'

    name = fields.Char(string='name')

    axis_label_show = fields.Char(string='axis label show')
    splitLineShow = fields.Boolean(string='split line show')
    split_line_color = fields.Char(string='split line color')
    split_area_color = fields.Char(string='split area color')

    legend_text_color = fields.Char(string='legend text color')

    time_line_item_color = fields.Char(string='time line item color')
    timeline_check_color = fields.Char(string='timeline check color')
    timeline_control_color = fields.Char(string='timeline control color')
    timeline_control_border_color = fields.Char(string='timeline control border color')
    timeline_label_color = fields.Char(string='timeline label color')

    symbol_border_width = fields.Integer(string='symbol_border_width')
    symbol = fields.Selection(
        string='symbol', 
        selection=[
        ("emptyArrow", "emptyArrow"), 
        ("arrow", "arrow"), 
        ("emptyPin", "emptyPin"), 
        ("symbolPin", "symbolPin"), 
        ("emptyDiamond", "emptyDiamond"), 
        ("diamond", "diamond"), 
        ("emptyTriangle", "emptyTriangle"), 
        ("triangle", "triangle"), 
        ("emptyRoundRect", "emptyRoundRect"), 
        ("roundRect", "roundRect"), 
        ("emptyRect", "emptyRect"), 
        ("rect", "rect"), 
        ("emptyCircle", "emptyCircle"), 
        ("circle", "circle")])
    
    symbol_size = fields.Integer(string='symbolSize')
    k_border_color_0 = fields.Char(string='k border color 0')
    axis_label_color = fields.Char(string='axis_label_color')
    timeline_line_width = fields.Integer(string='timeline_line_width')
    title_color = fields.Char(string='title_color')
    visual_mapping_colors = fields.One2many(
        string='visual mapping colors', 
        comodel_name='mana_dashboard.theme_color', inverse_name='theme_id')
    axis_line_color = fields.Char(string='axis_line_color')
    
    background = fields.Char(string='background')
    toolbox_color = fields.Char(string='toolbox color')
    tooltip_axis_color = fields.Char(string='tooltipAxisColor')
    toolltip_axis_width = fields.Integer(string='toolltip_axis_width')
    timeline_item_color_emp = fields.Char(string='timeline_item_color_emp')
    timeline_item_border_width = fields.Integer(string='time_line_item_border_width')
    timeline_control_border_width = fields.Integer(string='timeline_control_border_width')
    line_smooth = fields.Boolean(string='line_smooth')
    k_color_0 = fields.Char(string='k_color_0')
    graph_line_color = fields.Integer(string='graph_line_width')
    sub_title_color = fields.Char(string='sub title color')
    border_width = fields.Integer(string='border_width')

    border_color = fields.Char(string='border_color')
    theme_colors = fields.One2many(
        string='theme_colors', 
        comodel_name='mana_dashboard.theme_color', 
        inverse_name='theme_id')
    
    axis_seperate_setting = fields.Boolean(string='axis seperate setting')
    axis_line_show = fields.Boolean(string='axis_line_show')
    axis_tick_color = fields.Char(string='axis_tick_color')
    label_color = fields.Char(string='label_color')
    axis_tick_show = fields.Boolean(string='axis tick show')
    split_area_show = fields.Boolean(string='split_area_show')
    toolbox_emphasis_color = fields.Char(string='toolboxEmphasisColor')
    
    timeline_check_boarder_color = fields.Char(string='timeline_check_boarder_color')
    timeline_line_color = fields.Char(string='timeline_line_color')
    line_width = fields.Integer(string='line_width')
    
    k_color = fields.Char(string='k_color')
    k_border_color = fields.Char(string='k_border_color')
    k_border_width = fields.Integer(string='k_border_width')
