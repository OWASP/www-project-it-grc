# -*- coding: utf-8 -*-

{
    'name': "grcbit_gpt",
    'summary': "GPT Assistant",

    'description': """
        GPT Assistant
    """,

    'author': "GRCbit",
    'category': 'Website',
    'version': '0.1',

    'depends': ['base', 'base_setup', 'mail', 'im_livechat'],
    'external_dependencies': {'python': ['openai']},

    'license': 'LGPL-3',
    'maintainer': 'GRCbit',

    'data': [
        'security/ir.model.access.csv',
        'data/mail_channel_data.xml',
        'data/user_partner_data.xml',
        'views/res_config_settings_views.xml',
        'views/mail_channel_chatgpt.xml',
        'views/views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'chatgpt_assistant_discuss_integration/static/src/components/*/*.js',
            'chatgpt_assistant_discuss_integration/static/src/components/*/*.xml',
            'chatgpt_assistant_discuss_integration/static/src/components/*/*.scss',
        ],
        'im_livechat.assets_public_livechat': [
            'chatgpt_assistant_discuss_integration/static/src/public_models/*.js',
        ],
    },
    'images': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 0,
    'currency': 'EUR',
}
