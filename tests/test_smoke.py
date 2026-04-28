def test_smoke() -> None:
    assert True

def test_stage1_baselines_runs():
    import subprocess
    import sys
    import os
    from pathlib import Path

    # Caminho para um dataset de exemplo (ajuste conforme necessário)
    data_path = Path("data/churn_data_sample.csv")
    if not data_path.exists():
        # Cria um dataset mínimo para teste
        import pandas as pd
        df = pd.DataFrame({
            "feature1": [1, 2, 3, 4],
            "feature2": ["A", "B", "A", "B"],
            "Churn": [1, 0, 0, 1],
        })
        data_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(data_path, index=False)

    # Executa o script de baseline
    result = subprocess.run([
        sys.executable,
        "src/churn_stage1/stage1_baselines.py",
        "--data-path", str(data_path),
        "--target-col", "Churn",
        "--experiment-name", "ci_test_experiment",
        "--test-size", "0.5",
        "--random-state", "123"
    ], capture_output=True, text=True)

    assert result.returncode == 0, f"Erro ao rodar baseline: {result.stderr}"
    assert "MLflow run_id" in result.stdout
