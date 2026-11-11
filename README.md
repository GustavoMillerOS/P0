# P0 — Padronizador Automático de Chamados de Suporte

## 1. Descrição do Problema
Pessoas e usuários finais frequentemente relatam problemas técnicos de forma vaga ou informal (ex: "o sistema parou e não consigo trabalhar"). Este projeto resolve a necessidade de analistas de TI de converter relatos brutos em chamados estruturados.

- **Frase do Problema:** Converter relatos informais de falhas técnicas em relatórios padronizados com diagnóstico inicial e prioridade.
- **Público-alvo:** Equipes de Suporte Técnico / IT Service Desk.

## 2. Entradas e Saídas
- **Entrada:** Texto em linguagem natural com a descrição informal do problema pelo usuário.
- **Saída:** Texto formatado contendo:
  - Título do Chamado
  - Serviço/Equipamento Afetado
  - Resumo Padronizado
  - Prioridade Sugerida (Baixa, Média, Alta)

## 3. Justificativa do uso de LLM
O uso de um Modelo de Linguagem (LLM) é adequado pois a tarefa exige interpretação semântica de textos não estruturados, identificando a intenção do usuário e inferindo a gravidade da falha, algo inviável de realizar apenas com regras fixas de código.
