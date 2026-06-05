from odoo import models, fields, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    qty_difference = fields.Float(
        string='Diferença',
        compute='_compute_qty_difference',
        store=True,
        help="Diferença entre o Recebido e o Demandado."
    )

    @api.depends('product_uom_qty', 'quantity', 'picking_id.picking_type_code')
    def _compute_qty_difference(self):
        for move in self:
            # Só fazemos este cálculo para Receções (incoming)
            if move.picking_id.picking_type_code == 'incoming':
                # Odoo 17 usa 'quantity' para o que foi feito, e 'product_uom_qty' para a demanda
                move.qty_difference = move.quantity - move.product_uom_qty
            else:
                move.qty_difference = 0.0