# -*- coding: utf-8 -*-
##############################################################################
#                 @author IT Admin
#
##############################################################################

{
    'name': 'Contabildad Electronica Mexico',
    'version': '16.02',
    'description': ''' Contabilidad Electronica para Mexico (CFDI 1.3)
    ''',
    'category': 'Accounting',
    'author': 'IT Admin',
    'website': 'www.itadmin.com.mx',
    'depends': [
        'base',
        'account',
        'date_range',
        'report_xlsx',
        'cdfi_invoice',
        'web',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'data/res_currency_data.xml',
        'data/catalogos.pais_diot.csv',
        'wizard/trial_balance_wizard_view.xml',
        'menuitems.xml',
        'reports.xml',
        'report/templates/layouts.xml',
        'report/templates/trial_balance.xml',
        'report/templates/account_hirarchy.xml',
        'views/account_account_view.xml',
        'views/account_group.xml',
        'views/res_partner_view.xml',
        'views/res_currency_views.xml',
        'views/report_trial_balance.xml',
        'views/report_template.xml',
        'views/account_move.xml',
        'views/account_payment.xml',
        'views/iva_pedimentos.xml',
        "wizard/generar_xml_hirarchy.xml",
        "wizard/polizas_report_view.xml",
        "wizard/reporte_diot.xml",
        'wizard/actualizar_polizas_view.xml',
        'wizard/cierre_anual_view.xml',
        'wizard/folios_report_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
           "contabilidad_cfdi/static/src/js/web_ir_actions_act_multi.js",
           "contabilidad_cfdi/static/src/js/list_controller.js",
           "contabilidad_cfdi/static/src/css/report.css",
           "contabilidad_cfdi/static/src/js/account_financial_report_backend.js",
           "contabilidad_cfdi/static/src/js/account_financial_report_widgets.js",
           "contabilidad_cfdi/static/src/js/client_action.js",
           "contabilidad_cfdi/static/src/xml/report_action.xml",
           "contabilidad_cfdi/static/src/xml/list_controller.xml",
            ],
        'web.report_assets_common': [
            "contabilidad_cfdi/static/src/js/report.js",
        ],
    },
    'application': False,
    'installable': True,
    'price': 0.00,
    'currency': 'USD',
    'license': 'AGPL-3',
}
