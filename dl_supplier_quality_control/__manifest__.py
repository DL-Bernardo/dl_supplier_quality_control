# -*- coding: utf-8 -*-
{
    'name': 'DL Supplier Quality Control',
    'version': '17.0.1.0.0',
    'category': 'Inventory/Purchases',
    'summary': 'Controlo de Qualidade, Vendor Rating e Avaliação de Entregas de Fornecedores',
    'description': """
        Módulo avançado para avaliar o cumprimento de entregas dos fornecedores.
        - Compara quantidade demandada vs recebida.
        - Histórico consolidado e relatórios de desempenho.
        - Regras automáticas de alerta (falhas recorrentes, taxa de cumprimento).
        - Marcação visual no cadastro do fornecedor.
        - Notificações automáticas para compras/armazém.
    """,
    'author': 'Digitalub Angola',
    'website': 'https://www.digitalub.ao',
    'license': 'OPL-1',  # Alterado para OPL-1 porque o módulo é pago

    # Configuração de Preço (Conversão de $85 USD)
    'price': 79.00,
    'currency': 'EUR',

    'depends': [
        'base', 
        'stock', 
        'purchase', 
        'purchase_stock', 
        'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking_views.xml',
        'views/res_partner_views.xml',
        'views/supplier_delivery_history_views.xml',
        'views/supplier_quality_rule_views.xml',
        'views/menu_views.xml',
        'views/stock_picking_report_views.xml',
        'views/product_template_views.xml',
    ],
    
    # Imagem de capa para a Loja Odoo
    'images': [
        'static/description/main_screenshot.png'
    ],
    
    'installable': True,
    'application': False,
    'auto_install': False,
}