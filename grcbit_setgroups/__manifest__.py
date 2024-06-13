# -*- coding: utf-8 -*-
{
    'name': 'GRCBIT Set Groups',
    'version': '16.0',
    'summary': "grc4ciso: GRC + XDR + ZT + GPT",
    'description': "grc4ciso integrates GRC, XDR, Zero Trust and GPT cybersecurity capabilities into a unified Software-as-a-Service (SaaS) platform",
    'author':"grc4ciso",
    'website': "https://grc4ciso.com/",
    'license': 'OPL-1',
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
