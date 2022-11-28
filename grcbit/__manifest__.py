# -*- coding: utf-8 -*-
{
    'name': "grcbit",
    'summary': "Tool for ISO27001:2022 implementation",
    'description': "Tool for ISO27001:2022 implementation",
    'author':"rodolfo.lopez@grcbit.com",
    'website': "www.grcbit.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
