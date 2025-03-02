# -*- coding: utf-8 -*-
{
    'name': "GRCBIT BASE",
    'summary': "grc4ciso: GRC + XDR + ZT + GPT",
    'description': "grc4ciso integrates GRC, XDR, Zero Trust and GPT cybersecurity capabilities into a unified Software-as-a-Service (SaaS) platform",
    'author':"grc4ciso",
    'website': "https://grc4ciso.com/",
    'category': 'grc4ciso',
    'version': '16.0',
    'depends': [
        'base',
        'board',
        'mail',
        'grcbit_setgroups',
    ],

    # always loaded
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/asset_management_views.xml',
        'views/dashboard_view.xml',
        'views/menuitems.xml',
        'views/settings_views.xml',
        #'reports/report_data_asset.xml',
        #'reports/report_it_inventory.xml',
        'wizards/set_groups_views.xml',
    ],
    'assets':{
        'web.assets_backend':[
            'grcbit_base/static/src/js/user_menu_items.js',
            #'grcbit_base/static/src/js/dashboard.js',
            'grcbit_base/static/src/js/many2many_tags.js',
            #'grcbit_base/static/src/xml/dashboard.xml',
        ]
    },
    'installable': True,
    'application': True,
}
