# Etapa 1 - Definições

## Métricas técnicas
- AUC-ROC: desempenho global em classificação binária.
- PR-AUC: foco em qualidade na classe positiva (churn).
- F1: equilíbrio entre precision e recall no threshold escolhido.

## Métrica de negócio (template)
Use este cálculo para discutir custo evitado:

`custo_evitar_churn = TP * valor_cliente_retido - FP * custo_contato - FN * custo_perda`

Onde:
- `TP`: clientes de churn previstos corretamente.
- `FP`: clientes sem churn impactados por ação desnecessária.
- `FN`: churn não identificado.
