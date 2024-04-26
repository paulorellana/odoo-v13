# -*- coding: utf-8 -*-
{
    'name': 'POS multi UOM product right',
    'version': '13.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': 'This module allows you to modify the unit of measure used in the sale of products at the point of sale.',
    'category': 'Point of Sale',
    'depends': ['point_of_sale'],
    'data': [
        'views/views.xml',
        'views/templates.xml'
    ],
    'qweb': ['static/src/xml/pos.xml'],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 39.90
}