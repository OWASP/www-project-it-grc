# -*- coding: utf-8 -*-

{
    'name': 'Nomina Electrónica para México CFDI v1.2',
    'summary': 'Agrega funcionalidades para timbrar la nómina electrónica en México.',
    'description': '''
    Nomina CFDI Module
    ''',
    'author': 'IT Admin',
    'version': '16.02',
    'category': 'Employees',
    'depends': [
        'om_hr_payroll', 'cdfi_invoice'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'data/cron.xml',
        'data/nomina.otropago.csv',
        'data/nomina.percepcion.csv',
        'data/nomina.deduccion.csv',
        'views/hr_employee_view.xml',
        'views/hr_contract_view.xml',
        'views/hr_salary_view.xml',
        'views/hr_payroll_payslip_view.xml',
        'views/tablas_cfdi_view.xml',
        'views/res_company_view.xml',
        'report/report_payslip.xml',
        'views/res_bank_view.xml',
        'data/mail_template_data.xml',
        'data/res.bank.csv',
        'views/menu.xml',
        'views/horas_extras_view.xml',
        'wizard/wizard_liquidacion_view.xml',
        'wizard/import_nomina_xml.xml',
        'wizard/listado_de_nomina_wizard_view.xml',
        'wizard/generar_recibo_nomina.xml',
        'views/confirmar_cancelar_nomina.xml',
        'wizard/dar_baja_view.xml',
        'wizard/enviar_nomina_view.xml',
        'views/registro_patronal.xml',
        'views/caja_ahorro_view.xml',
        'wizard/entrega_fondo_caja_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'nomina_cfdi/static/src/js/caja_nomina.js',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
