
import pandas as pd
import numpy as np

# Different seed from training data
rng = np.random.default_rng(123)

# Generate 190 normal logs
normal = pd.DataFrame({
    "failed_attempts": rng.integers(0, 4, 190),
    "bytes_sent": rng.integers(200, 2000, 190),
    "hour": rng.integers(8, 21, 190),
    "actual_label": 0
})

# Generate 10 simulated suspicious logs
attacks = pd.DataFrame({
    "failed_attempts": rng.integers(12, 40, 10),
    "bytes_sent": rng.integers(50000, 150000, 10),
    "hour": rng.integers(0, 24, 10),
    "actual_label": 1
})

# Combine the records
df = pd.concat(
    [normal, attacks],
    ignore_index=True
)

# Shuffle the dataset
df = df.sample(
    frac=1,
    random_state=123
).reset_index(drop=True)

# Save testing data
df.to_csv(
    "data/test_logs.csv",
    index=False
)

print("Testing dataset generated successfully!")
print("Total testing records:", len(df))
print("\nActual labels:")
print(df["actual_label"].value_counts())
