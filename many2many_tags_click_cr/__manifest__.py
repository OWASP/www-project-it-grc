# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': "Many2Many Tag Record Open",

    'summary': """
        This module allows you to open Many2Many record. it will be applicable to any Many2Many Widget by adding widget""",

    'description': """        
        Many2many tags widget open record in readonly.
        =================================
        Many2many tags widget open record in readonly.
        
        Description
        ----------- 
        
        - This module allows you to open Many2Many record. it will be applicable to any Many2Many Widget by adding widget.  
        
    """,

    'author': "Candidroot Solutions Pvt Ltd",
    'website': "https://www.candidroot.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Extra Tools',
    'version': '16.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['web'],

    # always loaded
    'data': [],
    'images' : ['static/description/Banner.JPEG'],
    'live_test_url': 'https://youtu.be/-zrckumYmUw',
    'price': 5.99,
    'assets': {
        'web.assets_backend': [
            'many2many_tags_click_cr/static/src/js/many2many_tags.js',
        ]
    },
    'currency': 'USD',
    'installable': True,
    'auto_install': False,
    'application': False
}
