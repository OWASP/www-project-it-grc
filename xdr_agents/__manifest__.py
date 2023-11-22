# -*- coding: utf-8 -*-
{
    'name': "XDR Agents",
    'summary': "App for XDR Agents implementation",
    'description': "XDR Agents",
    'author':"HackDoo",
    'website': "https://hackdoo.com/",
    'category': 'Uncategorized',
    'version': '16.0',
    'depends': [
        'base',
        'backend_iframe',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/agents_views.xml',
        'views/mitre_views.xml',
        'views/menuitems.xml',
        'views/action_server.xml',
    ],
    # 'assets':{
    #     'web.assets_backend':[
        
    #     ]
    # }
}
