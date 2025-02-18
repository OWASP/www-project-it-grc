# -*- coding: utf-8 -*-
{
    'name': 'GRCBIT SET GROUPS',
    'summary': "grc4ciso: GRC + XDR + ZT + GPT",
    'description': "grc4ciso integrates GRC, XDR, Zero Trust and GPT cybersecurity capabilities into a unified Software-as-a-Service (SaaS) platform",
    'author':"grc4ciso",
    'website': "https://grc4ciso.com/",
    'category': 'grc4ciso',
    'version': '1.2',

    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_users_views.xml',
        'wizard/set_groups_views.xml',
    ],

    'auto_install': False,
    'application': False,

}
