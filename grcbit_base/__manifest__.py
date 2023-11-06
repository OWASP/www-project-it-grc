# -*- coding: utf-8 -*-
{
    'name': "GRCBIT Base",
    'summary': "App for grcbit base implementation",
    'description': "Dashboard, Asset Managment",
    'author':"HackDoo",
    'website': "https://hackdoo.com/",
    'category': 'Uncategorized',
    'version': '16.0',
    'depends': [
        'web',
        'base',
        'board',
        'document_page'
    ],

    # always loaded
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/asset_management_views.xml',
        'views/dashboard_view.xml',
        'views/menuitems.xml',
        'views/config_views.xml',

    ],
    'assets':{
        # 'web.assets':[
        #     'grcbit_base/static/src/js/**.js',
        #     'grcbit_base/static/src/xml/**.xml',
        # ],
        'web.assets_backend':[
            'grcbit_base/static/src/js/user_menu_items.js',
        ]
    }
}
