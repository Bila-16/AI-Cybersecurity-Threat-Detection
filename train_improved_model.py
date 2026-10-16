
import pandas as pd
import joblib
from pathlib import Path

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Load the new training dataset
df = pd.read_csv("data/realistic_train.csv")

features = [
    "failed_attempts",
    "bytes_sent",
    "hour"
]

X = df[features]

# Build the machine learning pipeline
model = Pipeline([
    ("scaler", StandardScaler()),
    ("detector", IsolationForest(
        n_estimators=200,
        contamination=0.10,
        random_state=42
    ))
])

# Train the model
model.fit(X)

# Save the improved model separately
Path("models").mkdir(exist_ok=True)

joblib.dump(
    model,
    "models/improved_threat_model.pkl"
)

print("Improved model trained successfully!")
print("Training records:", len(X))
print("Model saved to models/improved_threat_model.pkl")
