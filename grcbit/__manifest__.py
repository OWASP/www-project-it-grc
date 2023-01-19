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
    'depends': ['base', 'web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/security.xml',
        #'static/src/xml/template.xml',
        #'views/assets.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    #"qweb": [
    #    "static/src/xml/template.xml",
    #],
    #'assets': {
    #'web.assets_backend': [
        #"static/src/xml/template.xml",
        #"/open_in_new_tab/static/src/js/many2one.js",
        #'grcbit/static/src/js/many2one.js',
        #'grcbit/static/src/js/many2many.js',
        #'grcbit/static/src/js/tree_view.js',
        #'grcbit/static/src/xml/template.xml',
    #]
    #},
    'assets': {
        'web.assets_frontend': [
            #'many2many_tags_click_cr/static/src/js/many2many_tags.js'
            #'static/src/js/many2many_tags.js'
            'grcbit/static/src/js/many2many_tags.js',
            'grcbit/static/src/js/many2many_open.js',
            #'many2many_tags_click_cr/static/src/js/many2many_tags.js',
            'static/src/js/many2many_tags.js',
            'static/src/js/many2many_open.js',
            #'static/src/xml/template.xml',
            #'grcbit/static/src/xml/template.xml',
        ],
    },
}
