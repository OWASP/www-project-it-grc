# -*- coding: utf-8 -*-
{
    'name': "GRCBIT PCI",
    'summary': "grc4ciso: PCI",
    'description': "grc4ciso integrates PCI (SaaS) platform",
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
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    
    'installable': True,
}
