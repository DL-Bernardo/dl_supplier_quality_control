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
        histories_data = self.env['supplier.delivery.history'].read_group(
            [('partner_id', 'in', self.ids)],
            ['qty_demanded:sum', 'qty_received:sum'],
            ['partner_id']
        )

        history_map = {
            data['partner_id'][0]: {
                'qty_demanded': data['qty_demanded'],
                'qty_received': data['qty_received']
            }
            for data in histories_data
        }

        for partner in self:
            partner_data = history_map.get(partner.id)
            if partner_data:
                total_demanded = partner_data['qty_demanded']
                total_received = partner_data['qty_received']
                if total_demanded > 0:
                    partner.delivery_compliance_rate = (total_received / total_demanded) * 100
                else:
                    partner.delivery_compliance_rate = 100.0
            else:
                partner.delivery_compliance_rate = 100.0