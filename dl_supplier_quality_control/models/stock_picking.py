from odoo import models, fields, api
from datetime import timedelta

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _action_done(self):
        # 1. Executa a validação normal do Odoo (move o stock)
        res = super(StockPicking, self)._action_done()
        
        # 2. Pós-processamento para Controlo de Qualidade do Fornecedor
        for picking in self:
            # Só analisa se for uma Entrada (Receção) e se tiver um Fornecedor associado
            if picking.picking_type_code == 'incoming' and picking.partner_id:
                self._process_supplier_quality(picking)
        
        return res

    def _process_supplier_quality(self, picking):
        history_obj = self.env['supplier.delivery.history']
        
        # A. Criar o Registo de Histórico para cada produto recebido
        for move in picking.move_ids.filtered(lambda m: m.state == 'done'):
            history_obj.create({
                'partner_id': picking.partner_id.id,
                'product_id': move.product_id.id,
                'picking_id': picking.id,
                'purchase_id': picking.purchase_id.id if picking.purchase_id else False,
                'date_done': picking.date_done or fields.Datetime.now(),
                'qty_demanded': move.product_uom_qty,
                'qty_received': move.quantity,
            })
            
        # B. Avaliar o Fornecedor contra as Regras de Qualidade
        self._evaluate_quality_rules(picking.partner_id)

    def _evaluate_quality_rules(self, partner):
        rules = self.env['supplier.quality.rule'].search([('active', '=', True)])
        if not rules:
            return

        history_obj = self.env['supplier.delivery.history']
        now = fields.Datetime.now()

        for rule in rules:
            # Calcular o limite de data (ex: últimos 30 dias)
            date_limit = now - timedelta(days=rule.period_days)
            
            # Preparar o domínio de pesquisa base
            domain_failures = [
                ('partner_id', '=', partner.id),
                ('is_incomplete', '=', True),
                ('date_done', '>=', date_limit)
            ]
            
            # Se a regra restringe a produtos críticos, adiciona condição
            if rule.only_critical_products:
                domain_failures.append(('product_id.product_tmpl_id.is_critical_for_supplier', '=', True))
            
            # Contar quantas entregas falharam neste período
            failures_count = history_obj.search_count(domain_failures)

            # Obter a taxa de cumprimento geral do fornecedor
            compliance_rate = partner.delivery_compliance_rate

            # Verificar se violou as regras
            if failures_count >= rule.min_incomplete_deliveries or compliance_rate < rule.min_compliance_rate:
                
                # Ação 1: Marcar visualmente o fornecedor (se ainda não estiver marcado)
                if rule.action_mark_supplier and not partner.is_frequent_failer:
                    partner.is_frequent_failer = True
                
                # Ação 2: Gerar Notificações / Atividades Internas
                self._create_rule_alerts(rule, partner, failures_count, compliance_rate)

    def _create_rule_alerts(self, rule, partner, failures, compliance):
        if not rule.notify_user_ids:
            return
        
        # Prepara a mensagem de alerta
        summary = f"🚨 Alerta de Qualidade: Fornecedor {partner.name}"
        note = f"""
            <p>O fornecedor <b>{partner.name}</b> atingiu os critérios de falha da regra <b>{rule.name}</b>.</p>
            <ul>
                <li>Entregas incompletas recentes: <b>{failures}</b> (Regra: {rule.min_incomplete_deliveries})</li>
                <li>Taxa de cumprimento: <b>{compliance:.2f}%</b> (Mínimo exigido: {rule.min_compliance_rate}%)</li>
            </ul>
            <p>Por favor, reveja as ordens de compra e o histórico deste fornecedor.</p>
        """
        
        # Adiciona uma "Atividade" (To-Do / Tarefa) para cada utilizador configurado na regra
        for user in rule.notify_user_ids:
            self.env['mail.activity'].create({
                'res_id': partner.id,
                'res_model_id': self.env['ir.model']._get('res.partner').id,
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'summary': summary,
                'note': note,
                'user_id': user.id,
            })