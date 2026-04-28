# Tech Challenge - Fase 1

**Tema**: Rede Neural para Previsao de Churn com Pipeline Profissional End-to-End

**Dataset**: IBM Telco Customer Churn — 7.043 clientes, 33 variaveis, 26.5% de churn

## Estrutura

```
tech-challenge/
├── src/churn_stage1/       # pipeline, baselines e inferencia
├── data/                   # dataset (nao versionado)
├── models/                 # metricas, amostras e artefatos
├── notebooks/              # EDA e baselines (01_eda_baselines.ipynb)
├── docs/                   # ML Canvas, graficos de EDA
├── tests/                  # smoke test
├── pyproject.toml          # dependencias, lint, pytest
└── .gitignore
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -e ".[dev]"
```

## Etapa 1 - Resultados dos Baselines

| Modelo              | AUC-ROC | PR-AUC | F1    |
|---------------------|---------|--------|-------|
| Logistic Regression | 0.829   | 0.607  | 0.612 |
| DummyClassifier     | 0.500   | 0.265  | 0.000 |

## Dataset recomendado (IBM Telco)

https://www.kaggle.com/datasets/yeanzc/telco-customer-churn-ibm-dataset

Depois de baixar no Kaggle, coloque o arquivo em `data/`.
Se vier em XLSX, mantenha como `data/Telco_customer_churn.xlsx`.
Se vier em CSV, use `data/WA_Fn-UseC_-Telco-Customer-Churn.csv`.

## Como rodar a Etapa 1 (script)

```bash
python -m churn_stage1.stage1_baselines \
  --data-path data/Telco_customer_churn.xlsx \
  --target-col "Churn Value" \
  --experiment-name tech_challenge_stage1
```

A saida impressa inclui o `run_id` da regressao logistica para usar na inferencia.

Resultados gerados:
- `models/stage1_baselines_metrics.csv`
- `docs/stage1_eda_summary.json`
- execucoes no MLflow local (`mlruns/`)

## Abrir MLflow UI

```bash
mlflow ui --port 5001
# Acesse: http://127.0.0.1:5001
```

## Como prever churn (inferencia via MLflow)

```bash
python -m churn_stage1.predict \
  --model-uri "models:/churn_logistic_regression/latest" \
  --data-path data/Telco_customer_churn.xlsx \
  --target-col "Churn Value" \
  --output-path models/churn_predictions.csv
```

Saida: `models/churn_predictions.csv` com `customer_id`, `churn_score` e `churn_pred` ordenados por risco.


## CI/CD Pipeline Automático com MLflow na AWS

### Passo a passo para uso do pipeline:

1. **Suba uma instância EC2 (Ubuntu) na AWS**
  - Libere as portas 22 (SSH) e 5000 (Custom TCP) no Security Group.
  - Anote o IP público.

2. **Acesse a instância via SSH:**
  ```sh
  ssh -i caminho/para/sua-chave.pem ubuntu@IP_DA_INSTANCIA
  ```

3. **Instale dependências e MLflow:**
  ```sh
  sudo apt update
  sudo apt install python3-pip python3-venv sqlite3 -y
  python3 -m venv mlflow-venv
  source mlflow-venv/bin/activate
  pip install --upgrade pip
  pip install mlflow
  mkdir -p ~/mlruns
  chmod 777 ~/mlruns
  ```

4. **Rode o MLflow Tracking Server:**
  ```sh
  mlflow server \
    --host 0.0.0.0 \
    --port 5000 \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root file:///home/ubuntu/mlruns \
    --allowed-hosts '*' \
    --cors-allowed-origins '*'
  ```

5. **Acesse o MLflow pelo navegador:**
  - http://IP_DA_INSTANCIA:5000

6. **Configure o GitHub Actions:**
  - Adicione o valor de `MLFLOW_TRACKING_URI` como `http://IP_DA_INSTANCIA:5000` nas secrets do repositório.

7. **Faça um commit/push para acionar o pipeline CI/CD.**
  - O workflow irá rodar testes, treinar o modelo e registrar no MLflow da AWS.

---
## Checklist da Etapa 1

- [x] ML Canvas preenchido (docs/ml_canvas_template.md)
- [x] EDA com qualidade, distribuicao e data readiness
- [x] Metricas tecnicas definidas (AUC-ROC, PR-AUC, F1)
- [x] Metrica de negocio definida (custo de churn evitado)
- [x] Baseline com DummyClassifier
- [x] Baseline com Regressao Logistica
- [x] Runs registrados no MLflow com parametros, metricas e artefatos
- [x] Modelos registrados no MLflow Model Registry
