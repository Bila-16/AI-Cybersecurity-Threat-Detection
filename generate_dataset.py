
import pandas as pd
import numpy as np

# Generate sample cybersecurity logs
rng = np.random.default_rng(42)

# Normal activities
normal = pd.DataFrame({
    "failed_attempts": rng.integers(0, 4, 950),
    "bytes_sent": rng.integers(200, 2000, 950),
    "hour": rng.integers(8, 21, 950)
})

# Suspicious activities
anomalies = pd.DataFrame({
    "failed_attempts": rng.integers(12, 40, 50),
    "bytes_sent": rng.integers(50000, 150000, 50),
    "hour": rng.integers(0, 24, 50)
})

# Combine the datasets
df = pd.concat(
    [normal, anomalies],
    ignore_index=True
)

# Shuffle records
df = df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

# Save the dataset
df.to_csv("data/training_logs.csv", index=False)

print("Dataset generated successfully!")
print("Total records:", len(df))
print(df.head())
