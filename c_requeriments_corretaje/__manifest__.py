# -*- coding: utf-8 -*-
{
    'name': "c_requirements_corretaje",

    'summary': """
       Custom for corretaje bussines from Peru""",

    'description': """
        Long description of module's purpose
    """,

    'author': "odooperuerp",
    'website': "odooperuerp.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','mrp','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/corretaje.xml',
    ],
    # only loaded in demonstration mode
    'demo_xml': [],
    'active':True,
    'installable':True,
}
