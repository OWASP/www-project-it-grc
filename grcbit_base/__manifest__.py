# -*- coding: utf-8 -*-
{
    'name': "GRCBIT BASE",
    'summary': "grc4ciso: GRC + XDR + ZT + GPT",
    'description': "grc4ciso integrates GRC, XDR, Zero Trust and GPT cybersecurity capabilities into a unified Software-as-a-Service (SaaS) platform",
    'author':"grc4ciso",
    'website': "https://grc4ciso.com/",
    'category': 'grc4ciso',
    'version': '1.2',
    'depends': [
        #'web',
        'base',
        'board',
        'mail',
        'many2many_tags_click_cr',
        #'hide_login_ophackdoo',
        #'grcbit_compliance',
        #'grcbit_cvss',
        #'grcbit_iso27001',
        #'grcbit_pci4',
        #'grcbit_risk_management',
        #'grcbit_threat_scenario'
        'grcbit_setgroups',
        'grcbit_gpt',
        #'grcbit_cvss',
    ],

    # always loaded
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/asset_management_views.xml',
        'views/dashboard_view.xml',
        'views/menuitems.xml',
        'views/settings_views.xml',
        'reports/report_data_asset.xml',
        'reports/report_it_inventory.xml',
        'wizards/set_groups_views.xml',
        #'data/app_category.xml'
    ],
    'assets':{
        # 'web.assets':[
        #     'grcbit_base/static/src/js/**.js',
        #     'grcbit_base/static/src/xml/**.xml',
        # ],
        'web.assets_backend':[
            'grcbit_base/static/src/js/user_menu_items.js',
            'grcbit_base/static/src/js/dashboard.js',
            'grcbit_base/static/src/xml/dashboard.xml',
            'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.bundle.js',
            
        ]
    },
    'installable': True,
    'application': True,
}
