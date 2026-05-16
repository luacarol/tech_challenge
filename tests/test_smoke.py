def test_smoke() -> None:
    assert True


def test_stage1_baselines_runs(tmp_path):
    import subprocess
    import sys
    from pathlib import Path

    import pandas as pd

    # Dataset mínimo para smoke test — isolado de data/ para não sujar artefatos reais
    data_path = tmp_path / "churn_sample.csv"
    df = pd.DataFrame({
        "feature1": [1, 2, 3, 4, 5, 6, 7, 8],
        "feature2": ["A", "B", "A", "B", "A", "B", "A", "B"],
        "Churn": [1, 0, 0, 1, 1, 0, 0, 1],
    })
    df.to_csv(data_path, index=False)

    # --output-dir aponta para tmp_path: saídas não sobrescrevem artefatos de entrega
    result = subprocess.run(
        [
            sys.executable,
            "src/churn_stage1/stage1_baselines.py",
            "--data-path", str(data_path),
            "--target-col", "Churn",
            "--experiment-name", "ci_test_experiment",
            "--test-size", "0.5",
            "--random-state", "123",
            "--output-dir", str(tmp_path),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"Erro ao rodar baseline: {result.stderr}"
    assert "MLflow run_id" in result.stdout
    # Verifica que os arquivos foram criados no diretório temporário
    assert (tmp_path / "models" / "stage1_baselines_metrics.csv").exists()
    assert (tmp_path / "docs" / "stage1_eda_summary.json").exists()
