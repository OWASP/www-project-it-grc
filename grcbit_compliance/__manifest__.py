# -*- coding: utf-8 -*-
{
    'name': "GRCBIT COMPLIANCE",
    'summary': "App for grcbit compliance implementation",
    'description': "COMPLIANCE",
    'author':"HackDoo",
    'website': "https://hackdoo.com/",
    'category': 'Uncategorized',
    'version': '16.0',
    'depends': [
        'grcbit_base',
    ],

    # always loaded
    'data': [
        #security
        'security/ir.model.access.csv',

        #data
        'data/compliance.version.csv',
        'data/compliance.control.objective.csv',

        #views
        'views/compliance_views.xml',
    ],
    
}
