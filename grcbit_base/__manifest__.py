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
    ],

    # always loaded
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/asset_management_views.xml',
        'views/res_users_view.xml',
        'views/dashboard_view.xml',
        'views/menuitems.xml',
        'reports/report_data_asset.xml',
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
    }
}
