# -*- coding: utf-8 -*-
{
    'name': "mana_dashboard_base",

    'summary': """
        Base module for mana_dashboard
     """,

    'description': """
        Base module for mana_dashboard
    """,

    'author': "Funenc Co., Ltd.",
    'website': "https://www.openerpnext.com",

    'category': 'Apps/Dashboard',
    'version': '16.0.0.7',
    'license': 'OPL-1',

    'depends': ['base', 'web'],
    'images': ['static/description/banner.png'],

    "external_dependencies": {
        'python': [
            'xw_utils>=1.0.13',
        ],
    },

    'data': [
        'security/ir.model.access.csv',
        
        'views/mana_template.xml',
        'views/mana_dashboard_template.xml',
        'views/mana_result_type.xml',
        'views/mana_data_source_type.xml',
        'views/mana_series_type.xml',
        'views/mana_web.xml',

        'data/mana_data_source_type.xml',
        'data/mana_result_type.xml'
    ],

    'assets': {
        'web.assets_backend': [
            "/mana_dashboard_base/static/src/template_component/template_component.xml",
        ]
    }
}
