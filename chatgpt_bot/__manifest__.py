# -*- coding: utf-8 -*-
{
    'name': "OdooBot ChatGPT AI integration",

    'summary': """
    This module integrates the response from ChatGPT into Odoo's built-in chatbot, OdooBot.
        """,

    'description': """
        This module allows users to leverage the advanced natural language processing capabilities 
        of ChatGPT within Odoo's user-friendly interface. By integrating ChatGPT's responses into OdooBot,
        users can easily access the powerful language model's insights and capabilities without having to 
        navigate away from the Odoo platform. This integration can be used to enhance the functionality of 
        OdooBot, providing more accurate and detailed responses to user queries and improving overall user experience.
    """,

    'author': "FL1 sro",
    'website': "https://fl1.cz",
    "images": ["static/description/banner.png", "static/description/gif_chat.gif"],
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Productivity',
    'version': '15.0.0.4',
    'license': 'AGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'queue_job'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_config_settings.xml',
    
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "external_dependencies": {
        "python" : ['openai', 'markdown']
        },
    'price': 0.00,
    'currency': 'EUR',

}
