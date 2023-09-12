# -*- coding: utf-8 -*-
{
	'name': "Power BI Dashboards Integration",

    'summary': """
        Fetch all your Power BI Dashboard into Odoo in one click. Support both Master Login Feature and Organization Level Feature !!!! powerbi
        """,

    'description': """Powerbi odoo integration module gets all your power bi dashboards and show in odoo for analytics. Hosted dashboards and workspace is shown in odoo from power bi service. published and shared powerbi reports are now on your odoo.
        Connect You Power BI Custom Dashboards Into Odoo 
        Easily manage your power bi organizational dashbaards in odoo 
        Power BI Dashboard,
        Power BI Dashboard Connecter,
        Power BI Organization Dashboard ,
        Power BI Organization Dashboard Integration ,
        BI Dashboard, powerbi
        BI Dashboard Manager,
        Power BI Integration,
        Public Dashboard Integration,
        Power BI Dashboard Integration,
        Dashboard Integration In Odoo,
        Power BI Dashboard In Odoo,
        BI Dashboard in Odoo, 
        Odoo Dashboard,
        Dashboard,
        Dashboards,
        Odoo apps,
        Dashboard app,
        HR Dashboard,
        Sales Dashboard,
        inventory Dashboard,
        Lead Dashboard,
        Opportunity Dashboard,
        CRM Dashboard,
        POS,
        POS Dashboard,
        Connectors,
        Web Dynamic,
        Report Import/Export,
        Date Filter,
        HR,
        Sales,
        Theme,
        Tile Dashboard,
        Dashboard Widgets,
        Dashboard Manager,
        Debranding,
        Power BI Customize Dashboard,
        Graph Dashboard,
        Charts Dashboard,
        Invoice Dashboard,
        Project management,
        odoo dashboard apps
        odoo dashboard app
        odoo dashboard module
        odoo modules For Power BI
        dashboards BI
        powerful dashboards
        beautiful odoo dashboard
        odoo dynamic Power BI dashboard
        all in one Power BI dashboard
        multiple dashboard menu
        odoo dashboard portal
        beautiful odoo dashboard
        odoo best dashboard
        dashboard for management
        Odoo custom dashboard
        odoo dashboard management
        odoo dashboard apps
        create odoo dashboard
        odoo dashboard extension Power BI
        odoo BI dashboard module 
        odoo dashboard module 
    """,

    'author': "Odoo Tech",
    'website': "http://www.odootech.in",
    'support': 'helpdesk@odootech.in',
    'maintainer': 'Odoo Tech',
    'category': 'Third Party',
    'version': '1.1',

    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/dashboard.xml',
        'views/org_dashboard.xml',
        'views/menu.xml',
        'views/settings.xml',
        'views/resources.xml',
    ],

    'demo': [
        # 'demo/demo.xml',
    ],
    'assets': {
        'bi_dashboard_connecter.bi_dashboard_asset': ['https://code.jquery.com/jquery-3.1.1.min.js','/bi_dashboard_connecter/static/scr/css/style.scss', '/bi_dashboard_connecter/static/scr/js/app.js','/bi_dashboard_connecter/static/scr/js/app2.js'],
         },

    "application": True,
    "installable": True,
    'images': ['static/description/banner.gif'],
    'license': 'OPL-1',
    'price': '99',
    'currency': 'EUR',
}

