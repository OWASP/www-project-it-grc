# -*- coding: utf-8 -*-
{
    'name': "GRCBIT CVSS",
    'summary': "grc4ciso: GRC + XDR + ZT + GPT",
    'description': "grc4ciso integrates GRC, XDR, Zero Trust and GPT cybersecurity capabilities into a unified Software-as-a-Service (SaaS) platform",
    'author':"grc4ciso",
    'website': "https://grc4ciso.com/",
    'category': 'grc4ciso',
    'version': '1.2',
    'depends': [
        'grcbit_risk_management',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/cvss_calculator_view.xml',
        'views/risk_factor_views.xml',
        'reports/report_risk_factor_inherit.xml',
    ],
}
