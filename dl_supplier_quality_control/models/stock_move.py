# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    qty_difference = fields.Float(
        string='Diferença',
        compute='_compute_qty_difference',
        store=True,
        help="Diferença entre o Recebido e o Demandado."
    )

    @api.depends('product_uom_qty', 'quantity_done', 'picking_id.picking_type_code')
    def _compute_qty_difference(self):
        for move in self:
            if move.picking_id.picking_type_code == 'incoming':
                done_qty = getattr(move, 'quantity_done', getattr(move, 'quantity_done', 0.0))
                move.qty_difference = done_qty - move.product_uom_qty
            else:
                move.qty_difference = 0.0
