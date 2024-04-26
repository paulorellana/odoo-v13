{
    'name' : 'Personalización del ticket para el terminal punto de venta',
    'version' : '1.0.0',
    'author' : 'Paul Orellana',
    'license': 'GPL-3',
    'category' : 'Point Of Sale',
    'website' : '',
    'description': """

Tested on Odoo 8.0 f8d5a6727d3e8d428d9bef93da7ba6b11f344284
    """,
    'depends' : ['point_of_sale'],
    'data':[
        
        ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],
    'installable': True,
    'auto_install': False,
}
