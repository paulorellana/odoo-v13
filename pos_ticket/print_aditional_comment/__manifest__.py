# -*- coding: utf-8 -*-
{
    "name": u"Print aditional comment",
    'version': '13.0.1.0.0',
    'author': 'Consultoria Yaroslab',
    'website': 'http://www.yaroslab.com',
    "category": "account",
    "description": """
    Añade campo en la configuración de la compañía/multicompañias, aparecerá impreso en la Factura de Venta, encima del campo "Términos y Condiciones".
    """,
    "depends": ['account'],
    "data": [
        'views/qweb_templates.xml',
        'views/company_views.xml'
    ],
    'qweb': [],
    "installable": True,
    "active": False,
}
