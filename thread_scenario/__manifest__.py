# -*- coding: utf-8 -*-
{
    'name': "thread Scenario",
    'summary': "grc4ciso: GRC + XDR + ZT + GPT",
    'description': "grc4ciso integrates GRC, XDR, Zero Trust and GPT cybersecurity capabilities into a unified Software-as-a-Service (SaaS) platform",
    'author':"grc4ciso",
    'website': "https://grc4ciso.com/",
    'category': 'Uncategorized',
    'version': '16.0',
    'depends': [
        'base',
        'grcbit_base',
    ],

    # always loaded
    'data': [
        #security
        'security/ir.model.access.csv',

        #views
        'views/views.xml',
        'views/menuitems.xml',
    ],
    'installable': True,
    'application': True,
}
