# -*- coding: utf-8 -*-
{
    'name': "GRCBIT RISK MANAGEMENT",
    'summary': "grc4ciso: GRC + XDR + ZT + GPT",
    'description': "grc4ciso integrates GRC, XDR, Zero Trust and GPT cybersecurity capabilities into a unified Software-as-a-Service (SaaS) platform",
    'author':"grc4ciso",
    'website': "https://grc4ciso.com/",
    'category': 'grc4ciso',
    'version': '16.0',
    'depends': [
        'base',
        'hr',
        'grcbit_base',
    ],

    # always loaded
    'data': [
        #security
        'security/res_groups.xml',
        'security/ir.model.access.csv',

        #data
        # 'data/impact_level_data.xml',
        # 'data/probability_level_data.xml',
        # 'data/risk_classification_data.xml',
        # 'data/risk_level_data.xml',
        # 'data/inherent_risk_level_data.xml',
        # 'data/control_evaluation_criteria_data.xml',
        # 'data/residual_risk_level_data.xml',

        #views
        'views/risk_management_views.xml',
        'views/controls_views.xml',
        'views/menuitems.xml',
        'views/ir_sequence.xml',

        #wizards
        'wizards/set_groups_views.xml',

        #reports
        'reports/report_risk_factor.xml',
    ],
    'assets': {
        'web.assets_common': [
            'grcbit_risk_management/static/src/css/control_style.css',            
        ],
    }
    
}
