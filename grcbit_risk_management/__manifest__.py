# -*- coding: utf-8 -*-
{
    'name': "GRCBIT RISK MANAGEMENT",
    'summary': "App for grcbit risk management implementation",
    'description': "RISK MANAGEMENT",
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

        #reports
        'reports/report_risk_factor.xml'
    ],
    
}
