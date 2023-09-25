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

    ],
}