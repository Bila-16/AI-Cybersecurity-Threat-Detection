
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

# Step 1: Load the testing dataset
df = pd.read_csv("data/test_logs.csv")

# Step 2: Load trained model
model = joblib.load("models/threat_model.pkl")

# Step 3: Select model features
features = [
    "failed_attempts",
    "bytes_sent",
    "hour"
]

X_test = df[features]
y_true = df["actual_label"]

# Step 4: Predict using AI
predictions = model.predict(X_test)

# Convert predictions:
# Isolation Forest: -1 = anomaly, 1 = normal
# Our labels: 1 = suspicious, 0 = normal
y_pred = (predictions == -1).astype(int)

# Step 5: Calculate performance metrics
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(
    y_true, y_pred, zero_division=0
)
recall = recall_score(
    y_true, y_pred, zero_division=0
)
f1 = f1_score(
    y_true, y_pred, zero_division=0
)

print("\nAI MODEL EVALUATION")
print("-------------------------")

print(f"Accuracy:  {accuracy:.2%}")
print(f"Precision: {precision:.2%}")
print(f"Recall:    {recall:.2%}")
print(f"F1 Score:  {f1:.2%}")

print("\nConfusion Matrix:")
print(confusion_matrix(y_true, y_pred))

print("\nClassification Report:")
print(classification_report(
    y_true,
    y_pred,
    target_names=["Normal", "Suspicious"],
    zero_division=0
))

# Step 6: Save evaluation results
df["predicted_label"] = y_pred

df.to_csv(
    "data/evaluation_results.csv",
    index=False
)

print("\nEvaluation completed!")
