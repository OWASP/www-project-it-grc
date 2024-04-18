# -*- coding: utf-8 -*-
{
    'name': "GRCBIT POLICY",
    'summary': "App for grcbit policy implementation",
    'description': "POLICYS",
    'author':"HackDoo",
    'website': "https://hackdoo.com/",
    'category': 'Uncategorized',
    'version': '16.0',
    'depends': [
        'grcbit_risk_management',
        'document_page_approval',
        'document_page',
    ],

    # always loaded
    'data': [
        #reports
        'reports/document_page_report.xml',
        
        #views
        'views/document_page_views.xml',
        'views/menuitems.xml',

        #wizard
        'wizard/set_groups_view.xml',

    ],
 
}
