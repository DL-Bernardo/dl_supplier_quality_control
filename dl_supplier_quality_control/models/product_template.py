from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_critical_for_supplier = fields.Boolean(
        string='Produto Crítico (Qualidade de Fornecedores)',
        default=False,
        help='Se marcado, este produto será vigiado por regras de qualidade que focam apenas em produtos críticos.'
    )
