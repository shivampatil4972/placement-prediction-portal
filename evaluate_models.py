"""
Model evaluation script for Placement Portal.
Evaluates placement classification and salary regression using saved models
against available training dataset files.
"""

from __future__ import annotations

import json
import os
from datetime import datetime

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
)

from ml_utils import ml_predictor

PLACEMENT_FEATURES = [
    "cgpa",
    "branch_code",
    "internship_count",
    "project_count",
    "certification_count",
    "skill_count",
]

SALARY_FEATURES = ["cgpa", "internship_count", "placement_probability"]


def load_dataset() -> pd.DataFrame:
    """Load the most detailed dataset available in workspace."""
    candidates = ["training_data_advanced.csv", "training_data.csv"]
    for candidate in candidates:
        if os.path.exists(candidate):
            print(f"Using dataset: {candidate}")
            return pd.read_csv(candidate)
    raise FileNotFoundError("No training dataset found. Expected training_data_advanced.csv or training_data.csv")


def _safe_mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    denom = np.where(np.abs(y_true) < 1e-9, 1e-9, np.abs(y_true))
    return float(np.mean(np.abs((y_true - y_pred) / denom)) * 100)


def evaluate_placement(df: pd.DataFrame) -> dict:
    required = PLACEMENT_FEATURES + ["placed"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Placement evaluation requires columns: {missing}")

    if ml_predictor.placement_model is None:
        raise RuntimeError("placement_model.pkl is not loaded. Train model first.")

    x = df[PLACEMENT_FEATURES]
    y_true = df["placed"].to_numpy()

    y_pred = ml_predictor.placement_model.predict(x)
    y_prob = ml_predictor.placement_model.predict_proba(x)[:, 1]

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

    return {
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, y_pred, zero_division=0)), 4),
        "f1": round(float(f1_score(y_true, y_pred, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_true, y_prob)), 4),
        "confusion_matrix": {
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn),
            "tp": int(tp),
        },
        "positive_rate": round(float(np.mean(y_true)), 4),
    }


def evaluate_salary(df: pd.DataFrame) -> dict:
    required = SALARY_FEATURES + ["salary"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Salary evaluation requires columns: {missing}")

    if ml_predictor.salary_model is None:
        raise RuntimeError("salary_model.pkl is not loaded. Train model first.")

    x = df[SALARY_FEATURES]
    y_true = df["salary"].to_numpy()
    y_pred = ml_predictor.salary_model.predict(x)

    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))

    return {
        "r2": round(float(r2_score(y_true, y_pred)), 4),
        "mae": round(float(mean_absolute_error(y_true, y_pred)), 4),
        "rmse": round(rmse, 4),
        "mape": round(_safe_mape(y_true, y_pred), 2),
        "mean_actual_salary": round(float(np.mean(y_true)), 3),
        "mean_predicted_salary": round(float(np.mean(y_pred)), 3),
    }


def build_report(results: dict) -> str:
    cls = results["placement"]
    reg = results["salary"]

    return f"""# Model Evaluation Report

Generated on: {results['generated_at']}
Dataset: {results['dataset']}
Sample count: {results['sample_count']}

## Placement Model (Classification)
- Accuracy: {cls['accuracy'] * 100:.2f}%
- Precision: {cls['precision'] * 100:.2f}%
- Recall: {cls['recall'] * 100:.2f}%
- F1 Score: {cls['f1'] * 100:.2f}%
- ROC-AUC: {cls['roc_auc']:.4f}
- Positive Rate: {cls['positive_rate'] * 100:.2f}%

Confusion Matrix:
- TN: {cls['confusion_matrix']['tn']}
- FP: {cls['confusion_matrix']['fp']}
- FN: {cls['confusion_matrix']['fn']}
- TP: {cls['confusion_matrix']['tp']}

## Salary Model (Regression)
- R2 Score: {reg['r2']:.4f}
- MAE: ₹ {reg['mae']:.3f} LPA
- RMSE: ₹ {reg['rmse']:.3f} LPA
- MAPE: {reg['mape']:.2f}%
- Mean Actual Salary: ₹ {reg['mean_actual_salary']:.3f} LPA
- Mean Predicted Salary: ₹ {reg['mean_predicted_salary']:.3f} LPA

## Notes
- These metrics are computed on the available dataset file in the workspace.
- For production trust, run this script on real historical placement outcomes.
"""


def main() -> None:
    df = load_dataset()

    results = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "dataset": "training_data_advanced.csv" if os.path.exists("training_data_advanced.csv") else "training_data.csv",
        "sample_count": int(len(df)),
        "placement": evaluate_placement(df),
        "salary": evaluate_salary(df),
    }

    with open("model_evaluation_report.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    report_md = build_report(results)
    with open("MODEL_EVALUATION_REPORT.md", "w", encoding="utf-8") as f:
        f.write(report_md)

    print("=" * 78)
    print("MODEL EVALUATION COMPLETE")
    print("=" * 78)
    print(report_md)
    print("Saved: model_evaluation_report.json")
    print("Saved: MODEL_EVALUATION_REPORT.md")


if __name__ == "__main__":
    main()
