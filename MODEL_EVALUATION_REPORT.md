# Model Evaluation Report

Generated on: 2026-03-14T08:18:27
Dataset: training_data_advanced.csv
Sample count: 50000

## Placement Model (Classification)
- Accuracy: 99.79%
- Precision: 99.79%
- Recall: 99.99%
- F1 Score: 99.89%
- ROC-AUC: 0.9783
- Positive Rate: 97.60%

Confusion Matrix:
- TN: 1098
- FP: 103
- FN: 3
- TP: 48796

## Salary Model (Regression)
- R2 Score: 0.8833
- MAE: ₹ 0.479 LPA
- RMSE: ₹ 0.628 LPA
- MAPE: 5.83%
- Mean Actual Salary: ₹ 8.759 LPA
- Mean Predicted Salary: ₹ 8.757 LPA

## Notes
- These metrics are computed on the available dataset file in the workspace.
- For production trust, run this script on real historical placement outcomes.
