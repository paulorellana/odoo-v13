{
    'name': 'Pos ticket batches and series',
    'version': '13.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': '''
    This module allows you to add the batch number or serial number, at the bottom of the printed format of the invoice receipt
    ''',
    'category': 'Point of Sale',
    'depends': [
        'pos_ticket_format_invoice',
    ],
    'data': [
        "reports/ticket_template.xml",
    ],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 95.00
}
