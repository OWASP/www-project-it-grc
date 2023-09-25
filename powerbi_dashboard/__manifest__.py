{
    'name': 'Dashboard PowerBI (with 5 Hours support) ',
    'version': '16.0.0.1',
    'summary': 'PowerBI Dashboard',
    'sequence': 3,
    'description': "BI Dashboard",
    'author': 'Geo Technosoft',
    'category': 'Dashboard',
    'depends': ['base', 'web'],
    'website': 'https://www.geotechnosoft.com',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/dashboard_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/powerbi_dashboard/static/src/js/dashboard.js',
            '/powerbi_dashboard/static/src/xml/dashboard.xml'
        ],
    },
    'qweb': ["static/src/xml/dashboard.xml"],
    'images': ['static/description/banner.png'],
    'price': 49.00,
    'currency':'USD',
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'OPL-1',
}

