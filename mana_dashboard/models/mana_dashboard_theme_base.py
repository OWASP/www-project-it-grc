
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ManaDashboardTheme(models.Model):
    '''
    Mana Dashboard Theme Base
    '''
    _name = 'mana_dashboard.theme_base'
    _description = 'theme for dashboard'

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

    symbol_border_width = fields.Integer(string='symbol border width')
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
    axis_label_color = fields.Char(string='axis label color')
    timeline_line_width = fields.Integer(string='timeline line width')
    title_color = fields.Char(string='title color')
    visual_mapping_colors = fields.One2many(
        string='visual mapping colors', 
        comodel_name='mana_dashboard.theme_color', 
        inverse_name='theme_id')
    axis_line_color = fields.Char(string='axis line color')
    
    background = fields.Char(string='background')
    toolbox_color = fields.Char(string='toolbox color')
    tooltip_axis_color = fields.Char(string='tooltipAxisColor')
    toolltip_axis_width = fields.Integer(string='toolltip axis width')
    timeline_item_color_emp = fields.Char(string='timeline item color emp')
    timeline_item_border_width = fields.Integer(string='time line item border width')
    timeline_control_border_width = fields.Integer(string='timeline control border width')
    line_smooth = fields.Boolean(string='line smooth')
    k_color_0 = fields.Char(string='k color 0')
    graph_line_color = fields.Integer(string='graph line color')
    sub_title_color = fields.Char(string='sub title color')
    border_width = fields.Integer(string='border width')

    border_color = fields.Char(string='border color')
    theme_colors = fields.One2many(
        string='theme_colors', 
        comodel_name='mana_dashboard.theme_color', 
        inverse_name='theme_id')
    
    axis_seperate_setting = fields.Boolean(string='axis seperate setting')
    axis_line_show = fields.Boolean(string='axis line show')
    axis_tick_color = fields.Char(string='axis tick color')
    label_color = fields.Char(string='label color')
    axis_tick_show = fields.Boolean(string='axis tick show')
    split_area_show = fields.Boolean(string='split area show')
    toolbox_emphasis_color = fields.Char(string='toolboxEmphasisColor')
    
    timeline_check_boarder_color = fields.Char(string='timeline check boarder color')
    timeline_line_color = fields.Char(string='timeline line color')
    line_width = fields.Integer(string='line width')
    
    k_color = fields.Char(string='k color')
    k_border_color = fields.Char(string='k border color')
    k_border_width = fields.Integer(string='k border width')
