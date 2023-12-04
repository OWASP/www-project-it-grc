# -*- coding: utf-8 -*-
{
    'name': "GRCBIT SoD",
    'summary': "App for grcbit SoD implementation",
    'description': "SoD",
    'author':"HackDoo",
    'website': "https://hackdoo.com/",
    'category': 'Uncategorized',
    'version': '16.0',
    'depends': [
        'grcbit_base',
        'grcbit_iso27001',
        'grcbit_risk_management',
        'grcbit_compliance',
    ],

    # always loaded
    'data': [
        #security
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        #views
        'views/sod_views.xml',
        'views/menuitems.xml',
    ],
    
}
