
import pandas as pd
import numpy as np
from pathlib import Path

rng = np.random.default_rng(2026)
Path("data").mkdir(exist_ok=True)

def generate_logs(n_normal, n_suspicious, start_date):
    records = []
    start = pd.Timestamp(start_date)

    # Simulated normal events
    for i in range(n_normal):
        hour = int(rng.integers(0, 24))
        failed = int(rng.choice(
            [0, 1, 2, 3, 4, 5],
            p=[0.55, 0.20, 0.12, 0.07, 0.04, 0.02]
        ))

        traffic = int(rng.lognormal(7.5, 1.0))
        traffic = min(traffic, 60000)

        records.append({
            "timestamp": start + pd.Timedelta(
                hours=i % 168,
                minutes=int(rng.integers(0, 60))
            ),
            "source_ip": f"192.168.{int(rng.integers(1, 10))}.{int(rng.integers(1, 255))}",
            "event_type": "login_failed" if failed else "login_success",
            "failed_attempts": failed,
            "bytes_sent": traffic,
            "hour": hour,
            "actual_label": 0
        })

    # Simulated suspicious events
    for i in range(n_suspicious):
        pattern = i % 3

        if pattern == 0:
            # Repeated failed logins
            failed = int(rng.integers(8, 35))
            traffic = int(rng.integers(200, 10000))
            event = "login_failed"

        elif pattern == 1:
            # Unusually large traffic
            failed = int(rng.integers(0, 4))
            traffic = int(rng.integers(40000, 160000))
            event = "network_activity"

        else:
            # Mixed unusual activity
            failed = int(rng.integers(5, 25))
            traffic = int(rng.integers(15000, 100000))
            event = "login_failed"

        records.append({
            "timestamp": start + pd.Timedelta(
                hours=i % 168,
                minutes=int(rng.integers(0, 60))
            ),
            "source_ip": f"10.0.{int(rng.integers(1, 10))}.{int(rng.integers(1, 255))}",
            "event_type": event,
            "failed_attempts": failed,
            "bytes_sent": traffic,
            "hour": int(rng.integers(0, 24)),
            "actual_label": 1
        })

    df = pd.DataFrame(records)
    df = df.sample(
        frac=1,
        random_state=42
    ).reset_index(drop=True)

    return df

# Separate training and testing records
train = generate_logs(
    900, 100, "2026-09-01"
)

test = generate_logs(
    270, 30, "2026-10-01"
)

train.to_csv(
    "data/realistic_train.csv",
    index=False
)

test.to_csv(
    "data/realistic_test.csv",
    index=False
)

print("Datasets generated successfully!")
print("Training records:", len(train))
print("Testing records:", len(test))
print("\nTraining labels:")
print(train["actual_label"].value_counts())
print("\nTesting labels:")
print(test["actual_label"].value_counts())
