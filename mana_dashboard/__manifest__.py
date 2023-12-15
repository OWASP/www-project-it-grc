# -*- coding: utf-8 -*-
{
    "name":
        "mana_dashboard",
    "summary":
        """
        Mana dashboard for odoo, advance dashboard for odoo, Bi builder for odoo. to get the full version, please contact us: https://www.openerpnext.com
    """,
    "description":
        """
        mana dashboard for odoo,
        dashboard
        super dashboard
        advance dashboard
        advance dashboard for odoo
        dashboard for odoo
        odoo dashboard
        bi
        big data
        big data dashboard
        big data dashboard for odoo
        admin dashboard
        form builder
        reporter
        excel builder
        awesome odoo
        anita odoo
        editor
    """,
    "author":
        "Funenc Co., Ltd.",
    "website":
        "https://www.openerpnext.com",
    "live_test_url":
        "http://124.223.107.118:6010/web",
    "category":
        "application/dashboard",
    "version":
        "16.0.4.0",
    "price":
        0,
    "currency":
        "EUR",
    "license":
        "OPL-1",
    "depends": [
        'base',
        'anita_form_callback',
        'mana_dashboard_base',
        'grcbit_base',
    ],
    "external_dependencies": {
        "python": ['json5', 'pendulum', 'python-box', 'xw_utils>=1.0.15']
    },
    "images": ['static/description/banner.png'],
    "data": [
        'security/security.xml',
        'security/ir.model.access.csv',

        # data
        'data/mana_series_type.xml',
        'data/mana_action_block_category.xml',
        'data/mana_aggregation_type.xml',
        'data/mana_field_datetime_range.xml',
        'data/mana_line_chart_template.xml',
        'data/mana_list_template.xml',
        'data/mana_pie_chart_template.xml',
        'data/bar_chart/bar_chart_template.xml',
        'data/mana_scatter_chart_template.xml',
        'data/mana_candlestick_chart_template.xml',
        'data/mana_radar_chart_template.xml',
        'data/mana_gauge_chart_template.xml',
        'data/mana_config_sequence.xml',
        'data/mana_timer_sequence.xml',
        'data/nama_search_group_sequence.xml',
        'data/mana_data_table.xml',

        'data/mana_custom_chart_template.xml',
        'data/mana_none_template.xml',
        'data/mana_empty_card.xml',

        # card style
        'data/statistics_card/card_style1.xml',

        # views
        'views/mana_dashboard.xml',
        'views/mana_group_by_info.xml',
        'views/mana_aggregation_type.xml',
        'views/mana_template.xml',
        'views/mana_send_to_dashboard.xml',
        'views/mana_action_blocks.xml',
        'views/mana_dashboard_template.xml',
        'views/mana_template.xml',
        'views/mana_history_data.xml',
        'views/mana_order_by_info.xml',
        'views/mana_template_base.xml',
        'views/mana_field_info.xml',
        'views/mana_raw_field_info.xml',
        'views/mana_config.xml',
        'views/mana_content_editor.xml',
        'views/mana_datetime_range.xml',
        'views/mana_range_filter_traits.xml',
        'views/mana_search_info.xml',
        'views/mana_bind_menu_wizard.xml',
        'views/mana_data_source.xml',
        'views/mana_marquee_traits.xml',
        'views/mana_dashboard_import_wizard.xml',
        'views/mana_any_config.xml',
        'views/mana_timer_config.xml',
        'views/mana_search_group_traits.xml',
        'views/mana_dashboard_parameter.xml',
        'views/mana_dashboard_series_type.xml',
        'views/mana_dashboard_template.xml',
        'views/mana_dashboard_block_settings.xml',

        #wizard
        # 'wizard/set_groups_views.xml',
    ],

    'assets': {
        'web.assets_backend': [

            # css
            "/web/static/lib/daterangepicker/daterangepicker.css",
            "/mana_dashboard/static/css/mana_dashboard.scss",
            "/mana_dashboard/static/css/editor.min.css",
            "/mana_dashboard/static/css/card_style.scss",
            "/mana_dashboard/static/css/layout.scss",
            "/mana_dashboard/static/css/search.scss",

            # libs
            "/mana_dashboard/static/libs/editor/editor.min.js",
            "/mana_dashboard/static/libs/echarts/echarts.min.js",
            "/mana_dashboard/static/libs/tabulator/css/tabulator.min.css",
            "/mana_dashboard/static/libs/tabulator/css/tabulator_bootstrap4.css",

            # Mana2ManyOne
            "/mana_dashboard/static/js/mana_many2one.js",
            "/mana_dashboard/static/js/preview_widget/preview_widget.js",

            # tabulator
            "/mana_dashboard/static/libs/tabulator/js/tabulator.min.js",
            "/mana_dashboard/static/libs/bootstrap_blocks/blocks.min.js",
            "/mana_dashboard/static/libs/style_bg/style-bg.min.js",

            # custom config base
            "/mana_dashboard/static/js/mana_block_base.js",

            # block regsitry
            "/mana_dashboard/static/js/mana_block_registry.js",

            # block icon
            "/mana_dashboard/static/js/util/mana_icons.js",
            "/mana_dashboard/static/js/util/mana_field_template.js",

            # dialog patch
            "/mana_dashboard/static/src/mana_dialog_patch.js",

            # dashboard
            "/mana_dashboard/static/src/color_picker/color_picker.js",
            "/mana_dashboard/static/src/color_picker/color_picker.scss",
            "/mana_dashboard/static/src/color_picker/color_picker.xml",

            # color picker list
            "/mana_dashboard/static/src/color_picker_list/color_picker_list.js",
            "/mana_dashboard/static/src/color_picker_list/color_picker_list.xml",

            # according
            "/mana_dashboard/static/src/mana_accordion/mana_accordion.js",
            "/mana_dashboard/static/src/mana_accordion/mana_accordion.xml",
            "/mana_dashboard/static/src/mana_accordion/mana_accordion.scss",

            # config number
            "/mana_dashboard/static/src/mana_config_number/mana_config_number.js",
            "/mana_dashboard/static/src/mana_config_number/mana_config_number.xml",

            # config color
            "/mana_dashboard/static/src/mana_config_color/mana_config_color.js",
            "/mana_dashboard/static/src/mana_config_color/mana_config_color.xml",

            # color list config
            "/mana_dashboard/static/src/mana_config_color_list/mana_config_color_list.js",
            "/mana_dashboard/static/src/mana_config_color_list/mana_config_color_list.xml",

            # theme builder css
            "/mana_dashboard/static/src/theme_builder/css/_configs.color.scss",
            "/mana_dashboard/static/src/theme_builder/css/_settings.global.scss",
            "/mana_dashboard/static/src/theme_builder/css/_components.echarts.scss",
            "/mana_dashboard/static/src/theme_builder/css/_components.config.scss",
            "/mana_dashboard/static/src/theme_builder/css/_components.color.scss",
            "/mana_dashboard/static/src/theme_builder/css/_components.code.scss",

            # theme builder
            "/mana_dashboard/static/src/theme_builder/theme_builder.js",
            "/mana_dashboard/static/src/theme_builder/theme_builder.xml",
            "/mana_dashboard/static/src/theme_builder/chart_options.js",

            # color picker list
            "/mana_dashboard/static/src/color_picker_list/color_picker_list.js",
            "/mana_dashboard/static/src/color_picker_list/color_picker_list.xml",

            # mana config form
            "/mana_dashboard/static/js/chart_config_form/chart_config_form.js",

            # json editor
            "/mana_dashboard/static/js/json_editor/json_editor.js",

            # script editor
            "/mana_dashboard/static/libs/script_editor/script_editor.js",

            # preset
            "/mana_dashboard/static/js/editor_preset/editor_preset.js",

            # spectrum
            "/mana_dashboard/static/libs/spectrum/spectrum.js",
            "/mana_dashboard/static/libs/spectrum/spectrum.css",

            # charts
            "/mana_dashboard/static/js/charts/mana_chart_util.js",
            "/mana_dashboard/static/js/charts/mana_chart_builder.js",
            "/mana_dashboard/static/js/charts/mana_pie_chart.js",
            "/mana_dashboard/static/js/charts/mana_bar_chart.js",
            "/mana_dashboard/static/js/charts/mana_line_chart.js",
            "/mana_dashboard/static/js/charts/mana_scatter_chart.js",

            # data source
            "/mana_dashboard/static/js/data_source/mana_data_source.js",
            "/mana_dashboard/static/js/data_source/mana_record.js",
            "/mana_dashboard/static/js/data_source/mana_config.js",

            # basic blocks
            "/mana_dashboard/static/js/basic_blocks/mana_basic_blocks.js",

            # action widget
            "/mana_dashboard/static/js/action_widget/mana_action_block.js",
            "/mana_dashboard/static/js/action_widget/mana_action_widget.js",

            # svg block
            "/mana_dashboard/static/js/svg_block/svg_block.js",

            # date filter
            "/mana_dashboard/static/js/util/mana_date_util.js",

            # resize
            "/mana_dashboard/static/libs/ResizeObserver/ResizeObserver.js",
            "/mana_dashboard/static/js/resize_manager/resize_manager.js",

            # dialog
            "/mana_dashboard/static/js/dialog/mana_domain_selector.js",
            "/mana_dashboard/static/js/dialog/mana_dialog.js",

            # dashboard list
            "/mana_dashboard/static/js/mana_dashboard_list.js",

            # content
            "/mana_dashboard/static/js/content_block/content_block.js",

            # mana sub form view
            "/mana_dashboard/static/js/sub_form_view/mana_quick_create_form_view.js",
            "/mana_dashboard/static/js/sub_form_view/mana_sub_form_view.js",

            # theme builder widget
            "/mana_dashboard/static/js/theme_builder_widget.js",
            "/mana_dashboard/static/js/preview_theme_builder_widget.js",

            # chart traits
            "/mana_dashboard/static/js/form_trait/form_trait.js",

            # custom card
            "/mana_dashboard/static/js/empty_card/empty_card.js",

            # iframe
            "/mana_dashboard/static/js/iframe_widget/iframe_widget.js",

            # standlone
            "/mana_dashboard/static/js/standlone_field/mana_many2one_trait.js",
            "/mana_dashboard/static/js/standlone_field/mana_many2one_field.js",
            "/mana_dashboard/static/js/standlone_field/mana_many2many_field.js",
            "/mana_dashboard/static/js/standlone_field/mana_standlone_field.js",

            # qweb list
            "/mana_dashboard/static/js/qweb_block/qweb_block.js",

            # qweb template
            "/mana_dashboard/static/js/qweb_template/qweb_template.js",

            # data table
            "/mana_dashboard/static/js/data_table/data_table.js",

            # statistics_card
            "/mana_dashboard/static/js/statistics_card/statistics_card.js",

            # grid widget
            "/mana_dashboard/static/js/grid_widget/grid_widget.js",

            # mutex_toggle
            "/mana_dashboard/static/js/mutex_toggle.js",

            # search
            "/mana_dashboard/static/js/search/mana_search_group.js",
            "/mana_dashboard/static/js/search/mana_search_item.js",
            "/mana_dashboard/static/js/search/mana_search_time_range.js",

            # dashboard
            "/mana_dashboard/static/js/mana_dashboard.js",

            # search
            "/mana_dashboard/static/xml/misc.xml"
        ]
    }
}