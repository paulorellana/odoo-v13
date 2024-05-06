# -*- coding: utf-8 -*-
{
    "name": u"QR - Factura Electrónica",
    'version': '13.0.1.0.0',
    'author': 'Consultoria Yaroslab',
    'website': 'http://www.yaroslab.com',
    "category": "account",
    "description": """
    Genera el código QR en la impresión de las Facturas de Venta.
    """,
    "depends": [
        'account',
        'l10n_latam_invoice_document'
    ],
    "data": [
        'views/qweb_templates.xml'
    ],
    'qweb': [],
    "installable": True,
    "active": False,
}
