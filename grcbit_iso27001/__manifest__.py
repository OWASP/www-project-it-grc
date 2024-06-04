# -*- coding: utf-8 -*-
{
    'name': "GRCBIT ISO27001",
    'summary': "App for grcbit iso27001 implementation",
    'description': "ISO27001",
    'author':"HackDoo",
    'website': "https://hackdoo.com/",
    'category': 'Uncategorized',
    'version': '16.0',
    'depends': [
        #'web',
        #'project',
        #'mass_mailing',
        'grcbit_base',
        'grcbit_risk_management',
    ],

    # always loaded
    'data': [
        #security
        'security/res_groups.xml',
        'security/ir.model.access.csv',

        #data
        # 'data/control_type_data.xml',
        # 'data/control_category_data.xml',
        # 'data/cybersecurity_concept_data.xml',
        # 'data/operational_capability_data.xml',
        # 'data/security_domain_data.xml',
        # 'data/security_property_data.xml',
        # 'data/iso.control.csv',
        
        #views
        'views/iso_views.xml',
        'views/grcbit_base_views.xml',

        #reports
        'reports/report_statement_applicability.xml',
        'reports/summary_report_statement_applicability.xml',
    ],
    'assets': {
        'web.assets_common': [
            'grcbit_iso27001/static/src/css/iso_style.css',
            
        ],
    }
 
}
