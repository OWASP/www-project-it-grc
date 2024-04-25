# -*- coding: utf-8 -*-

{
    'name': 'ChatGPT HackDoo',
    'version': '16.0.1.1.2',
    'license': 'AGPL-3',
    'summary': 'ChatGPT HackDoo',
    'description': '''
        Allows the application to leverage the capabilities of the GPT language model to generate human-like responses, providing a more natural and intuitive user experience.
        You can configurate a assistant ID to link own app communication
        ''',
    'author': 'HackDoo',
    'company': 'HackDoo',
    'website': 'https://hackdoo.com',
    'depends': ['base', 'base_setup', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/chatgpt_model_data.xml',
        'data/mail_channel_data.xml',
        'data/user_partner_data.xml',
        'views/res_config_settings_views.xml',
    ],
    'external_dependencies': {'python': ['openai']},
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
