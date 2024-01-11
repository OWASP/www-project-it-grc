# -*- coding: utf-8 -*-
{
    'name': "GRCBIT Seller",
    'summary': "App for grcbit seller implementation",
    'description': "Res Partner, Sellers",
    'author':"HackDoo",
    'website': "https://hackdoo.com/",
    'category': 'Uncategorized',
    'version': '16.0',
    'depends': [
        'base',
        'contacts',
        'grcbit_setgroups',
    ],

    # always loaded
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'views/res_partner_views.xml',
        'views/res_company_views.xml',
        'wizards/set_groups_views.xml',
    ],
}
