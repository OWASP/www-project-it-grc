# -*- coding: utf-8 -*-
{
    'name': "GRCBIT COMPLIANCE",
    'summary': "App for grcbit compliance implementation",
    'description': "The NIST Special Publication 800-53, Security and Privacy Controls for Information Systems and Organizations is a set of recommended security and privacy controls for federal information systems and organizations to help meet the Federal Information Security Management Act (FISMA) requirements.",
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
        'data/compliance.version.csv',
        'data/compliance.control.objective.csv',
        'data/compliance.control.csv',

        #reports
        'reports/report_compliance.xml',

        #views
        'views/compliance_views.xml',
    ],
    
}
