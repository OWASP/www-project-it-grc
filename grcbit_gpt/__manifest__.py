# -*- coding: utf-8 -*-

{
    'name': "GRCBIT GPT",
    'summary': "grc4ciso: GRC + XDR + ZT + GPT",
    'description': "grc4ciso integrates GRC, XDR, Zero Trust and GPT cybersecurity capabilities into a unified Software-as-a-Service (SaaS) platform",
    'author':"grc4ciso",
    'website': "https://grc4ciso.com/",
    'category': 'grc4ciso',
    'version': '16.0',
    'depends': ['base', 'base_setup', 'mail', 'im_livechat'],
    'external_dependencies': {'python': ['openai']},

    'data': [
        #'security/ir.model.access.csv',
        'data/mail_channel_data.xml',
        'data/user_partner_data.xml',
        'views/res_config_settings_views.xml',
        'views/mail_channel_chatgpt.xml',
        'views/views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'grcbit_gpt/static/src/components/*/*.js',
            'grcbit_gpt/static/src/components/*/*.xml',
            'grcbit_gpt/static/src/components/*/*.scss',
        ],
        'im_livechat.assets_public_livechat': [
            'grcbit_gpt/static/src/public_models/*.js',
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
