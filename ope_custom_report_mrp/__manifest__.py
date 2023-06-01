# -*- coding: utf-8 -*-
{
    'name': 'MRP order Report  odoov13',
    'summary': 'Reportes',
    'category': 'Reporting',
     'description': """
Formato de Reportes de produccion : odoo v13
===============================
    """,
    'depends':
        [
            'base',
            'base_setup',
            'stock',
            'mrp',
           # 'l10n_pe_base',
        ],
    'data': [
        'views/report_mrporder.xml',
        'views/report_mrp.xml',
      #  'views/views_report.xml',
      #  'security/ir.model.access.csv'

    ],
   
}
