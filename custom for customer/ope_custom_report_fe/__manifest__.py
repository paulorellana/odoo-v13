# -*- coding: utf-8 -*-
{
    'name': 'Custom Report Sale Order odoov11 FE',
    'summary': 'Reportes',
    'category': 'Reporting',
     'description': """
Formato de Reportes FE : odoo v13
===============================
    """,
    'depends':
        [
            'base',
            'base_setup',
            'account',
            'sale',          
        ], 
    'data': [
       # 'views/report_paperformat.xml',
       # 'views/report_invoice.xml',
       # 'views/report_view.xml',
         'views/report_invoice_document.xml',
         'views/report_saleorder_document.xml'
       # 'views/header.xml',
        
    ],
    'qweb': [
    ],
    
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
}
