
import pandas as pd

# Step 1: Load the dataset
df = pd.read_csv("data/sample_logs.csv")

print("Original Dataset:")
print(df)

# Step 2: Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Step 3: Remove duplicates
df = df.drop_duplicates()

# Step 4: Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Step 5: Extract hour from timestamp
df["hour"] = df["timestamp"].dt.hour

# Step 6: Select numerical features
features = df[[
    "failed_attempts",
    "bytes_sent",
    "hour"
]]

print("\nProcessed Features:")
print(features)

# Step 7: Save cleaned dataset
df.to_csv("data/cleaned_logs.csv", index=False)

print("\nData preprocessing completed!")
print("Cleaned dataset saved successfully.")
