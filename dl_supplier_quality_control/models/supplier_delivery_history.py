from odoo import models, fields, api

class SupplierDeliveryHistory(models.Model):
    _name = 'supplier.delivery.history'
    _description = 'Histórico de Entregas de Fornecedores'
    _order = 'date_done desc'

    partner_id = fields.Many2one('res.partner', string='Fornecedor', required=True, index=True)
    product_id = fields.Many2one('product.product', string='Produto', required=True)
    picking_id = fields.Many2one('stock.picking', string='Receção', required=True)
    purchase_id = fields.Many2one('purchase.order', string='Ordem de Compra')
    
    date_done = fields.Datetime(string='Data de Receção', required=True)
    
    qty_demanded = fields.Float(string='Qtd. Demandada')
    qty_received = fields.Float(string='Qtd. Recebida')
    qty_difference = fields.Float(string='Diferença', compute='_compute_difference', store=True)
    
    is_incomplete = fields.Boolean(string='Entrega Incompleta', compute='_compute_difference', store=True)
    compliance_percent = fields.Float(string='% Cumprimento', compute='_compute_difference', store=True)

    @api.depends('qty_demanded', 'qty_received')
    def _compute_difference(self):
        for record in self:
            record.qty_difference = record.qty_received - record.qty_demanded
            record.is_incomplete = record.qty_difference < 0
            
            if record.qty_demanded > 0:
                # Evitar percentagens acima de 100% se enviarem a mais, o foco é na falha
                pct = (record.qty_received / record.qty_demanded) * 100
                record.compliance_percent = min(pct, 100.0)
            else:
                record.compliance_percent = 100.0