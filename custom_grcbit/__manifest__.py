# -*- coding: utf-8 -*-
{
    'name': "Custom GRCBIT",
    'summary': "App for grcbit custom implementation referent another models",
    'author':"HackDoo",
    'website': "https://hackdoo.com/",
    'category': 'Uncategorized',
    'version': '16.0',
    'depends': [
        'base',
        'project',
        'mass_mailing',
    ],

    # always loaded
    'data': [
       'views/mass_mailing_views.xml',
       'views/project_task_views.xml',
    ],
}
