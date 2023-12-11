# -*- coding: utf-8 -*-
{
    'name': "mana_dashboard_cards",

    'summary': """
        cards for mana dashboard, which is a free advanced dashboard for odoo
    """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Funenc, co.,ltd.",
    'website': "https://www.openerpnext.com",
    'live_test_url': 'https://www.openerpnext.com',
    'license': 'OPL-1',
    'currency': 'EUR',
    'price': 88,

    'category': 'Apps/dashboards',
    'depends': ['base', 'web', 'mana_dashboard'],

    'images': ['static/description/banner.png'],

    # always loaded
    'data': [
        'data/card_style1.xml',
        'data/card_style2.xml',
        'data/card_style3.xml',
        'data/card_style4.xml',
    ],
}
