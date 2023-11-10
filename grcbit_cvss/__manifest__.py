# -*- coding: utf-8 -*-
{
    'name': "GRCBIT CVSS",
    'summary': "App for grcbit cvss calculator",
    'description': "Calculator CVSS",
    'author':"HackDoo",
    'website': "https://hackdoo.com/",
    'category': 'Uncategorized',
    'version': '16.0',
    'depends': [
        'grcbit_risk_management',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/cvss_calculator_view.xml',
        'views/risk_factor_views.xml',
    ],
}
