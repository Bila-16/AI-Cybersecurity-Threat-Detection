
import pandas as pd
import joblib

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

df = pd.read_csv("data/realistic_test.csv")

features = [
    "failed_attempts",
    "bytes_sent",
    "hour"
]

X_test = df[features]
y_true = df["actual_label"]

model = joblib.load(
    "models/improved_threat_model.pkl"
)

# Convert Isolation Forest predictions
predictions = model.predict(X_test)
y_pred = (predictions == -1).astype(int)

print("\nIMPROVED MODEL EVALUATION")
print("------------------------")

print(f"Accuracy:  {accuracy_score(y_true, y_pred):.2%}")
print(f"Precision: {precision_score(y_true, y_pred, zero_division=0):.2%}")
print(f"Recall:    {recall_score(y_true, y_pred, zero_division=0):.2%}")
print(f"F1 Score:  {f1_score(y_true, y_pred, zero_division=0):.2%}")

print("\nConfusion Matrix:")
print(confusion_matrix(
    y_true, y_pred, labels=[0, 1]
))

print("\nClassification Report:")
print(classification_report(
    y_true,
    y_pred,
    target_names=["Normal", "Suspicious"],
    zero_division=0
))

df["predicted_label"] = y_pred

df.to_csv(
    "data/improved_evaluation.csv",
    index=False
)

print("\nEvaluation completed!")
