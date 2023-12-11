# -*- coding: utf-8 -*-
{
    'name': "anita_form_callback",

    'summary': """
        extend to support callback for form
    """,

    'description': """
        extend to support callback for form
    """,

    'author': "funec Co., Ltd.",
    'website': "https://www.openerpnext.com",
    'live_test_url': 'https://www.openerpnext.com',

    'category': 'Apps/Tools',
    'version': '16.0.0.2',
    'price': 0,

    'license': 'OPL-1',
    'images': ['static/description/banner.png'],

    'depends': ['base'],

    "application": False,
    "installable": True,
    "auto_install": False,

    'depends': ['base', 'web'],

    'data': [],

    'assets': {
        'web.assets_backend': [
            'anita_form_callback/static/src/action_service.js',
            'anita_form_callback/static/js/anita_form_extend.js',
        ],
        
        'web.assets_qweb': []
    }
}
