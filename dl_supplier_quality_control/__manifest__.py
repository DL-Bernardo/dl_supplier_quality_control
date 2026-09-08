# -*- coding: utf-8 -*-
{
    'name': 'DL Supplier Quality Control - Vendor Rating & Delivery Performance',
    'version': '17.0.1.0.1',
    'category': 'Inventory/Purchases',
    'summary': 'Supplier Quality Control, Vendor Rating, Delivery Discrepancy Tracking & On-Time In-Full (OTIF) Evaluation',
    'description': """
        Advanced Supplier Quality Control & Vendor Performance Rating for Odoo 17 Community & Enterprise.
        Key Features:
        - Automated comparison of ordered vs. received quantities on warehouse receipts.
        - Dynamic Vendor Rating calculation based on fulfillment accuracy and return rates.
        - Configurable quality alert rules (recurring delivery failures, tolerance thresholds).
        - Visual vendor rating badges directly on Contact and Purchase Order views.
        - Consolidated delivery history log with complete audit trail.
        - Multi-dimensional BI and Pivot analysis for procurement intelligence.
    """,
    'author': 'DIGITALUB ANGOLA, LDA',
    'website': 'https://www.digitalub.ao',
    'support': 'suporte@digitalub.ao',
    'license': 'OPL-1',

    # Configuração de Preço
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
    
    # Imagens de destaque na Loja Odoo
    'images': [
        'static/description/banner.png',
        'static/description/main_screenshot.png'
    ],
    
    'installable': True,
    'application': False,
    'auto_install': False,
}
