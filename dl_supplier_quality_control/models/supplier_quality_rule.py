from odoo import models, fields

class SupplierQualityRule(models.Model):
    _name = 'supplier.quality.rule'
    _description = 'Regras de Qualidade de Fornecedores'

    name = fields.Char(string='Nome da Regra', required=True)
    active = fields.Boolean(default=True)
    
    # Condições
    min_incomplete_deliveries = fields.Integer(string='Nº Máx. de Entregas Incompletas', default=3)
    period_days = fields.Integer(string='No Período de (Dias)', default=30)
    min_compliance_rate = fields.Float(string='Taxa de Cumprimento Mínima (%)', default=90.0)
    
    only_critical_products = fields.Boolean(
        string='Apenas Produtos Críticos', 
        default=False,
        help='Se marcado, a regra apenas considerará as falhas em produtos marcados como críticos.'
    )
    
    # Ações
    action_mark_supplier = fields.Boolean(string='Marcar Fornecedor com Falhas Recorrentes?', default=True)
    notify_user_ids = fields.Many2many('res.users', string='Utilizadores a Notificar (Armazém/Compras)')