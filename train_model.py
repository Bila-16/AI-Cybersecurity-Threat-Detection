
import pandas as pd
import joblib
import os

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Step 1: Load the dataset
df = pd.read_csv("data/training_logs.csv")

print("Dataset loaded successfully!")
print("Total records:", len(df))

# Step 2: Select features for training
features = [
    "failed_attempts",
    "bytes_sent",
    "hour"
]

X = df[features]

# Step 3: Create the machine learning model
model = Pipeline([
    ("scaler", StandardScaler()),
    ("detector", IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    ))
])

# Step 4: Train the model
model.fit(X)

print("\nModel training completed!")

# Step 5: Predict anomalies
predictions = model.predict(X)

# 1 means normal, -1 means anomaly
df["prediction"] = predictions

df["status"] = df["prediction"].map({
    1: "Normal",
    -1: "Suspicious"
})

# Step 6: Display results
print("\nAI Threat Detection Results:")
print(df["status"].value_counts())

# Step 7: Save the trained model
os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/threat_model.pkl")

print("\nModel saved successfully!")

# Step 8: Save prediction results
df.to_csv("data/prediction_results.csv", index=False)

print("Prediction results saved!")
