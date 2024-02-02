# -*- coding: utf-8 -*-
{
    'name': 'odoo17 Tweak,Ai Employee,Boost,Customize All in One. Customize,UI,Boost,Security,Data',
    'version': '16.24.01.02',
    'author': 'odooai.cn',
    'category': 'Extra Tools',
    'website': 'https://www.odooai.cn',
    'live_test_url': 'https://demo.odooapp.cn',
    'license': 'LGPL-3',
    'sequence': 2,
    'images': ['static/description/banner.gif'],
    'summary': """
    Ai as employee.1 click Tweak odoo. 48 Functions odoo enhancement. for Customize,UI,Boost Security,Development.
    Easy reset data, clear data, reset account chart, reset Demo data.
    For quick debug. Set brand,Language Switcher all in one.
    """,
    'depends': [
        'app_common',
        'base_setup',
        'web',
        'mail',
    ],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/app_odoo_customize_views.xml',
        'views/app_theme_config_settings_views.xml',
        'views/res_config_settings_views.xml',
        'views/ir_views.xml',
        'views/ir_module_module_views.xml',
        'views/ir_translation_views.xml',
        'views/ir_module_addons_path_views.xml',
        'views/ir_ui_menu_views.xml',
        'views/ir_ui_view_views.xml',
        'views/ir_model_fields_views.xml',
        'views/ir_model_data_views.xml',
        # data
        'data/ir_config_parameter_data.xml',
        'data/ir_module_module_data.xml',
        # 'data/digest_template_data.xml',
        'data/res_company_data.xml',
        'data/res_config_settings_data.xml',
    ],
    # 'qweb': [
    #     'static/src/xml/*.xml',
    # ],
    'assets': {
        'web.assets_backend': [
            'app_odoo_customize/static/src/scss/app.scss',
            'app_odoo_customize/static/src/scss/ribbon.scss',
            'app_odoo_customize/static/src/scss/dialog.scss',
            'app_odoo_customize/static/src/js/user_menu.js',
            'app_odoo_customize/static/src/js/ribbon.js',
            'app_odoo_customize/static/src/js/dialog.js',
            'app_odoo_customize/static/src/webclient/*.js',
            'app_odoo_customize/static/src/webclient/*.xml',
            'app_odoo_customize/static/src/xml/res_config_edition.xml',
        ],
    },
    'pre_init_hook': 'pre_init_hook',
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': True,
    'auto_install': True,
    'description': """
    App Customize Odoo (Change Title,Language,Documentation,Quick Debug)
    ============
    For Odoo17. Please get from the follow github. Done for 85%.
    https://github.com/guohuadeng/app-odoo/tree/17.0
    White label odoo. UI and Development Enhance.
    Support odoo 17,16,15,14,13,12,11,10,9.
    You can config odoo, make it look like your own platform.
    ============
    1. Deletes Odoo label in footer
    2. Replaces "Odoo" in Windows title
    3. Customize Documentation, Support, About links and title in usermenu
    4. Adds "Developer mode" link to the top right-hand User Menu.
    5. Adds Quick Language Switcher to the top right-hand User Menu.
    6. Adds Country flags  to the top right-hand User Menu.
    7. Adds English and Chinese user documentation access to the top right-hand User Menu.
    8. Adds developer documentation access to the top right-hand User Menu.
    9. Customize "My odoo.com account" button
    10. Standalone setting panel, easy to setup.
    11. Provide 236 country flags.
    12. Multi-language Support.
    13. Change Powered by Odoo in login screen.(Please change '../views/app_odoo_customize_view.xml' #15)
    14. Quick delete test data in Apps: Sales/POS/Purchase/MRP/Inventory/Accounting/Project/Message/Workflow etc.
    15. Reset All the Sequence to beginning of 1: SO/PO/MO/Invoice...
    16. Fix odoo reload module translation bug while enable english language
    17. Stop Odoo Auto Subscribe(Moved to app_odoo_boost)
    18. Show/Hide Author and Website in Apps Dashboard
    19. One Click to clear all data (Sometime pls click twice)
    20. Show quick upgrade in app dashboard, click to show module info not go to odoo.com
    21. Can clear and reset account chart. Be cautious
    22. Update online manual and developer document to odoo12
    23. Add reset or clear website blog data
    24. Customize Odoo Native Module(eg. Enterprise) Url
    25. Add remove expense data
    26. Add multi uninstall modules
    27. Add odoo boost modules link.
    28. Easy Menu manager.
    29. Apps version compare. Add Install version in App list. Add Local updatable filter in app list.
    30. 1 key export app translate file like .po file.
    31. Show or hide odoo Referral in the top menu.
    32. Fix odoo bug of complete name bug of product category and stock location..
    33. Add Demo Ribbon Setting.
    34. Add Remove all quality data.
    35. Fixed for odoo 14.
    36. Add refresh translate for multi module.
    37. Easy noupdate manage for External Identifiers(xml_id)
    38. Add Draggable and sizeable Dialog enable.
    39. Only erp manager can see debug menu..
    40. Fix support for enterprise version.
    41. Fix odoo bug, when click Preferences menu not hide in mobile.
    42. Mobile Enhance. Add menu navbar setup for top or bottom. navigator footer support.
    43. Check to only Debug / Debug Assets for Odoo Admin. Deny debug from url for other user.
    44. Check to stop subscribe and follow. This to make odoo speed up.
    45. Add addons path info to module.
    46. Add Help documentation anywhere.  easy get help for any odoo operation or action.
    47. Add ai robot app integration. Use Ai as your employee.
    """,
}
