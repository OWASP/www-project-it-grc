# -*- coding: utf-8 -*-
{
    'name': "mana_dashboard_gauge",

    'summary': """
        Guage chart form mana_dashboard
    """,

    'description': """
        Guage chart form mana_dashboard
        Dashboard
        Guage chart
        mana_dashboard_gauge
        Powerfull dashboard
        nice dashboard
        dashboard for odoo
        odoo dashboard
        simple dashboard
        bi
        simple bi
        nice bi
    """,

    'author': "Funenc co,.ltd",
    'website': "https://www.openerpnext.com",

    'category': 'Apps/Dashboards',
    'version': '16.0.0.1',
    'license': 'OPL-1',
    'price': 10.00,

    'depends': ['base', 'mana_dashboard'],
    'images': ['static/description/banner.png'],

    'data': [
        'data/mana_gauge_chart_template.xml',
    ],

    'assets': {
        'web.assets_backend': [
            "/mana_dashboard_gauge/static/js/mana_gauge_chart.js",
        ]
    }
}
