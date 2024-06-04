# -*- encoding: utf-8 -*-
{
    'name': "Zero Trust Iframe",
    'summary': """This module allows Clients to view external content through zero trust iframes.""",
    'description': """
        This module allows Clients to view external content through zero trust iframes.
    """,
    'version': '16.0',
    'category': 'Dashboards',
    'license': 'OPL-1',
    'author': "HackDoo",
    'depends': [
        'base',
        #'mail',
        #'vista_backend_theme',
        'grcbit_setgroups',
    ],
    'data': [
        'security/zero_trust_access_rules.xml',
        'security/ir.model.access.csv',
        'views/zero_trust.xml',
        'views/menuitems.xml',
        'wizards/set_groups_views.xml',
    ],
'assets': {
        'web.assets_backend': [
            '/grcbit_zt/static/src/js/iframe.js',
        ]},
    'images': [
        'static/description/main_screenshot.gif'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
