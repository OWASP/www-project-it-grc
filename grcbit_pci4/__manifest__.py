# -*- coding: utf-8 -*-
{
    'name': "GRCBIT PCI4",
    'summary': "grc4ciso: GRC + XDR + ZT + GPT",
    'description': "grc4ciso integrates GRC, XDR, Zero Trust and GPT cybersecurity capabilities into a unified Software-as-a-Service (SaaS) platform",
    'author':"grc4ciso",
    'website': "https://grc4ciso.com/",
    'category': 'grc4ciso',
    'version': '16.0',

    'depends': [
        'base',
        'grcbit_base',
        'grcbit_risk_management',
        'grcbit_compliance',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    
    'installable': True,
}
