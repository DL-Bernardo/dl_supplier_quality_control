# DL Supplier Quality Control (Vendor Rating)

Módulo avançado para controlo de qualidade e avaliação de desempenho de entregas de fornecedores no Odoo 17. 

## 🌟 Funcionalidades
* **Controlo de Receções:** Calcula automaticamente a diferença entre a quantidade demandada e a recebida.
* **Histórico Consolidado:** Grava todas as diferenças num histórico centralizado (Vendor Rating).
* **Regras de Alerta Automáticas:** Permite definir regras (ex: falhar mais de 3 vezes em 30 dias). Quando um fornecedor atinge a regra, o sistema gera Alertas Internos (To-Do) para a equipa de compras.
* **Marcação de Fornecedor:** Identificação visual através de uma etiqueta (Ribbon) de "Falhas Recorrentes" na ficha do parceiro, além de exibir a taxa de cumprimento (%).
* **Relatórios (Ecrã e PDF):** Exibe a diferença visualmente nas linhas de receção e no Relatório de Receção em PDF.
* **Análise Dinâmica:** Tabela Dinâmica (Pivot) integrada no módulo de Compras para analisar produtos com mais falhas.

## ⚙️ Instalação
1. Coloque a pasta `dl_supplier_quality_control` na diretoria `addons` do Odoo.
2. Reinicie o serviço Odoo.
3. Ative o "Modo de Desenvolvedor".
4. Vá a Aplicações > Atualizar Lista de Aplicações.
5. Procure por "DL Supplier Quality Control" e instale.

## 🚀 Como Usar
1. Vá à aplicação **Compras** > **Vendor Rating**.
2. Configure os parâmetros em **Regras de Alerta** (apenas Gestores).
3. Efetue as receções normais pelo Armazém.
4. Consulte o histórico e os relatórios em **Compras > Vendor Rating > Análise de Entregas**.

## Autor
* Digitalub Angola