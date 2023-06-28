{
    "name":"POS printer format custom FE",
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
