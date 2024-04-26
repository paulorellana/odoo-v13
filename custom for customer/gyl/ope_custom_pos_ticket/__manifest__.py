{
    "name":"POS printer format custom",
    
    'summary': """
        Custumize format ticket""",

    'description': """
        Custumize format ticket , show quantities without decimals, change font size and type
    """,

    'author': "odooperuerp",
    'website': "odooperuerp.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',


    "depends":['base','point_of_sale',
                'pos_order_mgmt',
                'gestionit_pe_fe',
                'gestionit_pe_ubicaciones',
                'gestionit_pe_consulta_ruc_dni',
                'l10n_latam_base'
                ],
    "data":[
    ],
    "qweb":[
        "static/src/xml/order_receipt.xml",
    ]
}
