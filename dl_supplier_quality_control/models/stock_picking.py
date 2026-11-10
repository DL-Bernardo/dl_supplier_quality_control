# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _action_done(self):
        res = super(StockPicking, self)._action_done()
        for picking in self:
            if picking.picking_type_code == 'incoming' and picking.partner_id:
                self._process_supplier_quality(picking)
        return res

    def _process_supplier_quality(self, picking):
        history_obj = self.env['supplier.delivery.history']
        moves = getattr(picking, 'move_ids', getattr(picking, 'move_ids_without_package', self.env['stock.move']))

        for move in moves.filtered(lambda m: m.state == 'done'):
            done_qty = getattr(move, 'quantity', getattr(move, 'quantity_done', 0.0))
            history_obj.create({
                'partner_id': picking.partner_id.id,
                'product_id': move.product_id.id,
                'picking_id': picking.id,
                'purchase_id': picking.purchase_id.id if getattr(picking, 'purchase_id', False) else False,
                'date_done': picking.date_done or fields.Datetime.now(),
                'qty_demanded': move.product_uom_qty,
                'qty_received': done_qty,
            })

        self._evaluate_quality_rules(picking.partner_id)

    def _evaluate_quality_rules(self, partner):
        rules = self.env['supplier.quality.rule'].search([('active', '=', True)])
        if not rules:
            return

        history_obj = self.env['supplier.delivery.history']
        now = fields.Datetime.now()

        for rule in rules:
            date_limit = now - timedelta(days=rule.period_days)
            domain_failures = [
                ('partner_id', '=', partner.id),
                ('is_incomplete', '=', True),
                ('date_done', '>=', date_limit)
            ]

            if rule.only_critical_products:
                domain_failures.append(('product_id.product_tmpl_id.is_critical_for_supplier', '=', True))

            failures_count = history_obj.search_count(domain_failures)
            compliance_rate = partner.delivery_compliance_rate

            if failures_count >= rule.min_incomplete_deliveries or compliance_rate < rule.min_compliance_rate:
                if rule.action_mark_supplier and not partner.is_frequent_failer:
                    partner.is_frequent_failer = True
                self._create_rule_alerts(rule, partner, failures_count, compliance_rate)

    def _create_rule_alerts(self, rule, partner, failures, compliance):
        if not rule.notify_user_ids:
            return

        summary = f"Alerta de Qualidade: Fornecedor {partner.name}"
        note = f"""
            <p>O fornecedor <b>{partner.name}</b> atingiu os critérios de falha da regra <b>{rule.name}</b>.</p>
            <ul>
                <li>Entregas incompletas recentes: <b>{failures}</b> (Regra: {rule.min_incomplete_deliveries})</li>
                <li>Taxa de cumprimento: <b>{compliance:.2f}%</b> (Mínimo exigido: {rule.min_compliance_rate}%)</li>
            </ul>
            <p>Por favor, reveja as ordens de compra e o histórico deste fornecedor.</p>
        """

        ir_model = self.env['ir.model']
        res_model_id = ir_model._get_id('res.partner') if hasattr(ir_model, '_get_id') else ir_model._get('res.partner').id
        todo_type = self.env.ref('mail.mail_activity_data_todo', raise_if_not_found=False)

        for user in rule.notify_user_ids:
            vals = {
                'res_id': partner.id,
                'res_model_id': res_model_id,
                'summary': summary,
                'note': note,
                'user_id': user.id,
            }
            if todo_type:
                vals['activity_type_id'] = todo_type.id
            self.env['mail.activity'].create(vals)
