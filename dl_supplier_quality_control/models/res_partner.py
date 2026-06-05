from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_frequent_failer = fields.Boolean(
        string='Falhas Recorrentes de Entrega', 
        default=False,
        help="Marcado automaticamente se o fornecedor quebrar as regras de qualidade."
    )
    delivery_compliance_rate = fields.Float(
        string='Taxa Global de Cumprimento (%)', 
        compute='_compute_compliance_rate'
    )

    def _compute_compliance_rate(self):
        for partner in self:
            histories = self.env['supplier.delivery.history'].search([('partner_id', '=', partner.id)])
            if histories:
                total_demanded = sum(histories.mapped('qty_demanded'))
                total_received = sum(histories.mapped('qty_received'))
                if total_demanded > 0:
                    partner.delivery_compliance_rate = (total_received / total_demanded) * 100
                else:
                    partner.delivery_compliance_rate = 100.0
            else:
                partner.delivery_compliance_rate = 100.0