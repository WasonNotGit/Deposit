# -*- coding: utf-8 -*-
{
    'name': "deposit_subject_wason",

    'summary': """
        Управляйте сбором сведений о залогах (объектах недвижимости, транспорта и так далее)""",

    'description': """
        Установите группу Залоги / Сотрудник тому сотруднику, в чьи обязанности входит обзвон заемщиков,
        получение от них документов и внесение в Оду сведений из этих документов.
        Права группы Залоги / Руководитель позволяют импортировать лиды из файла
    """,

    "application": True,

    'author': "Wason",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm'],

    # always loaded
    'data': [
        'security/deposit_access_rules.xml',
        'security/ir.model.access.csv',
        'views/deposit_tree_view.xml',
        'views/deposit_form_view.xml',
        'views/deposit_menu.xml',
        'views/templates.xml',
        #'views/resources.xml',
        'data/crm_stage_data.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}