# -*- coding: utf-8 -*-
{
    'name': "GRCBIT COMPLIANCE",
    'summary': "grc4ciso: GRC + XDR + ZT + GPT",
    'description': "grc4ciso integrates GRC, XDR, Zero Trust and GPT cybersecurity capabilities into a unified Software-as-a-Service (SaaS) platform",
    'author':"grc4ciso",
    'website': "https://grc4ciso.com/",
    'category': 'grc4ciso',
    'version': '16.0',
    'depends': [
        'grcbit_base',
        'grcbit_iso27001',
    ],

    # always loaded
    'data': [
        #security
        'security/ir.model.access.csv',

        #data
        # 'data/compliance.version.csv',
        # 'data/compliance.control.objective.csv',
        # 'data/compliance.control.csv',

        #reports
        'reports/report_compliance.xml',

        #views
        'views/compliance_views.xml',
    ],
    'assets': {
        'web.assets_common': [
            'grcbit_compliance/static/src/css/compliance_style.css',
            
        ],
    }
    
}
