# ML Canvas - Tech Challenge Churn

## 1) Problema de negócio
- **Decisão apoiada**: identificar clientes com alto risco de cancelamento para que o time
  de retenção possa agir de forma proativa (oferta de desconto, contato personalizado).
- **Impacto esperado**: redução da taxa de churn atual de ~26,5% e preservação de receita
  recorrente mensal (MRR). O custo de reter um cliente é estimado como menor do que o custo
  de adquirir um novo.

## 2) Stakeholders
- **Dono de negócio**: Diretoria Comercial / VP de Customer Success
- **Time de dados**: Engenharia de ML (construção e manutenção do modelo)
- **Time de produto/operação**: CRM e time de retenção (consumidores do score)
- **Usuários finais do score**: analistas de retenção e gestores de contas

## 3) Definição de churn
- **Evento que define churn**: cancelamento do contrato pelo cliente (Churn Value = 1)
- **Janela de observação**: histórico de uso e faturamento até o momento da predição
- **Janela de previsão**: próximo ciclo de faturamento (mensal)

## 4) Dados
- **Fonte**: IBM Telco Customer Churn Dataset (Kaggle: yeanzc/telco-customer-churn-ibm-dataset)
- **Granularidade**: 1 linha por cliente (contrato ativo ou encerrado)
- **Volume**: 7.043 clientes, 33 variáveis originais (32 após remover CustomerID)
- **Período coberto**: snapshot estático — Q3 de uma operadora fictícia da Califórnia
- **Qualidade e lacunas**:
  - Total Charges: 11 valores ausentes (clientes novos sem faturamento acumulado) — imputados com mediana
  - Churn Reason: 5.174 valores ausentes (só preenchido para quem já cancelou) — removida antes do treino
  - Demais colunas: sem ausências

## 5) Métricas

### Métricas técnicas
| Métrica  | Baseline (Dummy) | Baseline (LogReg) | Meta MLP |
|----------|-----------------|-------------------|----------|
| AUC-ROC  | 0.500           | **0.829**         | > 0.85   |
| PR-AUC   | 0.265           | **0.607**         | > 0.65   |
| F1       | 0.000           | **0.612**         | > 0.63   |

### Métrica de negócio
`valor_retido = TP * ticket_medio_mensal - FP * custo_contato - FN * ticket_medio_mensal`

Interpretação: cada cliente corretamente identificado como churn e retido preserva o ticket
mensal; contatos desnecessários (FP) têm custo operacional; clientes que churnam sem
intervenção (FN) representam perda total de receita.

## 6) SLOs e restrições
- **Latência máxima**: < 500ms por requisição (batch ou real-time via API)
- **Frequência de atualização**: re-treino mensal ou quando AUC-ROC cair > 3pp do baseline
- **Custo operacional**: modelo deve rodar em infraestrutura compartilhada (sem GPU dedicada)

## 7) Riscos e vieses
- **Viés geográfico**: dataset restrito à Califórnia — generalização para outros estados não garantida
- **Viés de contrato**: clientes month-to-month têm taxa de churn muito maior; modelo pode
  superpenalizar esse grupo
- **Data leakage**: colunas Churn Score, Churn Reason e Churn Label foram removidas antes
  do treino pois são derivadas do próprio evento de churn
- **Plano de mitigação**: validação cruzada estratificada, análise de fairness por subgrupo
  (gênero, senior citizen), monitoramento de distribuição de features em produção

## 8) Plano de validação
- **Split**: train/test estratificado por Churn Value (80/20), seed 42
- **Cross-validation**: StratifiedKFold k=5 para seleção de hiperparâmetros
- **Baselines**: DummyClassifier (referência mínima) e LogisticRegression (referência linear)
- **Critério mínimo para promover modelo**: AUC-ROC > 0.85 e F1 > 0.63 no conjunto de teste
