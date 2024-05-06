{
    'name': 'Select invoice format from POS',
    'version': '13.0.1.1.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': 'Select which invoice printing format will be used when issuing an Invoice from the Point of Sale.',
    'category': 'Point of Sale',
    'depends': ['point_of_sale'],
    'data': [
        'views/pos_config_views.xml',
        'static/src/xml/assets.xml'
    ],
    'qweb': ['static/src/xml/pos.xml'],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 45.00
}
